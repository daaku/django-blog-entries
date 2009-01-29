"""
Admin for blog_entries.

"""

from django.conf import settings
from django.contrib import admin
from blog_entries.models import Entry

class EntryAdmin(admin.ModelAdmin):
    "Options for the Entry Admin interface."

    change_form_template = 'blog_entries/change_form_' + getattr(settings, 'BLOG_ENTRIES_EDITOR', 'wmd') + '.html'

    prepopulated_fields = {
        'slug':        ('title',),
    }
    date_hierarchy = 'pub_date'
    fieldsets = (
        ('Metadata',
            {'fields': ('title', 'slug', 'pub_date', 'author', 'status', 'featured', 'enable_comments')}),
        ('Entry',
            {'fields': ('excerpt', 'body')}),
        ('Categorization and SEO',
            {'fields': ('tags', 'keywords', 'description')}),
    )
    list_display = ('title', 'pub_date', 'author', 'status', 'enable_comments', '_get_comment_count')
    list_filter = ('status',)
    search_fields = ('excerpt', 'body', 'title')
    model_admin_manager = Entry.unfiltered

site = admin.site
site.register(Entry, EntryAdmin)
