from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from product.models import Product
from .models import Cart, CartItem
from .serializer import CartSerializer, CartItemSerializer


class CartView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        cart = Cart.objects.filter(user=user, ordered=False).first()
        queryset = CartItem.objects.filter(cart=cart)
        serializer = CartItemSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        user = request.user
        cart,_ = Cart.objects.get_or_create(user=user, ordered=False)
        print(cart)
        product = Product.objects.get(id=data.get('product'))
        price = product.price
        quantity = data.get('quantity', 1)
        cart_items = CartItem(cart=cart, user=user, product=product, price=price, quantity=quantity)
        cart_items.save()

        total_price = 0
        cart_items = CartItem.objects.filter(user=user, cart=cart.id)
        for items in cart_items:
            total_price += items.price
        cart.total_price = total_price
        cart.save()
        return Response({'success': 'Items Added to your cart '})


    def put(self, request):
        data = request.data
        cart_item = CartItem.objects.get(id=data.get('id'))
        quantity = data.get('quantity')
        cart_item.quantity = quantity
        cart_item.save()
        return Response({'success': 'Items Updated'})


    def delete(self, request):
        user = request.user
        data = request.data
        cart_item = CartItem.objects.get(id=data.get('id'))
        cart_item.delete()

        cart = Cart.objects.filter(user=user, ordered=False).first()
        queryset = CartItem.objects.filter(cart=cart)
        serializer = CartItemSerializer(queryset, many=True)
        return Response(serializer.data)

