from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save #once the user reg, same time to create the basket


class Category(models.Model):
    name=models.CharField(max_length=200)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    title=models.CharField(max_length=200)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name="items")
    price=models.PositiveIntegerField()
    description=models.CharField(max_length=200,null=True)
    picture=models.ImageField(upload_to="images",default='default.jpg',null=True)
    is_trending=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Basket(models.Model):
    owner=models.OneToOneField(User,on_delete=models.CASCADE,related_name="cart")
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    @property
    def cart_items(self):
        qs=self.cartitem.all()
        return qs
    
    @property
    def basket_item_total(self):
        basket_items=self.cart_items
        if basket_items:
            total=sum([item.total for item in basket_items]) 
            return total
        else:
            return 0 


class BasketItem(models.Model):
    basket=models.ForeignKey(Basket,on_delete=models.CASCADE,related_name="cartitem")
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    qty=models.PositiveIntegerField(default=1)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    @property
    def total(self):
        return self.qty*self.product.price
    # total=models.PositiveIntegerField(null=True)

    # def save(self,*args,**kwargs):
    #     if not self.total:
    #         self.total=self.product.price * self.qty
    #     super().save(*args,**kwargs)       


def create_basket(sender,instance,created,**kwargs):
    if created:
        Basket.objects.create(owner=instance)
post_save.connect(create_basket,sender=User)