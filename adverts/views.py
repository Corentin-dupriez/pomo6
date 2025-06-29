import json
from django.db.models.functions import Coalesce, TruncDate
from django.http import HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404
from django.db.models import Q, Avg, Count, ExpressionWrapper, FloatField, QuerySet
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, FormView
from adverts.forms import AdvertForm, SearchForm, RatingResponseForm
from adverts.models import Advertisement, Views, Ratings


class ResultsView(ListView):
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

        queryset = Advertisement.objects.all().annotate(
            avg_rating=Coalesce(Avg('orders__ratings__rating'), 0, output_field=FloatField()),
            customers = Count('orders', filter=Q(orders__completed=True), distinct=True, output_field=FloatField()),
            note=ExpressionWrapper(
                Coalesce(Avg('orders__ratings__rating'), 0)* 0.7 +
                Count('orders', filter=Q(orders__completed=True), distinct=True) * 0.3,
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
            queryset = queryset.filter(Q(fixed_price__gte=min_price)|
                                       Q(min_price__gte=min_price)|
                                       Q(min_price__lte=max_price))

        if max_price:
            queryset = queryset.filter(Q(fixed_price__lte=max_price)|
                                       Q(fixed_price__isnull=True)|
                                       Q(max_price__lte=max_price))

        return queryset.order_by('-note')

    def get_context_data(self, *, object_list = ..., **kwargs) -> dict:
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

        labels = [row['date'].strftime('%Y-%m-%d') for row in queryset]
        data = [row['count'] for row in queryset]
        context['connected_user'] = self.request.user
        context["labels"] = json.dumps(labels)
        context["data"] = json.dumps(data)

        return context

    def get_template_names(self) -> list:
        if self.request.user.is_authenticated and (self.request.user.is_superuser or self.request.user == self.object.user):
            return ['listings/view-listing-by-owner.html']
        else:
            return ['listings/view-listing.html']

    def get_object(self, queryset:QuerySet=None) -> Advertisement:
        queryset = Advertisement.objects.annotate(
            avg_rating=Coalesce(Avg('orders__ratings__rating'), 0, output_field=FloatField()),
            nb_ratings=Coalesce(Count('orders', filter=Q(orders__completed=True), distinct=True), 0),
        ).prefetch_related('orders__ratings').prefetch_related('orders__ratings__responses')
        return get_object_or_404(queryset, pk=self.kwargs.get('pk'))

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        self.object = self.get_object()
        if not self.request.user.is_superuser and self.request.user != self.object.user:
            self.object.increase_views()
        return super().get(request, *args, **kwargs)
    
    def form_valid(self, form) -> HttpResponse:
        rating_id = form.cleaned_data['to_rating_id']
        
        rating = get_object_or_404(Ratings, pk=rating_id)
        
        response = form.save(commit=False)
        response.to_rating = rating
        response.save()
        
        return super().form_valid(form)


class ListingCreateView(CreateView):
    model = Advertisement
    form_class = AdvertForm
    template_name = 'listings/new-listing.html'
    success_url = reverse_lazy('home')

    def get_form_kwargs(self) -> dict:
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class ListingUpdateView(UpdateView):
    model = Advertisement
    form_class = AdvertForm
    template_name = 'listings/new-listing.html'
    success_url = reverse_lazy('home')

