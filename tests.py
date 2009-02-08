from blog_entries.models import Entry
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.comments.models import Comment
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.test import TestCase, Client


c = Client()

class EntryTest(TestCase):
    def setUp(self):
        self.original_filter = settings.MARKUP_FILTER
        settings.MARKUP_FILTER = (None, {}) # expect no alteration of content for tests
        self.user = user = User(username='me')
        user.save()

    def tearDown(self):
        settings.MARKUP_FILTER = self.original_filter
        self.user.delete()

    def test_zero_entries(self):
        """
        Makes sure dont fail with 0 entries.

        """

        response = c.get(reverse('blog_entries_archive_index'))
        self.failUnlessEqual(response.status_code, 200)

    def test_add_live_and_view_index(self):
        entry = Entry(
            author=self.user,
            slug='first-post',
            title='My First Post Title',
        )
        entry.save()

        response = c.get(reverse('blog_entries_archive_index'))
        self.failUnlessEqual(response.status_code, 200)
        self.failUnless("My First Post Title" in response.content)
        entry.delete()

    def test_add_live_and_view_entry(self):
        entry = Entry(
            author=self.user,
            slug='first-post',
            title='My First Post Title',
        )
        entry.save()

        response = c.get(entry.get_absolute_url())
        self.failUnlessEqual(response.status_code, 200)
        self.failUnless("My First Post Title" in response.content)
        entry.delete()

    def test_add_draft_and_view_index(self):
        entry = Entry(
            author=self.user,
            slug='first-post',
            title='My First Post Title',
            status=Entry.DRAFT_STATUS,
        )
        entry.save()

        response = c.get(reverse('blog_entries_archive_index'))
        self.failUnlessEqual(response.status_code, 200)
        self.failUnless("My First Post Title" not in response.content)
        entry.delete()

    def test_add_draft_and_view_entry(self):
        entry = Entry(
            author=self.user,
            slug='first-post',
            title='My First Post Title',
            status=Entry.DRAFT_STATUS,
        )
        entry.save()

        response = c.get(entry.get_absolute_url())
        self.failUnlessEqual(response.status_code, 404)
        self.failUnless("My First Post Title" not in response.content)
        entry.delete()

    def test_add_live_and_feed(self):
        entry = Entry(
            author=self.user,
            slug='first-post',
            title='My First Post Title',
        )
        entry.save()

        response = c.get(reverse('blog_entries_feeds', kwargs={'url': 'latest'}))
        self.failUnlessEqual(response.status_code, 200)
        self.failUnless("My First Post Title" in response.content)
        entry.delete()

    def test_add_live_tagged_and_feed(self):
        entry = Entry(
            author=self.user,
            slug='first-post',
            title='My First Post Title',
            tags='tag1',
        )
        entry.save()

        response = c.get(reverse('blog_entries_feeds', kwargs={'url': 'tag/tag1'}))
        self.failUnlessEqual(response.status_code, 200)
        self.failUnless("My First Post Title" in response.content)
        entry.delete()

    def test_add_live_and_view_entry_body(self):
        entry = Entry(
            author=self.user,
            slug='first-post',
            title='My First Post Title',
            body='iambody',
        )
        entry.save()

        response = c.get(entry.get_absolute_url())
        self.failUnlessEqual(response.status_code, 200)
        self.failUnless("iambody" in response.content)
        entry.delete()

    def test_add_live_and_view_entry_excerpt(self):
        entry = Entry(
            author=self.user,
            slug='first-post',
            title='My First Post Title',
            excerpt='iamexcerpt',
        )
        entry.save()

        response = c.get(reverse('blog_entries_archive_index'))
        self.failUnlessEqual(response.status_code, 200)
        self.failUnless("iamexcerpt" in response.content)
        entry.delete()

    def test_get_next_previous(self):
        entry1 = Entry(
            author=self.user,
            slug='first-post',
            title='My First Post title',
        )
        entry1.save()
        entry2 = Entry(
            author=self.user,
            slug='second-post',
            title='My Second Post title',
        )
        entry2.save()
        entry3 = Entry(
            author=self.user,
            slug='third-post',
            title='My Third Post title',
        )
        entry3.save()

        self.failUnlessEqual(entry1.get_next().id, entry2.id)
        self.failUnlessEqual(entry2.get_previous().id, entry1.id)
        self.failUnlessEqual(entry2.get_next().id, entry3.id)
        self.failUnlessEqual(entry3.get_previous().id, entry2.id)
        [e.delete() for e in (entry1, entry2, entry3)]

    def test_get_zero_comment_count(self):
        entry = Entry(
            author=self.user,
            slug='first-post',
            title='My First Post title',
        )
        entry.save()

        self.failUnlessEqual(entry._get_comment_count(), 0)
        entry.delete()

    def test_get_one_comment_count(self):
        entry = Entry(
            author=self.user,
            slug='first-post',
            title='My First Post title',
        )
        entry.save()

        comment = Comment(
            content_object=entry,
            site=Site.objects.get(pk=settings.SITE_ID),
            comment='iamcomment',
        )
        comment.save()

        self.failUnlessEqual(entry._get_comment_count(), 1)
        entry.delete()
        comment.delete()

    def test_featured(self):
        entry1 = Entry(
            author=self.user,
            slug='first-post',
            title='My First Post title',
            featured=False,
        )
        entry1.save()
        entry2 = Entry(
            author=self.user,
            slug='second-post',
            title='My Second Post title',
            featured=True,
        )
        entry2.save()

        featured = Entry.live.featured()
        self.failUnlessEqual(featured[0].id, entry2.id)
        entry1.delete()
        entry2.delete()

    def test_no_latest_featured(self):
        entry = Entry(
            author=self.user,
            slug='first-post',
            title='My First Post title',
            featured=False,
        )
        entry.save()

        latest_featured = Entry.live.latest_featured()
        self.failUnlessEqual(latest_featured, None)
        entry.delete()

    def test_latest_featured(self):
        entry1 = Entry(
            author=self.user,
            slug='first-post',
            title='My First Post title',
            featured=False,
        )
        entry1.save()
        entry2 = Entry(
            author=self.user,
            slug='second-post',
            title='My Second Post title',
            featured=True,
        )
        entry2.save()
        entry3 = Entry(
            author=self.user,
            slug='third-post',
            title='My Third Post title',
            featured=True,
        )
        entry3.save()

        latest_featured = Entry.live.latest_featured()
        self.failUnlessEqual(latest_featured.id, entry3.id)
        entry1.delete()
        entry2.delete()
        entry3.delete()
