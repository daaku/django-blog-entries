from django.contrib.sitemaps import GenericSitemap
from blog_entries.models import Entry

info_dict = {
    'queryset': Entry.live.all(),
    'date_field': 'pub_date',
}
BlogEntriesSitemap = GenericSitemap(info_dict, priority=1)
