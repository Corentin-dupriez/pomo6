from django.contrib import admin

from search_indexing.models import SearchIndex


# Register your models here.
@admin.register(SearchIndex)
class SearchIndexAdmin(admin.ModelAdmin):
    pass