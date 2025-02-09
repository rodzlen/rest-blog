from django.contrib.auth import get_user_model
from django.db.models import Manager, Q
from django.utils import timezone
from django.db import models

from utills.models import TimeStampModel

class PublishedManager(Manager):
    def get_queryset(self):
        now = timezone.now()
        return super().get_queryset().filter(
            Q(published_at__isnull=True) |
            Q(published_at__lte=now)
        )

User = get_user_model()
class Blog(TimeStampModel):
    title = models.CharField('제목', max_length=100)
    content = models.TextField('내용')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    published_at = models.DateTimeField('배포일시', null=True, blank=True)

    objects = PublishedManager()
    all_objects = Manager()

    @property
    def is_active(self):
        now = timezone.now()
        if not self.published_at:
            return True
        return self.published_at <= now

    class Meta:
        verbose_name ='블로그'
        verbose_name_plural = '블로그 목록'
        ordering = ['-created_at', '-id']

class Comment(TimeStampModel):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField('댓글 내용')

    class Meta:
        verbose_name = '댓글'
        verbose_name_plural = '댓글 목록'
        ordering = ('-created_at','-id')