from django.contrib.auth.models import Group, Permission
from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from app_auth.serializers import UserSerializer, GroupSerializer
from app_auth.models import User


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


def test_view(request):
    per = Permission.objects.first()
    group = Group.objects.all()
    # print(per.codename)
    print("Group: ", group)

    return render(request, 'test.html')
