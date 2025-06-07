from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator

from adverts.forms import AdvertForm
from adverts.models import Advertisement


# Create your views here.
def search_view(request):
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category')
    category_choices = Advertisement.CategoryChoices.choices
    adverts = Advertisement.objects.all()

    if query:
        adverts = adverts.filter(Q(title__icontains=query) |
                                    Q(description__icontains=query) |
                                    Q(category__icontains=query))

    if category :
        adverts = adverts.filter((Q(title__icontains=query) |
                                               Q(description__icontains=query) |
                                               Q(category__icontains=query)) &
                                               Q(category = category))


    paginator = Paginator(adverts, 5)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    context = {
        'adverts': page_obj,
        'category': category,
        'query': query,
        'category_choices': category_choices,
    }

    return render(request, 'search.html', context)

def advert_view(request, pk: int, slug: str):
    advert = Advertisement.objects.filter(id=pk).first()

    context = {
        'advert' : advert
    }

    return render(request, 'view-listing.html', context)

def create_ad_view(request):
    form = AdvertForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()

    context = {'form': form}
    return render(request, 'new_add.html', context)

