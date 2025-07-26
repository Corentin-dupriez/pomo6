import json
import os
import joblib
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.functions import Coalesce, TruncDate
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.db.models import Q, Avg, Count, ExpressionWrapper, FloatField, QuerySet
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, FormView, DeleteView
from drf_spectacular.utils import extend_schema
from adverts.forms import AdvertForm, SearchForm, RatingResponseForm, OrderForm, UpdateOrderForm
from adverts.models import Advertisement, Views, Ratings, Order
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from adverts.permissions import IsOrderOwnerOrClient
from adverts.serializers import OrderUpdateSerializer, ListingUpdateSerializer, PredictCategorySerializer
from chat.models import Thread
from common import permissions

#import model and vectorizer required for API
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model = joblib.load(os.path.join(BASE_DIR, "ml_model", "model.pkl"))
vectorizer = joblib.load(os.path.join(BASE_DIR, "ml_model", "vectorizer.pkl"))


class BaseResultsView(ListView):
    # This is the base results view. It returns the advert adverts matching the search criteria.
    # It is inherited by other views (such as my adverts).
    model = Advertisement
    template_name = 'search.html'
    form_class = SearchForm
    paginate_by = 5
    paginator_class = Paginator

    def get_ratings(self) -> tuple:
        try:
            min_rating = int(self.request.GET.get('min_rating', 0))
        except ValueError:
            min_rating = 0

        try:
            max_rating = int(self.request.GET.get('max_rating', 5))
        except ValueError:
            max_rating = 5

        return min_rating, max_rating

    def get_queryset(self) -> QuerySet:
        query = self.request.GET.get('query', '').strip()
        category = self.request.GET.get('category')

        min_rating, max_rating = self.get_ratings()

        min_price = int(self.request.GET.get('min_price', 0))
        max_price = int(self.request.GET.get('max_price', 1000))

        #To the queryset, we add a note column, which is based on average rating and orders count
        queryset = Advertisement.objects.all().annotate(
            avg_rating=Coalesce(Avg('orders__ratings__rating'), 0, output_field=FloatField()),
            customers=Count('orders', filter=Q(orders__status='COMPLETED'), distinct=True, output_field=FloatField()),
            note=ExpressionWrapper(
                Coalesce(Avg('orders__ratings__rating'), 0) * 0.7 +
                Count('orders', filter=Q(orders__status='COMPLETED'), distinct=True) * 0.3,
                output_field=FloatField()
            )
        )

        if query:
            queryset = queryset.filter(Q(title__icontains=query) |
                                       Q(description__icontains=query) |
                                       Q(category__icontains=query))

        if category:
            queryset = queryset.filter(category=category)

        if min_rating:
            queryset = queryset.filter(Q(note__gte=min_rating))

        if max_rating:
            queryset = queryset.filter(Q(note__lte=max_rating))

        if min_price:
            queryset = queryset.filter(Q(fixed_price__gte=min_price) |
                                       Q(min_price__gte=min_price) |
                                       Q(min_price__lte=max_price))

        if max_price:
            queryset = queryset.filter(Q(fixed_price__lte=max_price) |
                                       Q(fixed_price__isnull=True) |
                                       Q(max_price__lte=max_price))

        return queryset.order_by('-note')

    def get_context_data(self, *, object_list=..., **kwargs) -> dict:
        min_rating, max_rating = self.get_ratings()

        min_price = int(self.request.GET.get('min_price', 0))
        max_price = int(self.request.GET.get('max_price', 1000))

        context = super().get_context_data(**kwargs)
        context.update({
            'form': self.form_class(self.request.GET or None),
            'query': self.request.GET.get('query', ''),
            'category': self.request.GET.get('category', ''),
            'min_rating': min_rating,
            'max_rating': max_rating,
            'min_price': min_price,
            'max_price': max_price,
        })
        return context

class ResultsView(BaseResultsView):
    #Get the queryset of the base view, and filter it to return only approved and not archived listings
    #This view is used to display search results on the search page
    def get_queryset(self) -> QuerySet:
        query = super().get_queryset()
        query = query.filter(approved=True, archived=False)
        return query


class ListingView(DetailView, FormView):
    model = Advertisement
    form_class = RatingResponseForm

    def get_success_url(self) -> str:
        return reverse_lazy('advert_view', kwargs={'pk': self.kwargs.get('pk'),
                                                   'slug': self.kwargs.get('slug')})

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)

        queryset = (Views.objects.filter(advertisement=context['object'])
                    .annotate(date=TruncDate('view_date'))
                    .values('date')
                    .annotate(count=Count('id'))
                    .order_by('date'))

        #The following is used to display the graph containing the views of the listing
        labels = [row['date'].strftime('%Y-%m-%d') for row in queryset]
        data = [row['count'] for row in queryset]
        context['connected_user'] = self.request.user
        context["labels"] = json.dumps(labels)
        context["data"] = json.dumps(data)

        return context


    def get_template_names(self) -> list:
        if self.request.user.is_authenticated and self.request.user == self.object.user:
            return ['adverts/view-listing-by-owner.html']
        else:
            return ['adverts/view-listing.html']


    def get_object(self, queryset:QuerySet=None) -> Advertisement:
        queryset = Advertisement.objects.annotate(
            avg_rating=Coalesce(Avg('orders__ratings__rating'), 0, output_field=FloatField()),
            nb_ratings=Coalesce(Count('orders', filter=Q(orders__status='COMPLETED'), distinct=True), 0),
        ).prefetch_related('orders__ratings').prefetch_related('orders__ratings__responses')
        return get_object_or_404(queryset, pk=self.kwargs.get('pk'))


    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        self.object = self.get_object()
        #increase the number of views if the user is not superuser or the listing creator
        if not self.request.user.is_superuser and self.request.user != self.object.user:
            self.object.increase_views()
        return super().get(request, *args, **kwargs)


    def form_valid(self, form) -> HttpResponse:
        #Used to add a response to a rating comment
        rating_id = form.cleaned_data['to_rating_id']
        
        rating = get_object_or_404(Ratings, pk=rating_id)
        
        response = form.save(commit=False)
        response.to_rating = rating
        response.save()
        
        return super().form_valid(form)


