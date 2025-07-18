import os
import random

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pomo6.settings')
django.setup()

from adverts.models import Advertisement

def generate_it_advert_title():
    verbs = ['develop ', 'build ', 'fix ', 'debug ', 'improve ', 'review ', 'design ']
    techs = ['a Django website',
             'a website developed in React',
             'a Java application',
             'an API in the technology of your choice',
             'a WordPress or Blogger website',
             'any application in JS',
             'a React Web App',
             'anything done with COBOL',
             'a Go application',
             'a game done with C#',
             'a Windows App',
             'an iOS application',
             'an Android app',
             'a full stack website',
             'a WordPress website',
             'a shopify website',
             'an enterprise application',
             ]
    return random.choice(verbs) + random.choice(techs)


def generate_handyman_advert_title():
    verbs = ['install ', 'build ', 'make ', 'manufacture ', 'fix ']
    things = ['a sink',
              'a wardrobe',
              'any hardwood furniture you want',
              'wooden furniture',
              'IKEA furniture',
              'beds, sofas, and armchairs',
              'shower cabins',
              'bathtubs',
              'furniture',
              'an oven',
              'a TV',
              'a fridge',
              'a custom kitchen']
    return random.choice(verbs) + random.choice(things)


def generate_cleaning_advert_title():
    verbs = ['clean ',
             'clean up ',
             'wash ',
             'scrub ',
             'polish ',
             'disinfect ']
    things = ['your apartment',
              'your house or apartment',
              'your garage',
              'your bed',
              'your furniture',
              'your AC',
              'anything you need',
              'cars',
              'your kitchen',
              'your kitchen with natural products',
              'your floors and make them spark!']
    return random.choice(verbs) + random.choice(things)

def generate_childcare_advert_title():
    pass

def generate_tutoring_advert_title():
    pass

def generate_transport_advert_title():
    pass

def generate_pet_advert_title():
    pass

def generate_other_advert_title():
    pass

def generate_title(category: str):
    title_starts = ['I can ', 'I will ']
    title_map = {
        'IT': generate_it_advert_title,
        'HANDYMAN': generate_handyman_advert_title,
        'CLEANING': generate_cleaning_advert_title,
        'CHILDCARE': generate_childcare_advert_title,
        'TUTORING': generate_tutoring_advert_title,
        'TRANSPORTATION': generate_tutoring_advert_title,
        'PET': generate_pet_advert_title,
        'OTHER': generate_other_advert_title,
    }
    title = title_starts[random.randint(0, len(title_starts) - 1)]
    title += title_map[category]()
    return title


def generate_advertisement(category: str, nb_advertisements: int) -> list[Advertisement]:
    advertisements = []
    adverts_number = nb_advertisements
    for _ in range(adverts_number):
        title = generate_title(category)
        advertisement = Advertisement(title=title, category=category)
        advertisements.append(advertisement)
    return advertisements

categories = [category[0] for category in Advertisement.CategoryChoices.choices]

for category in categories:
    print(f'Category: {category}')
    adverts = generate_advertisement(category, nb_advertisements=5)
    print(f'Advertisements: {", ". join(advert.title for advert in adverts)}')