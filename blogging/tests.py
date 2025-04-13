from django.test import TestCase
from django.utils.timezone import make_aware, now as django_now

from datetime import datetime, timedelta
import datetime
from blogging.models import Post, Category
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory

# from blogging.views import detail_view
from django.test import TestCase
from django.utils.timezone import now as django_now
from datetime import timedelta
from blogging.models import Post, Category
from django.contrib.auth.models import User


class PostTestCase(TestCase):
    fixtures = ["blogging_test_fixture.json"]

    def setUp(self):
        # Ensure there's a user available from fixture or create one
        if not User.objects.filter(pk=1).exists():
            User.objects.create_user("testuser", "test@example.com", "password")
        self.user = User.objects.get(pk=1)

    def test_string_representation(self):
        expected = "This is a title"
        p1 = Post(title=expected, author=self.user)
        actual = str(p1)
        self.assertEqual(expected, actual)


class CategoryTestCase(TestCase):
    def test_string_representation(self):
        expected = "A Category"
        c1 = Category(name=expected)
        actual = str(c1)
        self.assertEqual(expected, actual)


class FrontEndTestCase(TestCase):
    def setUp(self):
        self.user, _ = User.objects.get_or_create(
            username="testuser", email="test@example.com", password="password"
        )
        self.now = django_now()

        for count in range(1, 5):  # Example with 4 posts for simplicity
            post = Post(
                title=f"Post {count} Title",
                text="Text for post {count}",
                author=self.user,
            )
            if count % 2 == 0:
                post.published_date = self.now - timedelta(
                    days=365
                )  # Clearly in the past
            post.save()
            # Immediately fetch and print to verify
            saved_post = Post.objects.get(pk=post.pk)
            print(
                f"Post ID: {saved_post.pk}, Set Date: {post.published_date}, Saved Date: {saved_post.published_date}"
            )

    def test_details_only_published(self):
        for post in Post.objects.all():
            response = self.client.get(f"/posts/{post.pk}/")
            print(f"Testing post {post.pk}, Published Date: {post.published_date}")
            if post.published_date:
                self.assertEqual(
                    response.status_code,
                    200,
                    f"Expected 200 for post {post.pk}, got {response.status_code}",
                )
            else:
                self.assertEqual(
                    response.status_code,
                    404,
                    f"Expected 404 for post {post.pk}, got {response.status_code}",
                )
