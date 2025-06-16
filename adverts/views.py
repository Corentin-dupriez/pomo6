from django.db.models.functions import Coalesce
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q, Avg, Count, ExpressionWrapper, FloatField
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from adverts.forms import AdvertForm, SearchForm
from adverts.models import Advertisement, Ratings, Order

class ResultsView(ListView):
    model = Advertisement
    template_name = 'search.html'
    form_class = SearchForm
    paginate_by = 5
    paginator_class = Paginator

    def get_queryset(self):
        query = self.request.GET.get('query', '').strip()
        category = self.request.GET.get('category')

        try:
            min_rating = int(self.request.GET.get('min_rating', 0))
        except ValueError:
            min_rating = 0

        try:
            max_rating = int(self.request.GET.get('max_rating', 5))
        except ValueError:
            max_rating = 5

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

    def get_context_data(
        self, *, object_list = ..., **kwargs
    ):
        try:
            min_rating = int(self.request.GET.get('min_rating', 0))
        except ValueError:
            min_rating = 0

        try:
            max_rating = int(self.request.GET.get('max_rating', 5))
        except ValueError:
            max_rating = 5

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


class ListingView(DetailView):
    model = Advertisement
    template_name = 'view-listing.html'

class ListingCreateView(CreateView):
    model = Advertisement
    form_class = AdvertForm
    template_name = 'new-listing.html'
    success_url = reverse_lazy('home')

class ListingUpdateView(UpdateView):
    model = Advertisement
    form_class = AdvertForm
    template_name = 'new-listing.html'
    success_url = reverse_lazy('home')

