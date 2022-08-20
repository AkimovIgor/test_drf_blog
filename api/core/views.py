from .serializers import PostSerializer
from .models import Post
from rest_framework import mixins
from rest_framework import generics


class PostList(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               generics.GenericAPIView):

    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'slug'

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
