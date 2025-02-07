from django.contrib.auth import get_user_model
from django.db import models

from utills.models import TimeStampModel

User = get_user_model()
class Blog(TimeStampModel):
    title = models.CharField('제목', max_length=100)
    content = models.TextField('내용')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    published_at = models.DateTimeField('배포일시', null=True)

    class Meta:
        verbose_name ='블로그'
        verbose_name_plural = '블로그 목록'
        ordering = ['-created_at', '-id']
