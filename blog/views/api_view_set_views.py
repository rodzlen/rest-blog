import json
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.viewsets import ReadOnlyModelViewSet

from blog.models import Blog
from blog.serializers import UserSerializer, BlogSerializer

User = get_user_model()


@csrf_exempt
def blog_list(request):
    if request.method == 'GET':
        blogs = Blog.objects.all()
        data = {
            'blog_list': [{'id': blog.id, 'title': blog.title, 'content': blog.content} for blog in blogs]
        }
        return JsonResponse(data, status=200)
    else:
        body = json.loads(request.body.decode('utf-8'))
        Blog.objects.create(**body, author=User.objects.first())

        return JsonResponse({"msg": "저장성공"}, status=200)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all().order_by('-created_at')
    serializer_class = BlogSerializer

