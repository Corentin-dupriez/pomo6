from django.core.management import BaseCommand
from search_indexing.utils import index_ad, calculate_tf_idf
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
        calculate_tf_idf()

