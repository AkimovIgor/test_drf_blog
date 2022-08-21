from .serializers import PostSerializer, TagSerializer, ContactSerializer
from .models import Post
from rest_framework import mixins
from rest_framework import generics
from rest_framework import filters
from rest_framework.response import Response
from .permissions import AllowedMethods
from .pagination import PageNumberSetPagination
from taggit.models import Tag
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404
from django.core.mail import send_mail
from django.conf import settings


class PostList(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               generics.GenericAPIView):

    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    lookup_field = 'slug'
    permission_classes = [AllowedMethods]
    pagination_class = PageNumberSetPagination
    search_fields = ['content', 'header']
    filter_backends = (filters.SearchFilter,)

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


class FeedBack(mixins.CreateModelMixin, generics.GenericAPIView):

    serializer_class = ContactSerializer
    permission_classes = [AllowedMethods]

    def post(self, request, *args, **kwargs):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            name = data.get('name')
            email = data.get('email')
            subject = data.get('subject')
            message = data.get('message')
            send_mail(f'От {name} | {subject}', message, email, [
                settings.EMAIL_HOST_USER
            ])
            response_data = {'success': 'Sent'}
        else:
            response_data = {'success': 'False', 'errors': serializer.errors}
        return Response(response_data)
