# # from django.db import models
# # from Store.models import Product,Variation # Make sure this import is correct
# #
# #
# #
# #
# # class Cart(models.Model):
# #     cart_id = models.CharField(max_length=100, blank=True)
# #     date_added = models.DateField(auto_now_add=True)
# #
# #     def __str__(self):
# #         return self.cart_id
# #
# # class CartItem(models.Model):
# #     product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Direct reference
# #     variations= models.ManyToManyField(Variation, blank=True)
# #     cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
# #     quantity = models.IntegerField(default=1)
# #     is_active = models.BooleanField(default=True)
# #
# #     def sub_total(self):
# #         return self.product.price * self.quantity
# #
# #     color = models.CharField(max_length=50, blank=True, null=True)
# #     size = models.CharField(max_length=50, blank=True, null=True)
# #
# #
# #     def __str__(self):
# #         return self.product
# #
# #
# #
# #
#
#
# from django.db import models
# from Store.models import Product, Variation  # Ensure this import is correct
#
# from Account.models import Account
#
#
# class Cart(models.Model):
#     cart_id = models.CharField(max_length=100, blank=True)
#     date_added = models.DateField(auto_now_add=True)
#
#     def __str__(self):
#         return self.cart_id
#
# # class CartItem(models.Model):
# #     product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Direct reference
# #     variation = models.ForeignKey(Variation, on_delete=models.SET_NULL, null=True, blank=True)  # Use ForeignKey if only one variation
# #     cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
# #     quantity = models.IntegerField(default=1)
# #     is_active = models.BooleanField(default=True)
# #     color = models.CharField(max_length=50, blank=True, null=True)
# #     size = models.CharField(max_length=50, blank=True, null=True)
# #     user=models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
#
# class CartItem(models.Model):
#     user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     variations = models.ManyToManyField(Variation, blank=True)
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
#     quantity = models.IntegerField()
#     is_active = models.BooleanField(default=True)
#
#     def sub_total(self):
#         return self.product.price * self.quantity
#
#     def __unicode__(self):
#         # Ensure this returns a string, not a Product object
#         return f'{self.product} - {self.quantity}'  # or use another field name



from django.db import models
from django.conf import settings
from Store.models import Product, Variation

class Cart(models.Model):
    cart_id = models.CharField(max_length=100, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f'{self.product} - {self.quantity}'

    class Meta:
        unique_together = ('user', 'product', 'cart')
