from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.models import Blog
from rest_framework import status
from blog.serializers import BlogSerializer
from utills.permissions import IsAuthorOrReadOnly


class BlogListCreateAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        blog_list = Blog.objects.all().order_by('-created_at').select_related('author')
        paginater = PageNumberPagination()
        queryset = paginater.paginate_queryset(blog_list, request)
        serializer = BlogSerializer(queryset, many=True)
        return paginater.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            blog = serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogDetailAPIView(APIView):
    permission_classes = [IsAuthorOrReadOnly]
    object = None

    def get(self, request, format=None, *args, **kwargs):
        blog = self.get_object(request, *args, **kwargs)
        serializer = BlogSerializer(blog, many=False)
        return Response(serializer.data)

    def patch(self, request, format=None, *args, **kwargs):
        blog = self.get_object(request, *args, **kwargs)
        serializer = BlogSerializer(blog, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        blog = self.get_object(request, *args, **kwargs)
        blog.delete()
        return Response({
            'deleted': True,
            'pk': self.kwargs.get('pk')
        }, status.HTTP_200_OK)

    def get_object(self, request, *args, **kwargs):
        if self.object:
            return self.object
        blog_list = Blog.objects.all().select_related('author')
        pk = kwargs.get('pk', 0)

        blog = get_object_or_404(blog_list, pk=pk)
        self.object = blog
        return blog
