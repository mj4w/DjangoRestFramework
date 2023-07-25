# from django.http import JsonResponse ,HttpResponse
import json
from django.forms.models import model_to_dict
from product.models import Product
from rest_framework.response import Response
from rest_framework.decorators import api_view
from product.serializers import ProductSerializer

@api_view(["POST"])
def api_home(request,*args,**kwargs):

    """
    DRF API VIEW
    """
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        # instance = serializer.save()
        print(serializer.data)
        return Response(serializer.data)
    return Response({"invalid":"not good data"},status=200)
    # if request.method != "GET":
    #     return Response({"detail":"Get not allowed"}, status=301)
    # data = request.data
    # instance = Product.objects.all().order_by("?").first()
    # data = {}
    # if instance:
    #     data = ProductSerializer(instance).data
    #     # data = model_to_dict(model_data, fields=['id','title','price','sale_price'])
    
    # return Response(data)
    # #     print(data)
    # #     data =  dict(data)
    # #     json_data_str = json.dumps(data)
    # #     # data['id'] = model_data.id
    # #     # data['title'] = model_data.title
    # #     # data['content'] = model_data.content
    # #     # data['price'] = model_data.price
    # #     # serialization
    # #     # model instance (model_data) 
    # #     # turn a Python Dict
    # #     # return JSON to my client
    # # return JsonResponse(json_data_str, headers={"content-type":"application/json"})








    # #request -> HTTPRequest -> Django
    # #print(dir(request))
    # #request.body
    # print(request.GET)
    # print(request.POST)
    # body = request.body # byte string of JSON DATA
    # data = {}
    # try:
    #     data = json.loads(body) # string of JSON Data -> Python Dict
    # except:
    #     pass

    # print(data)
    # data['params'] = dict(request.GET)
    # data['headers'] = dict(request.headers)
    # # data['headers'] = request.headers # request.META ->
    # data['content_type'] = request.content_type