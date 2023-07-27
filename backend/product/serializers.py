from rest_framework import serializers
from  .models import Product
from rest_framework.reverse import reverse
from .validators import validate_title_no_hello,unique_product_title
from api.serializers import UserPublicSerializer

class ProductSerializer(serializers.ModelSerializer):
    owner = UserPublicSerializer(source='user',read_only=True)
    edit_url = serializers.SerializerMethodField(read_only=True)
    detail_url = serializers.SerializerMethodField(read_only=True)
    delete_url = serializers.SerializerMethodField(read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='product-detail',lookup_field='pk')
    #for validation
    title = serializers.CharField(validators=[validate_title_no_hello,unique_product_title])
    # source function make replace what you put inside 
    # name = serializers.CharField(source='title',read_only=True) 

    # email = serializers.EmailField(write_only=True)
    class Meta:
        model = Product
        fields = ['owner',
                  'id',
                  'url',
                  'detail_url',
                  'edit_url',
                  'delete_url',
                  'title',
                  'content',
                  'price',
                  'sale_price',
                  'public',
                  'path',
                ]



    def get_my_user_data(self,obj):
        return{
            "username":obj.user.username

        }
    # def create(self,validated_data):
    #     # return Product.objects.create(**validated_data)
    #     # email = validated_data.pop('email')
    #     obj = super().create(validated_data)
    #     # print(email,obj)
    #     return obj
    
    # def update(self,instance,validated_data):
    #     email = validated_data.pop('email')
    #     instance.title = validated_data.get('title')
    #     return super().update(instance,validated_data)



    
    def get_edit_url(self,obj):
        # return f"/api/products/{obj.pk}/"
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("product-edit", kwargs={"pk":obj.pk}, request=request)
    
    def get_detail_url(self,obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("product-detail",kwargs={"pk":obj.pk},request=request)
    
    def get_delete_url(self,obj):
        if not isinstance(obj,Product):
            return None
        request = self.context.get('request')
        if request is None:
            return None
        
        return reverse("product-delete",kwargs={"pk":obj.pk},request=request)

