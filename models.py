'''
Models for blog_entries.

'''


import datetime

from comment_utils.moderation import CommentModerator, moderator
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.comments import models as comment_models
import tagging
from tagging.fields import TagField

from blog_entries import managers

class Entry(models.Model):
    'An entry in the weblog.'

    LIVE_STATUS = 1
    DRAFT_STATUS = 2
    HIDDEN_STATUS = 3
    STATUS_CHOICES = (
        (LIVE_STATUS, 'Live'),
        (DRAFT_STATUS, 'Draft'),
        (HIDDEN_STATUS, 'Hidden'),
    )

    # Metadata.
    author = models.ForeignKey(User)
    enable_comments = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    pub_date = models.DateTimeField(u'Date posted', default=datetime.datetime.today)
    slug = models.SlugField(unique_for_date='pub_date',
                            help_text=u'Used in the URL of the entry. Must be unique for the publication date of the entry.')
    status = models.IntegerField(choices=STATUS_CHOICES, default=LIVE_STATUS,
                                 help_text=u'Only entries with "live" status will be displayed publicly.')
    title = models.CharField(max_length=250)

    # The actual entry bits.
    body = models.TextField(blank=True, null=True)
    excerpt = models.TextField(blank=True, null=True)

    # Managers.
    objects = models.Manager()
    live = managers.LiveEntryManager()

    # Categorization and SEO.
    tags = TagField()
    keywords = models.TextField(blank=True, null=True,
                                help_text=u'Comma separated keywords or phrases used for search engine optimization.')
    description = models.TextField(blank=True, null=True,
                                   help_text=u'Brief description used for search engine optimization.')

    class Meta:
        get_latest_by = 'pub_date'
        ordering = ['-pub_date']
        verbose_name_plural = 'Entries'

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('blog_entries_detail', (), { 'year': self.pub_date.strftime('%Y'),
                                               'month': self.pub_date.strftime('%b').lower(),
                                               'day': self.pub_date.strftime('%d'),
                                               'slug': self.slug })

    def _next_previous_helper(self, direction):
        return getattr(self, 'get_%s_by_pub_date' % direction)(status__exact=self.LIVE_STATUS)

    def get_next(self):
        """
        Returns the next Entry with "live" status by ``pub_date``, if
        there is one, or ``None`` if there isn't.

        """
        return self._next_previous_helper('next')

    def get_previous(self):
        """
        Returns the previous Entry with "live" status by ``pub_date``,
        if there is one, or ``None`` if there isn't.

        """
        return self._next_previous_helper('previous')

    def _get_comment_count(self):
        ctype = ContentType.objects.get_for_model(self)
        return comment_models.Comment.objects.filter(content_type__pk=ctype.id, object_pk__exact=self.id).count()
    _get_comment_count.short_description = 'Number of comments'




class BlogEntriesModerator(CommentModerator):
    akismet = True
    auto_close_field = 'pub_date'
    email_notification = True
    enable_field = 'enable_comments'
    close_after = settings.COMMENTS_MODERATE_AFTER

moderator.register([Entry], BlogEntriesModerator)

tagging.register(Entry, 'tag_set')
