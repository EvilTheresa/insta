from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from ..models import Post, PostLike


@method_decorator(csrf_exempt, name='dispatch')
class PostLikeToggle(View):
    def post(self, request, post_id):
        post = Post.objects.get(id=post_id)
        like, created = PostLike.objects.get_or_create(user=request.user, post=post)

        if not created:
            like.delete()
            liked = False
        else:
            liked = True

        return JsonResponse({'likes_count': post.count_likes(), 'liked': liked})
