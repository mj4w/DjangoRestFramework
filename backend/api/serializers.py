from rest_framework import serializers

#THE COMMENT REFER TO A OTHER PRODUCTS, LIKE IN THE ECOMMERCE WEBSITE THEY HAVE A LIST OF RECOMMENDED PRODUCTS IF YOU SEE THE PRODUCT DETAIL

# class UserProductInlineSerializer(serializers.Serializer):
#     url = serializers.HyperlinkedIdentityField(view_name='product-detail',lookup_field='pk',read_only=True)
#     title = serializers.CharField(read_only=True)






#serializers.Serializer Prefer from the USER DATA
class UserPublicSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only =True)
    email = serializers.EmailField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    # other_products = serializers.SerializerMethodField(read_only=True)

    # def get_other_products(self,obj):
    #     request = self.context.get('request')
    #     print(obj)
    #     user = obj
    #     my_products_qs = user.product_set.all()[:5]
    #     return UserProductInlineSerializer(my_products_qs, many=True, context=self.context).data


