import re

from django.contrib.auth import get_user_model
from rest_framework import serializers
from djoser.serializers import UserSerializer
from .models import Follow
User = get_user_model()


class UserSerializer(UserSerializer):
    pass
    password = serializers.CharField(write_only=True)
    is_subscribed = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('id', 'password', 'username', 'email',
            'first_name', 'last_name', 'is_subscribed')
        read_only_fields = ('id',)

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user == obj:
            return False
        return True        
    
    # def create(self, validated_data):
    #     user = User.objects.create_user(
    #         username=validated_data['username'],
    #         password=validated_data['password'],
    #         email=validated_data['email'],
    #         first_name=validated_data['first_name'],
    #         last_name=validated_data['last_name'],
    #     )
    #     return user
    
    
    # def validate_username(self, value):
    #     if value.lower() == "me":
    #         raise serializers.ValidationError(
    #             "Имя 'me' использовать запрещено.")

    #     if not re.match(r'^[\w.@+-]+\Z', value):
    #         raise serializers.ValidationError(
    #             "Неправильный формат имени пользователя.")

    #     return value