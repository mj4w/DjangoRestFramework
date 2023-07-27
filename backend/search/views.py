
from rest_framework import generics
from product.models import Product
from product.serializers import ProductSerializer
from api.serializers import UserPublicSerializer
from rest_framework.response import Response
from . import client


#this search is from algolia search engine
class SearchListView(generics.GenericAPIView):
    def get(self, request, *args,**kwargs):
        user = None

        #request.user is perform search individually by a user 
        if request.user.is_authenticated:
            user = request.user.username

        query = request.GET.get('q')
        public = str(request.GET.get('public')) != "0"
        tag = request.GET.get('tag') or None
        # print(user,query,public,tag)
        if not query:
            return Response('',status=400)
        results = client.perform_search(query,tags=tag,user=user, public=public)
        return Response(results)



# class SearchListView(generics.ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer


#     def get_queryset(self,*args,**kwargs):
#         qs = super().get_queryset(*args,**kwargs)
#         q = self.request.GET.get('q')
#         results = Product.objects.none()
#         if q is not None:
#             user = None
#             if self.request.user.is_authenticated:
#                 user = self.request.user
#             results = qs.search(q, user=user)
#         return results
    

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
    
    