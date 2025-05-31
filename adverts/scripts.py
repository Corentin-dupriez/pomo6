import random

import os
import django
from django.utils.text import slugify

# Set the environment variable to your settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pomo6.settings')

# Initialize Django
django.setup()

from adverts.models import Advertisement

def create_add() -> list:
    categories = [
        'IT', 'HANDYMAN', 'CLEANING', 'CHILDCARE',
        'TUTORING', 'TRANSPORTATION', 'PET', 'OTHER'
    ]

    ads = [
        {
            'category': 'IT',
            'title': 'Fix any computer issues remotely within 1 hour',
            'description': 'I offer remote IT support for both Windows and Mac systems. I can troubleshoot slow performance, remove viruses, optimize your system, and help with software installations.'
        },
        {
            'category': 'IT',
            'title': 'Build and deploy your website with Django',
            'description': 'As a full-stack web developer, I specialize in Django-based websites. I will help you design, develop, and deploy a custom solution including user authentication, admin panels, and secure hosting.'
        },
        {
            'category': 'HANDYMAN',
            'title': 'Assemble IKEA furniture quickly and reliably',
            'description': 'Don’t waste time trying to decode furniture instructions. I will come to your home and assemble your IKEA (or any brand) furniture efficiently and securely.'
        },
        {
            'category': 'HANDYMAN',
            'title': 'Fix broken door hinges and handles',
            'description': 'Need help with squeaky or broken door parts? I’ll bring tools and fix or replace your hinges, handles, and locks in no time.'
        },
        {
            'category': 'CLEANING',
            'title': 'Deep clean your entire kitchen and bathroom',
            'description': 'I provide thorough cleaning services with professional-grade supplies, leaving your kitchen and bathroom spotless and hygienic.'
        },
        {
            'category': 'CLEANING',
            'title': 'Post-construction cleaning service',
            'description': 'Just finished a renovation or remodeling? I specialize in post-construction clean-ups — removing dust, paint stains, and debris with attention to detail.'
        },
        {
            'category': 'CHILDCARE',
            'title': 'Experienced babysitter for evenings and weekends',
            'description': 'I’m a certified childcare provider with 5+ years of experience. I offer responsible, caring babysitting services with fun, educational activities.'
        },
        {
            'category': 'CHILDCARE',
            'title': 'Weekend nanny available - CPR certified',
            'description': 'Looking for help on weekends? I provide safe and engaging care for children of all ages, and I’m trained in emergency response.'
        },
        {
            'category': 'TUTORING',
            'title': 'Math tutor for high school and college students',
            'description': 'Struggling with algebra, geometry, or calculus? I break down difficult concepts and help you build problem-solving skills with customized practice.'
        },
        {
            'category': 'TUTORING',
            'title': 'Learn Spanish from a native speaker',
            'description': 'I offer beginner to advanced Spanish tutoring, focusing on conversation, grammar, and culture. Virtual and in-person sessions available.'
        },
        {
            'category': 'TRANSPORTATION',
            'title': 'Reliable airport drop-off and pick-up',
            'description': 'I provide timely and professional airport transportation with clean vehicles and flexible scheduling. Luggage assistance included.'
        },
        {
            'category': 'TRANSPORTATION',
            'title': 'Moving help with large van',
            'description': 'Need to move furniture or boxes across town? I offer moving services with a spacious van and extra hands to lift and load.'
        },
        {
            'category': 'PET',
            'title': 'Daily dog walking in your neighborhood',
            'description': 'I offer weekday and weekend dog walking services. Reliable, caring, and insured. Great with all dog breeds!'
        },
        {
            'category': 'PET',
            'title': 'Cat sitting and litter box cleaning',
            'description': 'I’ll visit your home to feed, play with, and clean up after your cat while you’re away. Personalized care and updates provided.'
        },
        {
            'category': 'OTHER',
            'title': 'Help setting up your smart home devices',
            'description': 'Need assistance setting up Alexa, Google Home, or smart lights? I’ll configure everything and make sure it works seamlessly with your phone.'
        },
        {
            'category': 'OTHER',
            'title': 'Virtual assistant for scheduling and emails',
            'description': 'Busy schedule? I can help manage your calendar, send reminders, organize emails, and handle basic admin tasks remotely.'
        },
        # 34 more randomly generated entries
    ]

    # Add random variations to generate 50
    while len(ads) < 50:
        category = random.choice(categories)
        title = f"{random.choice(['Quick', 'Professional', 'Affordable', 'Reliable'])} {category.lower()} service for your needs"
        description = (
            f"I offer high-quality {category.lower()} services tailored to your specific situation. "
            "I’m experienced, punctual, and focused on providing great value. Let’s work together to get the job done!"
        )
        ads.append({
            'category': category,
            'title': title[:100],
            'description': description[:2000]
        })

    for ad in ads:
        ad['slug'] = slugify(ad['title'])

    return ads

def populate_data():
    adds_to_create = create_add()
    listings = [Advertisement(**ad) for ad in adds_to_create]
    Advertisement.objects.bulk_create(listings)

populate_data()