from django.utils import timezone
from django.db.models import Q
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, \
    ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from blog.models import Blog, Comment
from blog.serializers import BlogSerializer, CommentSerializer
from utills.permissions import IsAuthorOrReadOnly


class BlogQuerySetMixin:
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def get_queryset(self):
        return self.queryset.filter(
            Q(published_at__isnull=True) |
            Q(published_at__gte=timezone.now())
        ).order_by('-created_at').select_related('author')


class BlogListAPIView(BlogQuerySetMixin, ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class BlogRetrieveAPIView(BlogQuerySetMixin, RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthorOrReadOnly]



class CommentListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = Comment.objects.all()
        blog = self.get_blog_object()
        return queryset.filter(blog=blog)

    def get_blog_object(self):
        return get_object_or_404(Blog, pk=self.kwargs.get('blog_pk'))

    def perform_create(self, serializer):
        blog = self.get_blog_object()
        serializer.save(author=self.request.user, blog=blog)

class CommentUpdateDestroyAPIView(UpdateAPIView, DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]






