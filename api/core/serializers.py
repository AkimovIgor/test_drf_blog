from rest_framework import serializers
from .models import Post
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer
from django.contrib.auth.models import User
from taggit.models import Tag


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):

    tags = TagListSerializerField()
    author = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:

        model = Post
        fields = '__all__'
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class TagSerializer(serializers.ModelSerializer):

    class Meta:

        model = Tag
        fields = ('name',)
        lookup_field = 'name'
        extra_kwargs = {
            'url': {'lookup_field': 'name'}
        }


class ContactSerializer(serializers.Serializer):

    name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    subject = serializers.CharField()
    message = serializers.CharField(required=True)


class RegisterSerializer(serializers.ModelSerializer):

    password_confirm = serializers.CharField(write_only=True)

    class Meta:

        model = User
        fields = [
            'username',
            'password',
            'password_confirm',
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        password_confirm = validated_data['password_confirm']
        if password != password_confirm:
            raise serializers.ValidationError({'password': 'Пароли не совпадают'})
        user = User(username=username)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model = User
        fields = '__all__'
