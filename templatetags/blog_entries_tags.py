from django import template
from template_utils.templatetags.generic_content import GenericContentNode


register = template.Library()


class LatestFeaturedNode(GenericContentNode):
    def _get_query_set(self):
        return self.queryset.filter(featured__exact=True)


def do_featured_entries(parser, token):
    """
    Retrieves the latest ``num`` featured entries and stores them in a
    specified context variable.

    Syntax::

        {% get_featured_entries [num] as [varname] %}

    Example::

        {% get_featured_entries 5 as featured_entries %}

    """
    bits = token.contents.split()
    if len(bits) != 4:
        raise template.TemplateSyntaxError("'%s' tag takes three arguments" % bits[0])
    if bits[2] != 'as':
        raise template.TemplateSyntaxError("second argument to '%s' tag must be 'as'" % bits[0])
    return LatestFeaturedNode('blog_entries.entry', bits[1], bits[3])

def do_featured_entry(parser, token):
    """
    Retrieves the latest featured Entry and stores it in a specified
    context variable.

    Syntax::

        {% get_featured_entry as [varname] %}

    Example::

        {% get_featured_entry as featured_entry %}

    """
    bits = token.contents.split()
    if len(bits) != 3:
        raise template.TemplateSyntaxError("'%s' tag takes two arguments" % bits[0])
    if bits[1] != 'as':
        raise template.TemplateSyntaxError("first argument to '%s' tag must be 'as'" % bits[0])
    return LatestFeaturedNode('blog_entries.entry', 1, bits[2])

register.tag('get_featured_entries', do_featured_entries)
register.tag('get_featured_entry', do_featured_entry)
