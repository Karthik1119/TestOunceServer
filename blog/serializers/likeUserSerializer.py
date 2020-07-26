from rest_framework import serializers
from CustomAuth.models import User


class LikedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id","first_name")