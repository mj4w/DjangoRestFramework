from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register
from .models import Product


@register(Product)
class ProductIndex(AlgoliaIndex):

    #should_index capture all the products that has been a checked or true
    # should_index = 'is_public'

    fields = [
        'title',
        'content',
        'price',
        'user',
        'public',
    ]
    #this tags get randomly place in every products 
    tags = 'get_tags_list'

    #this make our search engine limited by searching product
    settings = {
        'searchableAttributes':['title','content'],
        'attributesForFaceting':['user','public']
    }