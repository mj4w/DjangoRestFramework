from django.shortcuts import render
from rest_framework import generics
from product.models import Product
from product.serializers import ProductSerializer
from django.contrib.auth.models import User
from api.serializers import UserPublicSerializer
from django.contrib.auth import get_user_model
# Create your views here.
User = get_user_model()

class SearchListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


    def get_queryset(self,*args,**kwargs):
        qs = super().get_queryset(*args,**kwargs)
        q = self.request.GET.get('q')
        results = Product.objects.none()
        if q is not None:
            user = None
            if self.request.user.is_authenticated:
                user = self.request.user
            results = qs.search(q, user=user)
        return results
    

# class UserListView(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserPublicSerializer

#     def get_queryset(self,*args,**kwargs):
#         qs = super().get_queryset(*args,**kwargs)
#         q = self.request.GET.get('q')
#         results_user = User.objects.none()
#         if q is not None:
#             user = None
#             if self.request.user.is_authenticated:
#                 user = self.request.user
#             results_user = qs.search(q,user=user)
#         return results_user
    
    