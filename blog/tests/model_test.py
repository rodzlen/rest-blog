from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone

from django.test import TestCase
from blog.models import Blog

User = get_user_model()
class BlogModelTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='테스트', is_active=True)
        Blog.objects.create(title='제목', content='본문', author=user)
        future_published_at = timezone.now() + timedelta(days=30)

        Blog.objects.create(title='배포전',
                            content='본문2',
                            author=user,
                            published_at=future_published_at)

    def test_blog_is_published(self):
        published_blog = Blog.objects.get(title='제목')
        un_published_blog = Blog.all_objects.get(title='배포전')

        self.assertEqual(published_blog.is_active, True)
        self.assertEqual(un_published_blog.is_active, False)

    def test_blog_manager(self):
        objects_count = Blog.objects.count()
        all_objects_count = Blog.all_objects.count()
        self.assertEqual(objects_count, 1)
        self.assertEqual(all_objects_count, 2)

