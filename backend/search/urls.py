from django.urls import path
from . import views


urlpatterns = [
    path('', views.SearchListView.as_view(), name='search'),
    # path('user/',views.UserListView.as_view(),name='user-search'),
]