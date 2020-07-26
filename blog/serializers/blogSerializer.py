from rest_framework import serializers
from .likeUserSerializer import LikedUserSerializer
from Common.serializer import AssetSerializer

class BlogSerializer(serializers.ModelSerializer):
    likes = LikedUserSerializer(many=True)
    images = AssetSerializer

    class Meta:
        fields = ("id","title","description","images","likes")