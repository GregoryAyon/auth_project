from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.models import Group, Permission
from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from app_auth.serializers import UserSerializer, GroupSerializer, EmailSerializer, ResetPasswordSerializer
from app_auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404


class UserListCreateView(ListCreateAPIView):
    permission_classes = []
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserRetriveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'id'


class GroupListCreateView(ListCreateAPIView):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()


class GroupUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    lookup_field = 'id'


class UserGroupPermissionApi(APIView):
    def post(self, request, format=None):
        try:
            user_id = request.data.get('user_id')
            group_id = request.data.get('group_id')

            user = get_object_or_404(User, id=user_id)
            group = get_object_or_404(Group, id=group_id)

            user.groups.add(group)
            return Response({'status': 'Success!'}, status=status.HTTP_201_CREATED)
        except:
            return Response({'status': 'Error!'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        try:
            user_id = request.data.get('user_id')
            group_id = request.data.get('group_id')

            user = get_object_or_404(User, id=user_id)
            group = get_object_or_404(Group, id=group_id)

            user.groups.remove(group)
            return Response({'status': 'Detele!'}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'status': 'Error!'}, status=status.HTTP_400_BAD_REQUEST)


def test_view(request):
    per = Permission.objects.first()
    group = Group.objects.all()
    # print(per.codename)
    # print("Group: ", group)

    return render(request, 'test.html')


# --- Reset Password ---


class PasswordReset(APIView):
    serializer_class = EmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]
        user = User.objects.filter(email=email).first()
        if user:
            encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))
            token = PasswordResetTokenGenerator().make_token(user)
            reset_url = reverse(
                "app_auth:reset-password",
                kwargs={"encoded_pk": encoded_pk, "token": token},
            )
            reset_link = f"http://127.0.0.1:8000{reset_url}"

            return Response(
                {
                    "message":
                    f"Your password rest link: {reset_link}"
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"message": "User doesn't exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ResetPasswordAPI(APIView):
    serializer_class = ResetPasswordSerializer

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"kwargs": kwargs}
        )
        serializer.is_valid(raise_exception=True)
        return Response(
            {"message": "Password reset complete"},
            status=status.HTTP_200_OK,
        )
