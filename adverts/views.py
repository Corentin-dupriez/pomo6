from django.db.models.functions import Coalesce
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q, Avg, Count, ExpressionWrapper, FloatField
from django.core.paginator import Paginator

from adverts.forms import AdvertForm
from adverts.models import Advertisement, Ratings, Order


#Search view used to filter and display the results of the search
def search_view(request):
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category')
    min_rating = request.GET.get('min_rating', 0)
    max_rating = request.GET.get('max_rating', 5)
    category_choices = Advertisement.CategoryChoices.choices

    #annotate the results to get the ratings and customers of the listing
    #also add another column weighing the ratings and customer numbers
    adverts = Advertisement.objects.all().annotate(
        avg_rating=Coalesce(Avg('orders__ratings__rating'), 0, output_field=FloatField()),
        customers = Count('orders', filter=Q(orders__completed=True), distinct=True, output_field=FloatField()),
        note=ExpressionWrapper(
            Coalesce(Avg('orders__ratings__rating'), 0)* 0.7 +
            Count('orders', filter=Q(orders__completed=True), distinct=True) * 0.3,
            output_field=FloatField()
        )
    ).order_by('-note')

    if query:
        adverts = adverts.filter(Q(title__icontains=query) |
                                    Q(description__icontains=query) |
                                    Q(category__icontains=query))

    if category :
        adverts = adverts.filter(Q(category = category))

    if min_rating:
        adverts = adverts.filter(Q(avg_rating__gte=min_rating))

    if max_rating:
        adverts = adverts.filter(Q(avg_rating__lte=max_rating))

    #create a paginator objet to return 5 results per page
    paginator = Paginator(adverts, 5)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    context = {
        'adverts': page_obj,
        'category': category,
        'query': query,
        'min_rating': min_rating,
        'max_rating': max_rating,
        'category_choices': category_choices,
    }

    return render(request, 'search.html', context)

def advert_view(request, pk: int, slug: str):
    advert = Advertisement.objects.filter(id=pk).first()

    context = {
        'advert' : advert,
    }

    return render(request, 'view-listing.html', context)

def create_ad_view(request):
    form = AdvertForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()

    context = {'form': form}
    return render(request, 'new_add.html', context)