class MyListingsView(BaseResultsView):
    def get_queryset(self) -> QuerySet:
        #Get the queryset of the base view, but filter for the results of the connected user
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs) -> dict:
        ctx = super().get_context_data()
        ctx['my_listings'] = True
        return ctx

class ListingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Advertisement
    success_url = reverse_lazy('home')

    def test_func(self):
        obj = self.get_object()
        return self.request.user.is_superuser or self.request.user == obj.user

    def delete(self, request, *args, **kwargs) -> HttpResponse:
        self.object = self.get_object()
        if self.object.approved:
            self.object.archived = True
            self.object.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super().post(request, *args, **kwargs)


class ListingsToApproveView(UserPassesTestMixin, LoginRequiredMixin, BaseResultsView):

    def get_context_data(self, *, object_list=..., **kwargs) -> dict:
        ctx = super().get_context_data()
        ctx['to_approve'] = True
        return ctx

    def test_func(self) -> bool:
        return self.request.user.is_superuser #TODO: Add check on the user's authorizations

    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset()
        queryset = queryset.filter(approved=False)
        return queryset


class ListingCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Advertisement
    form_class = AdvertForm
    template_name = 'adverts/new-listing.html'
    success_url = reverse_lazy('home')
    success_message = "Advert created successfully"

    def get_form_kwargs(self) -> dict:
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class ListingUpdateView(UserPassesTestMixin, SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Advertisement
    form_class = AdvertForm
    template_name = 'adverts/new-listing.html'
    success_url = reverse_lazy('home')
    success_message = "Advert updated successfully"

    def get_form_kwargs(self) -> dict:
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, *, object_list=..., **kwargs) -> dict:
        ctx = super().get_context_data(**kwargs)
        #Used to change the heading of the page from 'Create a new listing' to 'Update a listing'
        ctx['update_listing'] = True
        return ctx

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user

class CreateOrderView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/new_order.html'
    success_url = reverse_lazy('home')
    success_message = "Order created successfully"

    def get_form_kwargs(self) -> dict:
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['advert_id'] = self.kwargs.get('pk')
        kwargs['thread_id'] = Thread.objects.filter(participants=self.request.user, advert=self.kwargs.get('pk')).first().id
        return kwargs

    def test_func(self):
        advert = get_object_or_404(Advertisement, pk=self.kwargs.get('pk'))
        return advert.user == self.request.user

class UpdateOrderView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, UpdateView):
    model = Order
    form_class = UpdateOrderForm
    template_name = 'orders/new_order.html'
    success_message = 'Order updated successfully'

    def test_func(self):
        offer = get_object_or_404(Order, pk=self.kwargs.get('pk'))
        return offer.user == self.request.user

    def get_initial(self) -> dict:
        object = get_object_or_404(Order, pk=self.kwargs.get('pk'))
        return object.__dict__

    def get_success_url(self) -> str:
        return reverse_lazy('order_detail', kwargs={'pk': self.kwargs.get('pk')})

class OrderDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Order
    template_name = 'orders/order.html'

    def test_func(self):
        order = get_object_or_404(Order, pk=self.kwargs.get('pk'))
        return order.user == self.request.user or order.advertisement.user == self.request.user

class PredictCategoryView(APIView):
    @extend_schema(
        request=PredictCategorySerializer,
    )

    def post(self, request, *args, **kwargs):
        title = request.data.get('title', '')

        if not title:
            return Response({'error': 'title is required'}, status=status.HTTP_400_BAD_REQUEST)

        title_vec = vectorizer.transform([title])
        predicted_category = model.predict(title_vec)[0]

        return Response({'predicted_category': predicted_category}, status=status.HTTP_200_OK)

class UpdateOrderStatusView(generics.UpdateAPIView):
    model = Order
    serializer_class = OrderUpdateSerializer
    queryset = Order.objects.all()
    permission_classes = (IsOrderOwnerOrClient,)
    http_method_names = ['patch']

    def patch(self, request, *args, **kwargs):
        order = self.get_object()
        serializer = self.get_serializer(instance=order,
                                         data=request.data,
                                         partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': 'success'}, status=status.HTTP_200_OK)

class ApproveListingView(generics.UpdateAPIView):
    model = Advertisement
    serializer_class = ListingUpdateSerializer
    queryset = Advertisement.objects.all()
    permission_classes = (permissions.IsStaff,)
    http_method_names = ['patch']

    def patch(self, request, *args, **kwargs):
        listing = self.get_object()
        serializer = self.get_serializer(instance=listing,
                                         data=request.data,
                                         partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': 'success'}, status=status.HTTP_200_OK)