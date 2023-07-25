from rest_framework import generics,mixins
from .models import Product
from .serializers import ProductSerializer
from api.permissions import IsStaffEditorPermission
from rest_framework.decorators import api_view
from rest_framework.response import Response
#from django.http import Http404
from django.shortcuts import get_object_or_404
from api.mixins import StaffEditorPermissionMixin, UserQuerySetMixin
#Retrieve products for example api/products/1 
class ProductDetailAPIView(StaffEditorPermissionMixin,UserQuerySetMixin,generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    #lookup_field = "pk"
    
product_detail_view = ProductDetailAPIView.as_view()

#create a products api 
class ProductListCreateAPIView(StaffEditorPermissionMixin,UserQuerySetMixin,generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    #the IsAuthenticated you can't see the list but in OrReadOnly you see the list 
    # permission_classes = [permissions.IsAdminUser,IsStaffEditorPermission]

    def perform_create(self,serializer):
        #serializer.save(user=self.request.user)
        # print(serializer)
        # email = serializer.validated_data.pop('email')
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = title
        serializer.save(user=self.request.user,content=content) #form.save() model.save()

    # def get_queryset(self, *args, **kwargs):
    #     qs = super().get_queryset(*args,**kwargs)
    #     request = self.request
    #     user = request.user
    #     if not user.is_authenticated:
    #         return Product.objects.none()
    #     return qs.filter(user=request.user)
    


product_list_create_view = ProductListCreateAPIView.as_view()

#to update products 
class ProductUpdateAPIView(StaffEditorPermissionMixin,UserQuerySetMixin,generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "pk"
    # permission_classes = [permissions.IsAdminUser,IsStaffEditorPermission]
    
    def perform_update(self,serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title
            ##
product_update_view = ProductUpdateAPIView.as_view()


#to delete products 
class ProductDeleteAPIView(StaffEditorPermissionMixin,generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "pk"
    # permission_classes = [permissions.IsAdminUser,IsStaffEditorPermission]
    
    def perform_destroy(self,instance):
        #instance
        super().perform_destroy(instance)

product_delete_view = ProductDeleteAPIView.as_view()



# class ProductListAPIView(generics.ListAPIView):
#     '''
#     Not gonna use this method
#     '''
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

# product_list_view = ProductListAPIView.as_view()



class ProductMixinView(mixins.ListModelMixin,generics.GenericAPIView,mixins.RetrieveModelMixin,mixins.CreateModelMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def get(self,request,*args,**kwargs):
        pk = kwargs.get("pk")
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request,*args,**kwargs)
    
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)
      

product_mixin_view = ProductMixinView.as_view()

@api_view(['GET','POST'])
def product_alt_view(request,pk=None, *args,**kwargs):
    method = request.method #Put -> update #Destroy

    if method == 'GET':
        if pk is not None:
            #detail view
            obj = get_object_or_404(Product, pk=pk) #Http 404
            data = ProductSerializer(obj, many=False).data
            return Response(data)
        #list view
        queryset = Product.objects.all()
        data = ProductSerializer(queryset, many=True).data
        return Response(data)
    

    if method == 'POST':
        #create an item
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            title = serializer.validated_data.get('title')
            content = serializer.validated_data.get('content') or None
            if content is None:
                content = title
            serializer.save(content=content)
            return Response(serializer.data)
        return Response({'invalid':'not good data'}, status=200)