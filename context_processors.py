"""
A context processor which adds the value of the
``COMMENTS_MODERATE_AFTER`` setting to each ``RequestContext`` in
which it is applied.

"""

from template_utils.context_processors import settings_processor


comment_moderation = settings_processor('COMMENTS_MODERATE_AFTER')
