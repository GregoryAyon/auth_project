from django.contrib.auth.models import Group, Permission
from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from app_auth.serializers import UserSerializer, GroupSerializer
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
    print("Group: ", group)

    return render(request, 'test.html')
