from django.contrib.auth import get_user_model

from djoser.serializers import UserSerializer
from rest_framework import serializers


User = get_user_model()


class UserSerializer(UserSerializer):
    password = serializers.CharField(write_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'password', 'username', 'email',
                  'first_name', 'last_name', 'is_subscribed')
        read_only_fields = ('id',)

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        return (
            user.is_authenticated
            and user.subscriptions.filter(user=obj).exists()
        )
