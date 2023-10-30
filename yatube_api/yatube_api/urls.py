from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework import routers

from api.views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')
router.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)
router.register(r'groups', GroupViewSet, basename='group')
router.register(r'follow', FollowViewSet, basename='follow')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/', include('djoser.urls')),
    path('api/v1/', include('djoser.urls.jwt')),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]
