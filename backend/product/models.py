from django.db import models
from django.conf import settings
from django.db.models.query import QuerySet
from django.db.models import Q
import random


User = settings.AUTH_USER_MODEL


TAGS_MODELS_VALUES = ['electronics','cars','boats','movies','cameras']
# class UserQuerySet(models.QuerySet):
#     def search(self,query,user=None):
#         lookup = Q(username__icontains=query)
#         if user is not None:
#             lookup &= Q(user=user)
#         return self.filter(lookup)

# class UserManager(models.Manager):
#     def get_queryset(self,*args,**kwargs):
#         return UserQuerySet(self.model, using=self._db)
    
#     def search(self,query,user=None):
#         return self.get_queryset().search(query,user=user)



class ProductQuerySet(models.QuerySet):
    def is_public(self):
        return self.filter(public=True)

    def search(self, query, user=None):
        lookup = Q(title__icontains=query) | Q(content__icontains=query)
        qs =  self.is_public().filter(lookup)
        if user is not None:
            qs2 = self.filter(user=user).filter(lookup)
            qs = (qs | qs2).distinct()
        return qs
    

#search 
#query_set() is built in Model Manager
class ProductManager(models.Manager):
    def get_queryset(self, *args,**kwargs):
        return ProductQuerySet(self.model, using=self._db)
    

    def search(self,query,user=None):
        return self.get_queryset().search(query,user=user)
    



class Product(models.Model):
    #pk
    user = models.ForeignKey(User,default=1,on_delete=models.SET_NULL,null=True)
    title = models.CharField(max_length=120)
    content = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=99.99)
    public = models.BooleanField(default=True)
    
    #connect Product Manager to Product
    objects = ProductManager()
    
    def is_public(self) -> bool:
        return self.public # True or False
    
    def get_tags_list(self):
        return [random.choice(TAGS_MODELS_VALUES)]


    @property
    def sale_price(self):
        return "%.2f" %(float(self.price) * 0.8)
