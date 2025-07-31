import math
from django.core.management import BaseCommand
from django.db.models import Count, F
from search_indexing.utils import index_ad
from adverts.models import Advertisement
from search_indexing.models import SearchIndex


class Command(BaseCommand):
    help = 'Index ads.'

    def handle(self, *args, **options):
        #Delete existing index
        SearchIndex.objects.all().delete()

        #Get all advertisements that are approved and not archived -> they are indexed
        advertisements = Advertisement.objects.filter(
            approved=True,
            archived=False,
        )

        #Build the index containing word, advert, title and description TF
        for adv in advertisements:
            index_ad(adv)

        #Calculate IDF: We get the number of ads where each word appears and the total number of ads
        indexes = (SearchIndex.objects.values('word')
                   .annotate(doc_count=Count('advert', distinct=True)))
        advert_number = Advertisement.objects.count()

        for index in indexes:
            word = index['word']
            df = index['doc_count']
            idf = math.log(advert_number / (1+df))
            #Update each row with the IDF of the word
            SearchIndex.objects.filter(word=word).update(idf=idf)

            #Update each row again with the TF-IDF
            SearchIndex.objects.all().update(title_tfidf=F('title_tf') * F('idf'),
                                 body_tfidf=F('body_tf') * F('idf'),)

