from django.urls import path, include
from blog.views import api_view_set_views
from rest_framework import routers

app_name = 'view_set_urls'
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users', api_view_set_views.UserViewSet, basename='user')
router.register(r'blogs', api_view_set_views.BlogViewSet, basename='blog')

urlpatterns = [
    # path('', api_views.blog_list, name='blog_list'),
    path('', include(router.urls)),
]
