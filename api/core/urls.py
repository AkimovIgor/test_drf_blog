from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *


urlpatterns = [
    path('posts', PostList.as_view()),
    path('posts/<slug:slug>', PostDetail.as_view()),
    path('tags', TagList.as_view()),
    path('tags/<slug:tag_slug>', TagDetail.as_view()),
    path('last_posts', LastPostsList.as_view()),
    path('feedback', FeedBack.as_view()),
    path('register', Register.as_view()),
    path('profile', Profile.as_view()),
    path('comments', CommentSent.as_view()),
    path('comments/<slug:post_slug>', CommentList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
