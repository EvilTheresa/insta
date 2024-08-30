from rest_framework import status, permissions
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from api_v1.permissions import IsAuthenticatedToEdit, IsAuthorOrReadOnly
from api_v1.serializers.post import PostSerializer
from webapp.models import Post


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permissions = [IsAuthenticatedToEdit, IsAuthorOrReadOnly]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        elif self.action in ['like', 'unlike', 'create']:
            permission_classes = [IsAuthenticatedToEdit]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthorOrReadOnly]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=['POST'], detail=True, url_path='like')
    def like_post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if request.user not in post.like_users.all():
            post.like_users.add(request.user)
            return Response({'status': 'like added'}, status=status.HTTP_201_CREATED)
        return Response({'status': 'like already exists'}, status=status.HTTP_418_IM_A_TEAPOT)

    @action(methods=['POST'], detail=True, url_path='unlike')
    def unlike_post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if request.user in post.like_users.all():
            post.like_users.remove(request.user)
            return Response({'status': 'like removed'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'status': 'user did not like'}, status=status.HTTP_404_NOT_FOUND)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        user.auth_token.delete()
        return Response({'status': 'ok'})
