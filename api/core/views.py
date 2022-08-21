from .serializers import PostSerializer, TagSerializer
from .models import Post
from rest_framework import mixins
from rest_framework import generics
from .permissions import AllowedMethods
from .pagination import PageNumberSetPagination
from taggit.models import Tag
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404


class PostList(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               generics.GenericAPIView):

    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    lookup_field = 'slug'
    permission_classes = [AllowedMethods]
    pagination_class = PageNumberSetPagination

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PostDetail(mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 generics.GenericAPIView):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'
    permission_classes = [AllowedMethods]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class TagDetail(mixins.ListModelMixin, generics.GenericAPIView):

    serializer_class = PostSerializer
    permission_classes = [AllowedMethods]
    pagination_class = PageNumberSetPagination

    def get_queryset(self):
        tag_slug = self.kwargs['tag_slug'].lower()
        try:
            tag = Tag.objects.get(slug=tag_slug)
        except ObjectDoesNotExist:
            raise Http404
        return Post.objects.filter(tags=tag)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class TagList(mixins.ListModelMixin, generics.GenericAPIView):

    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = [AllowedMethods]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class LastPostsList(mixins.ListModelMixin, generics.GenericAPIView):

    serializer_class = PostSerializer
    queryset = Post.objects.all().order_by('-id')[:5]
    permission_classes = [AllowedMethods]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
