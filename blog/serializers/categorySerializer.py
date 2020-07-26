from rest_framework import serializers
from Common.serializer import AssetSerializer
from blog.models import Category

class CategorySerializer(serializers.ModelSerializer):
    image = AssetSerializer(many=False)
    class Meta:
        fields = ("id","title","image")
        model = Category