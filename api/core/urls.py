from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import PostList


urlpatterns = [
    path('posts', PostList.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
