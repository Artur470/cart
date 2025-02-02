from django.db import models
from django.conf import settings
from product.models import Product
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    total_price = models.FloatField(default=0)

    def __str__(self):
        return str(self.user.username) + " " + str(self.total_price)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    isOrder = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return str(self.user.username) + " " + str(self.product.title)


@receiver(pre_save, sender=CartItem)
def correct_price(sender, **kwargs):
    cart_items = kwargs['instance']
    price_of_product = Product.objects.get(id=cart_items.product.id)
    cart_items.price = cart_items.quantity * float(price_of_product.price)
    # total_cart_items = CartItem.objects.filter(user=cart_items.user)
    # cart = Cart.objects.get(id=cart_items.cart.id)
    # cart.total_price = cart_items.price
    # cart.save()

#
# class Orders(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
#     amount = models.FloatField(default=0)
#     is_paid = models.BooleanField(default=False)
#     order_id = models.CharField(max_length=100)
#     payment_id = models.CharField(max_length=100)
#     payment_signature = models.CharField(max_length=100)
