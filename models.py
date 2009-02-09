'''
Models for blog_entries.

'''

from blog_entries import managers
from comment_utils.moderation import CommentModerator, moderator
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.db import models
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext_lazy as _
from tagging.fields import TagField
from template_utils.markup import formatter
from translatable_model import LanguageField
import datetime
import tagging


class Entry(models.Model):
    'An entry in the weblog.'

    LIVE_STATUS = 1
    DRAFT_STATUS = 2
    HIDDEN_STATUS = 3
    STATUS_CHOICES = (
        (LIVE_STATUS, _(u'Live')),
        (DRAFT_STATUS, _(u'Draft')),
        (HIDDEN_STATUS, _(u'Hidden')),
    )

    # Metadata.
    author = models.ForeignKey(User)
    enable_comments = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    pub_date = models.DateTimeField(_(u'Date posted'), default=datetime.datetime.today,
                                    help_text=_(u'Entries with a publication date in the future will not be visible.'))
    slug = models.SlugField(unique_for_date='pub_date',
                            help_text=_(u'Used in the URL of the entry. Must be unique for the publication date of the entry.'))
    status = models.IntegerField(choices=STATUS_CHOICES, default=LIVE_STATUS,
                                 help_text=_(u'Only entries with "live" status will be displayed publicly.'))
    title = models.CharField(max_length=250)
    language = LanguageField()
    sites = models.ManyToManyField(Site, default=[settings.SITE_ID], verbose_name=_('sites'),
                                    help_text=_('The site(s) the page is accessible at.'))

    # The actual entry bits.
    body = models.TextField(blank=True, null=True)
    body_html = models.TextField(editable=False, blank=True)
    excerpt = models.TextField(blank=True, null=True)
    excerpt_html = models.TextField(blank=True, null=True, editable=False)

    # Managers.
    live = managers.LiveEntryManager()
    unfiltered = models.Manager()

    # Categorization and SEO.
    tags = TagField()
    keywords = models.TextField(blank=True, null=True,
                                help_text=_(u'Comma separated keywords or phrases used for search engine optimization.'))
    description = models.TextField(blank=True, null=True,
                                   help_text=_(u'Brief description used for search engine optimization.'))

    class Meta:
        get_latest_by = 'pub_date'
        ordering = ['-pub_date']
        verbose_name_plural = 'Entries'

    def save(self):
        if self.body:
            self.body_html = formatter(self.body)
        if self.excerpt:
            self.excerpt_html = formatter(self.excerpt)
        super(Entry, self).save()

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
        return Comment.objects.filter(
                content_type__pk=smart_unicode(ctype.id),
                object_pk__exact=smart_unicode(self.id)).count()
    _get_comment_count.short_description = _(u'Number of comments')



BLOG_ENTRIES_COMMENTS_MODERATE_AFTER = getattr(settings, 'BLOG_ENTRIES_COMMENTS_MODERATE_AFTER', None)
class BlogEntriesModerator(CommentModerator):
    akismet = not settings.DEBUG
    auto_close_field = 'pub_date'
    email_notification = True
    enable_field = 'enable_comments'
    if BLOG_ENTRIES_COMMENTS_MODERATE_AFTER:
        close_after = BLOG_ENTRIES_COMMENTS_MODERATE_AFTER

moderator.register([Entry], BlogEntriesModerator)

tagging.register(Entry, 'tag_set')
