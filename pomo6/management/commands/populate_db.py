import random

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from django.db.models import QuerySet
from django.utils.text import slugify

from adverts.models import Advertisement
from search_indexing.utils import index_ad, calculate_tf_idf

UserModel = get_user_model()

class Command(BaseCommand):
    @staticmethod
    def generate_it_advert_title():
        verbs = ['develop ', 'build ', 'fix ', 'debug ', 'improve ', 'review ', 'design ']
        techs = ['a Django website',
                 'a website developed in React',
                 'anything using Python',
                 'a web app with Python',
                 'any software using Java',
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def generate_childcare_advert_title():
        verbs = ['watch ', 'look after ', 'babysit ']
        things = ['your kids',
                  'kids older than 6',
                  'your baby',
                  'your kid for a whole afternoon!',
                  'children under 5',
                  'children, and make them play the whole day!',
                  'kids using Montessori',
                  'your kids and teach them good manners']
        return random.choice(verbs) + random.choice(things)

    @staticmethod
    def generate_tutoring_advert_title():
        verbs = ['teach you ',
                 'tutor you in ',
                 'help you understand ',
                 'help you learn ',
                 'train you ',
                 'upskill you in ',
                 'teach you or your kids ',
                 'tutor your kids in ']
        things = ['maths',
                  'physics',
                  'calculus',
                  'French',
                  'computer science',
                  'English',
                  'mathematics',
                  'language learning',
                  'multiplication tables',
                  'algebra',
                  'Python',
                  'any subject'
                  ]
        return random.choice(verbs) + random.choice(things)

    @staticmethod
    def generate_pet_advert_title():
        verbs = ['walk ',
                 'watch ',
                 'look after ',
                 'train ',
                 'feed ']
        things = ['your dog',
                  'your animals',
                  'your cats',
                  'dogs or cats',
                  'small dogs',
                  'french bulldogs',
                  'exotic pets',
                  'cats',
                  'and give love to your pets',
                  'your pets while you\'re away']
        return random.choice(verbs) + random.choice(things)

    def generate_title(self, category: str):
        title_starts = ['I can ', 'I will ']
        title_map = {
            'IT': self.generate_it_advert_title,
            'HANDYMAN': self.generate_handyman_advert_title,
            'CLEANING': self.generate_cleaning_advert_title,
            'CHILDCARE': self.generate_childcare_advert_title,
            'TUTORING': self.generate_tutoring_advert_title,
            'PET': self.generate_pet_advert_title,
        }
        title = title_starts[random.randint(0, len(title_starts) - 1)]
        title += title_map[category]()
        return title

    @staticmethod
    def get_existing_users():
        users = UserModel.objects.all()
        return users

    def generate_advertisement(self, category: str, users: QuerySet, nb_advertisements: int) -> list[Advertisement]:
        advertisements = []
        adverts_number = nb_advertisements
        for _ in range(adverts_number):
            title = self.generate_title(category)
            user = random.choice(users)
            advertisement = Advertisement(title=title,
                                          category=category,
                                          user=user,
                                          slug=slugify(title),
                                          description=title,
                                          fixed_price=random.randint(1, 500),
                                          is_fixed_price=True,
                                          approved=True)
            advertisements.append(advertisement)
        return advertisements

    def handle(self, *args, **options):
        categories = [category[0] for category in Advertisement.CategoryChoices.choices]
        existing_users_pks = self.get_existing_users()

        all_adverts_to_commit = []

        for category in categories:
            adverts = self.generate_advertisement(category, existing_users_pks, nb_advertisements=random.randint(80, 100))
            print(f'Generated {len(adverts)} advertisements for {category}')
            all_adverts_to_commit.extend(adverts)

        print(f'Generated {len(all_adverts_to_commit)} advertisements')

        user_input = input('Are you sure you want to create the advertisements? (y/n)')
        if user_input == 'y':
            print('Saving advertisements')
            commited_adverts = Advertisement.objects.bulk_create(all_adverts_to_commit)
            print('Advertisements saved!')

            for advert in commited_adverts:
                index_ad(advert)

            calculate_tf_idf()
            print('Adverts indexed and tf-idf calculated!')

        else:
            print('Aborting')