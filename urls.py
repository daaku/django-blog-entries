"""
URLs for blog_entries.

"""

from blog_entries.feeds import LatestEntries, LatestEntriesByTag
from blog_entries.models import Entry
from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic import date_based, list_detail


PAGINATE_BY = getattr(settings, 'BLOG_ENTRIES_PAGINATE_BY', 15)

queryset = Entry.live
if hasattr(settings, 'BLOG_ENTRIES_QUERYSET'):
    queryset = settings.BLOG_ENTRIES_QUERYSET(queryset)

entry_info_dict = {
    'queryset': queryset,
    'date_field': 'pub_date',
    'template_name': 'blog_entries/entry_list.html',
}
list_page_dict = {
    'queryset': queryset,
    'paginate_by': PAGINATE_BY,
}
tagged_info_dict = {
    'queryset_or_model': queryset,
    'template_name': 'blog_entries/tagged.html',
    'paginate_by': PAGINATE_BY,
}
feeds = {
    'latest': LatestEntries,
    'tag': LatestEntriesByTag,
}

urlpatterns = patterns('',
                       url(r'^$',
                           list_detail.object_list,
                           list_page_dict,
                           name='blog_entries_archive_index'),
                       url(r'^(?P<year>\d{4})/$',
                           date_based.archive_year,
                           dict(entry_info_dict, make_object_list=True),
                           name='blog_entries_archive_year'),
                       url(r'^(?P<year>\d{4})/(?P<month>\w{3})/$',
                           date_based.archive_month,
                           entry_info_dict,
                           name='blog_entries_archive_month'),
                       url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/$',
                           date_based.archive_day,
                           entry_info_dict,
                           name='blog_entries_archive_day'),
                       url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
                           date_based.object_detail,
                           {'queryset': queryset, 'date_field': 'pub_date', 'slug_field': 'slug'},
                           name='blog_entries_detail'),
                       url(r'^tag/(?P<tag>.*)/$',
                           'tagging.views.tagged_object_list',
                           tagged_info_dict,
                           name='blog_entries_tagged'),
                        url(r'^feeds/(?P<url>.*)/$',
                            'django.contrib.syndication.views.feed',
                            {'feed_dict': feeds},
                            name='blog_entries_feeds'),
                       )
