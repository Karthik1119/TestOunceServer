from .models import Asset
from rest_framework import serializers

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id","file","file_xxl","file_xl","file_l","icon")