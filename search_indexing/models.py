from django.db import models

class SearchIndex(models.Model):
    word = models.CharField(max_length=100)
    advert = models.ForeignKey(to='adverts.Advertisement',
                               on_delete=models.CASCADE)
    title_tf = models.FloatField()
    body_tf = models.FloatField()
    idf = models.FloatField(null=True,
                                    blank=True)
    title_tfidf = models.FloatField(null=True,
                                    blank=True)
    body_tfidf = models.FloatField(null=True,
                                   blank=True)
