"""
Managers for blog_entries.

"""

import datetime

from comment_utils.managers import CommentedObjectManager
from django.db import models


class LiveEntryManager(CommentedObjectManager):
    """
    Custom manager for the Entry model, providing shortcuts for
    filtering by entry status.

    """
    def featured(self):
        """
        Returns a ``QuerySet`` of featured Entries.

        """
        return self.filter(featured__exact=True)

    def get_query_set(self):
        """
        Overrides the default ``QuerySet`` to only include Entries
        with a status of 'live'.

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
