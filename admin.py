"""
Admin for blog_entries.

"""

from blog_entries.models import Entry
from django.conf import settings
from django.contrib import admin
from django.core.urlresolvers import get_callable


class EntryAdmin(admin.ModelAdmin):
    "Options for the Entry Admin interface."

    prepopulated_fields = {
        'slug': ('title',),
    }
    date_hierarchy = 'pub_date'
    fieldsets = (
        ('Metadata',
            {'fields': ('title', 'slug', 'pub_date', 'author', 'status', 'featured', 'enable_comments', 'sites', 'language')}),
        ('Entry',
            {'fields': ('excerpt', 'body')}),
        ('Categorization and SEO',
            {'fields': ('tags', 'keywords', 'description')}),
    )
    list_display = ('title', 'pub_date', 'author', 'status', 'enable_comments', '_get_comment_count')
    list_filter = ('status',)
    search_fields = ('excerpt', 'body', 'title')
    model_admin_manager = Entry.unfiltered

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'body' or db_field.name == 'excerpt':
            setting_name = 'BLOG_ENTRIES_%s_WIDGET' % db_field.name.upper()
            widget = getattr(settings, setting_name, None)
            if widget:
                c, k = widget
                kwargs['widget'] = get_callable(c)(**k)
        return super(EntryAdmin, self).formfield_for_dbfield(db_field, **kwargs)

site = admin.site
site.register(Entry, EntryAdmin)
