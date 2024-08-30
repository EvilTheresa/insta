from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from api_v1.views import PostViewSet, LogoutView

app_name = 'api_v1'

router = routers.DefaultRouter()
router.register('posts', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', obtain_auth_token, name='api_token_auth'),
    path('logout/', LogoutView.as_view(), name='api_token_delete'),
    # path('posts/<int:post_id>/like/', like_post, name='like_post'),
    # path('posts/<int:post_id>/unlike/', unlike_post, name='unlike_post'),
]