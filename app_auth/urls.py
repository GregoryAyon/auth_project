from django.urls import path
from app_auth.views import UserListCreateView, UserRetriveUpdateDeleteView, GroupListCreateView, GroupUpdateDeleteView, test_view

app_name = 'app_auth'

urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='users_list_create'),
    path('users/<int:pk>/', UserRetriveUpdateDeleteView.as_view(),
         name='users_retrive_update_delete'),

    path('group-list-create/', GroupListCreateView.as_view(),
         name='group_list_create'),
    path('group-update-delete/<int:id>',
         GroupUpdateDeleteView.as_view(), name='group_update_delete'),

    path('test/', test_view),
]
