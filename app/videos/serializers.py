from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Video
from users.serializers import UserInfoSerializer
from comments.serializers import CommentSerializer
from reactions.models import Reaction


class VideoListSerializer(ModelSerializer):
    user = UserInfoSerializer(read_only = True)

    class Meta:
        model = Video
        fields = '__all__'
        # depth = 1

# 댓글 정보가 추가됨
class VideoDetailSerializer(ModelSerializer):
    user = UserInfoSerializer(read_only = True)

    comment_set = CommentSerializer(many = True, read_only = True)

    reactions = serializers.SerializerMethodField()
    class Meta:
        model = Video
        fields = '__all__'

    def get_reactions(self, video):
        return Reaction.get_video_reactions(video)