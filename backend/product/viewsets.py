from rest_framework import viewsets,mixins
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    '''
    get -> list -> Queryset
    get -> retrieve -> Product Instant Detail View
    post -> create -> New Instance
    put -> Update
    patch -> Partial Update
    delete -> destroy
    '''
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "pk" #default


class ProductGenericViewSet(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.RetrieveModelMixin):
    '''
    get -> list -> Queryset
    get -> retrieve -> Product Instant Detail Viewz
    '''
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "pk" #default
