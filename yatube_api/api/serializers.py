from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Follow, Group, Post, User


class BaseAuthorSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )


class PostSerializer(BaseAuthorSerializer):

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(BaseAuthorSerializer):
    post = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = '__all__'
        validators = (
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following',),
                message="Вы уже подписаны на этого пользователя"
            ),
        )

    def validate(self, data):
        request_user = self.context['request'].user
        following_user = data['following']
        if request_user == following_user:
            raise serializers.ValidationError('Нельзя подписаться на себя')
        return data
