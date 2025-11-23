# models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    priority = models.IntegerField(default=999, help_text="ترتیب نمایش در صفحه اصلی (عدد کمتر= بالاتر)")

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = price = models.PositiveIntegerField(
        validators=[MaxValueValidator(9999999)]
    )
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True)
    priority = models.IntegerField(default=999, help_text="ترتیب نمایش در صفحه اصلی (عدد کمتر= بالاتر)")


    def __str__(self):
        return self.name


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return self.menu_item.price * self.quantity

    def __str__(self):
        return f"{self.user.username} cart: {self.menu_item.name}"


# class Order(models.Model):
#     STATUS_CHOICES = [
#         ('Pending', 'در انتظار پرداخت'),
#         ('Paid', 'پرداخت شده'),
#         ('Preparing', 'در حال آماده‌سازی'),
#         ('Sent', 'ارسال شده'),
#         ('Delivered', 'تحویل شده'),
#     ]

#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
#     created_at = models.DateTimeField(auto_now_add=True)
#     total_price = models.PositiveIntegerField(default=0) 
    
#     def __str__(self):
#         return f"Order #{self.id} - {self.user.username}"


# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
#     product_name = models.CharField(max_length=100) 
#     product_price = models.PositiveIntegerField() 
#     quantity = models.PositiveIntegerField(default=1)

#     def __str__(self):
#         return f"{self.product_name} (x{self.quantity})"
