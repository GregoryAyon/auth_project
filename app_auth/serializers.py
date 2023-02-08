from rest_framework import serializers
from app_auth.models import User
from django.contrib.auth.decorators import user_passes_test

from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = [
        #     "id",
        #     "username",
        #     "first_name",
        #     "last_name",
        #     'full_name',
        #     "phone",
        #     "password",
        #     'is_Active',
        #     'is_Active',
        #     'date_joined'
        # ]
        fields = '__all__'
        extra_kwargs = {
            "password": {
                "write_only": True,
            },
        }

    def create(self, validated_data):

        return User.objects.create_user(**validated_data)


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'
