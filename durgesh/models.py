from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"Profile: {self.user.username}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('placed', 'Placed'),
        ('preparing', 'Preparing'),
        ('delivering', 'Delivering'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    subtotal = models.IntegerField(default=0)
    delivery_fee = models.IntegerField(default=0)
    taxes = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='placed')

    def __str__(self):
        return f"Order {self.id} by {self.user.username} - {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    qty = models.IntegerField(default=1)
    image = models.CharField(max_length=512, blank=True)

    def __str__(self):
        return f"{self.qty}x {self.name} ({self.order.id})"


class SavedItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_items')
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    image = models.CharField(max_length=512, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Saved: {self.name} ({self.user.username})"


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    qty = models.IntegerField(default=1)
    image = models.CharField(max_length=512, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'name', 'price')

    def __str__(self):
        return f"CartItem: {self.qty}x {self.name} ({self.user.username})"
