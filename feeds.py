# coding: utf-8
from django.conf import settings
from django.contrib.syndication.feeds import Feed
from tagging.utils import parse_tag_input, get_tag
from tagging.models import TaggedItem

from blog_entries.models import Entry


feed_title = settings.BLOG_ENTRIES_FEED_TITLE or ''

class EntriesFeed(Feed):
    title_template = 'blog_entries/feeds_title.html'
    description_template = 'blog_entries/feeds_description.html'

    def item_pubdate(self, item):
        return item.pub_date

    def item_categories(self, item):
        return parse_tag_input(item.tags)

class LatestEntries(EntriesFeed):
    title = feed_title
    link = '/'
    description = 'New posts on ' + feed_title

    def items(self):
        return Entry.live.order_by('-pub_date')[:10]

class LatestEntriesByTag(EntriesFeed):
    link = '/'
    description = 'New posts on ' + feed_title

    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return bits[0]

    def title(self, tag):
        return tag + u' — ' + feed_title

    def link(self, tag):
        return '/tag/' + tag

    def items(self, tag):
        return TaggedItem.objects.get_by_model(Entry, get_tag(tag)).order_by('-pub_date')[:10]
