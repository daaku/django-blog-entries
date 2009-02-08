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


  [1]: http://github.com/django/django/tree
  [2]: http://github.com/nshah/django-admin-manager-monkey/tree
  [3]: http://github.com/nshah/django-comment-utils/tree
  [4]: http://github.com/nshah/django-tagging/tree
  [5]: http://github.com/nshah/django-template-utils/tree
  [6]: http://github.com/nshah/django-translatable-model/tree
