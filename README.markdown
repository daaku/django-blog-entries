Blog Entries
============

A generic Blog application with too many features:


Features
--------

  - Live/Draft/Hidden Entries
  - Uses Generic List and Date views
  - Future Entries are hidden until the date arrives
  - Uses comment-utils for Moderation/Akismet integration
  - Uses django-tagging
  - Uses django-translatable-model for Language specific Models
  - Uses django.contrib.sitemaps
  - Uses django.contrib.sites
  - Uses django.contrib.syndication.feeds for latest/tag based feeds
  - Uses django.utils.translation
  - Uses template-utils for formatting support


Dependencies
------------

  - [django (trunk)][1]
  - [django-admin-manager-monkey][2] - to allow specifying the manager for
    admin
  - [django-comment-utils][3]
  - [django-tagging][4]
  - [django-template-utils][5]
  - [django-translatable-model][6]

Optional
--------

  - [django-rte-widgets][7]


Settings
--------

### `BLOG_ENTRIES_FEED_TITLE`

The title for use with feeds.

### `BLOG_ENTRIES_BODY_WIDGET`

*Optional*. Can be used to specify a Widget for the Body field in the Admin
interface. [django-rte-widgets][7] provides some widgets which can be used
here. For example:

    BLOG_ENTRIES_BODY_WIDGET = ('rte_widgets.yui.YuiTextarea', {'config': {'height': '400px', 'width': '700px', 'format': 'xhtml'}})

The setting must be a tuple of two elements, where the first is a resolved to a
callable using django's `get_callable` and the second is a dict which will be
passed to the callable as keyword arguments. This works with standard Widget
classes.

### `BLOG_ENTRIES_EXCERPT_WIDGET`

*Optional*. Can be used to specify a Widget for the Excerpt field in the Admin
interface.

### `BLOG_ENTRIES_PAGINATE_BY`

The number of items to show per page. *Defaults to **15***.

### `BLOG_ENTRIES_COMMENTS_MODERATE_AFTER`

*Optional*. The number of days after which comments will be closed on an Entry.
The default is None which means never.



  [1]: http://github.com/django/django/tree
  [2]: http://github.com/nshah/django-admin-manager-monkey/tree
  [3]: http://github.com/nshah/django-comment-utils/tree
  [4]: http://github.com/nshah/django-tagging/tree
  [5]: http://github.com/nshah/django-template-utils/tree
  [6]: http://github.com/nshah/django-translatable-model/tree
  [7]: http://github.com/nshah/django-rte-widgets/tree
