from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q

from adverts.forms import AdvertForm
from adverts.models import Advertisement


# Create your views here.
def search_view(request):
    query = request.GET.get('q')
    category = request.GET.get('category')
    category_choices = Advertisement.CategoryChoices.choices
    adverts = None
    if query != '' and category is None:
        adverts = Advertisement.objects.filter(Q(title__icontains=query) |
                                               Q(description__icontains=query) |
                                               Q(category__icontains=query))
    if query != '' and query is not None and category is not None:
        adverts = Advertisement.objects.filter((Q(title__icontains=query) |
                                               Q(description__icontains=query) |
                                               Q(category__icontains=query)) &
                                               Q(category = category))
    if (query == '' or query is None) and category is not None:
        adverts = Advertisement.objects.filter(category=category)
    if (query == '' or query is None) and category is None:
        adverts = Advertisement.objects.all()

    context = {
        'adverts': adverts,
        'category_choices': category_choices,
    }

    return render(request, 'search.html', context)

def advert_view(request, pk: int, slug: str):
    adverts = Advertisement.objects.filter(id=pk).first()
    return HttpResponse(f'<h1>{adverts.title}</h1>')

def create_ad_view(request):
    form = AdvertForm(request.POST or None)
    context = {'form': form}
    return render(request, 'new_add.html', context)