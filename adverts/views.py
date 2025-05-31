from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q


from adverts.models import Advertisement


# Create your views here.
def search_view(request):
    query = request.GET.get('q')
    category = request.GET.get('category')
    category_choices = Advertisement.CategoryChoices.choices
    adverts = None
    if query is not None:
        adverts = Advertisement.objects.filter(Q(title__icontains=query) |
                                               Q(description__icontains=query) |
                                               Q(category__icontains=query))
    if category:
        adverts = Advertisement.objects.filter(category=category)

    context = {
        'adverts': adverts,
        'category_choices': category_choices,
    }

    return render(request, 'search.html', context)

def advert_view(request, pk: int, slug: str):
    adverts = Advertisement.objects.filter(id=pk).first()
    return HttpResponse(f'<h1>{adverts.title}</h1>')