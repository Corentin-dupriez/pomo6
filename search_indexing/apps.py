from django.apps import AppConfig


class SearchIndexingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'search_indexing'

    def ready(self):
        import search_indexing.signals
