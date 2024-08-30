from rest_framework import serializers

from webapp.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "image", "content", "author", "like_users", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at", "like_users", "author"]
