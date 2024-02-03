from django.shortcuts import render


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework import authentication,permissions
from rest_framework.decorators import action



from api.serializers import UserSerializer,ProductSerializer,BasketItemSerializer,BasketSerializer
from api.models import Product,Basket,BasketItem





class SignUpView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(data=serializer.errors)
    
class ProductsView(viewsets.ModelViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=ProductSerializer
    queryset=Product.objects.all()

    def create(self,request,*args,**kwargs):
        raise serializers.ValidationError("permission denied")

    def update(self,request,*args,**kwargs):
        raise serializers.ValidationError("permission denied")
    
    def destroy(self,request,*args,**kwargs):
        raise serializers.ValidationError("permission denied") 

    @action(methods=["post"],detail=True)
    def add_to_basket(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        product_object=Product.objects.get(id=id)
        basket_object=request.user.cart
        serializer=BasketItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(product=product_object,basket=basket_object)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
class BasketView(viewsets.ViewSet):

    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def list(self,request,*args,**kwargs):
        qs=request.user.cart
        serializer=BasketSerializer(qs,many=False)
        return Response(data=serializer.data)
    
class BasketItemView(viewsets.ModelViewSet):

    serializer_class=BasketItemSerializer
    queryset=BasketItem.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def create(self,request,*args,**kwargs):
        raise serializers.ValidationError("permission denied")




