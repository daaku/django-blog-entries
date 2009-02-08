"""
Managers for blog_entries.

"""

from comment_utils.managers import CommentedObjectManager
from django.db import models
from translatable_model import LanguageManager
import datetime


class LiveEntryManager(CommentedObjectManager, LanguageManager):
    """
    Custom manager for the Entry model, providing defaults for
    query filtering and shortcuts for featured entries.

    """
    def featured(self):
        """
        Returns a ``QuerySet`` of featured Entries.

        """
        return self.filter(featured__exact=True)

    def get_query_set(self):
        """
        Overrides the default ``QuerySet`` to only include Entries
        with a status of 'live' and a publication date in the past.
        LanguageManager adds the current language to the filter.

        """
        return (super(LiveEntryManager, self).
                get_query_set().
                filter(status__exact=self.model.LIVE_STATUS).
                filter(pub_date__lte=datetime.datetime.now).
                order_by('-pub_date'))

    def latest_featured(self):
        """
        Returns the latest featured Entry if there is one, or ``None``
        if there isn't.

        """
        try:
            return self.featured()[0]
        except IndexError:
            return None

    def _clone(self):
        """
        This is for the generic view's benefit which expects a queryset. Since
        we want to evaluate our query set at runtime to account for sites and
        languages, we provide this to make the manager emulate a queryset for
        what the object_list/object_detail views expect. Yuk.

        """
        return self.get_query_set()
