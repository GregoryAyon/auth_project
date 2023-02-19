from rest_framework import serializers
from app_auth.models import User
from django.contrib.auth.decorators import user_passes_test

from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

# --- Reset Password ---
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode


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


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields = ("email",)


class ResetPasswordSerializer(serializers.Serializer):

    password = serializers.CharField(
        write_only=True,
        min_length=1,
    )

    class Meta:
        field = ("password")

    def validate(self, data):
        password = data.get("password")
        token = self.context.get("kwargs").get("token")
        encoded_pk = self.context.get("kwargs").get("encoded_pk")

        if token is None or encoded_pk is None:
            raise serializers.ValidationError("Missing data.")

        pk = urlsafe_base64_decode(encoded_pk).decode()
        user = User.objects.get(pk=pk)
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError("The reset token is invalid")

        user.set_password(password)
        user.save()
        return data
