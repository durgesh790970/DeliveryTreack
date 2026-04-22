from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    """Extended user profile with complete personal information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Personal Info
    phone = models.CharField(max_length=15, blank=True, null=True)
    alternate_phone = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('Other', 'Other')], blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    
    # Profile Details
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    # Preferences
    receive_notifications = models.BooleanField(default=True)
    receive_offers = models.BooleanField(default=True)
    receive_sms = models.BooleanField(default=False)
    
    # Metadata
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"Profile: {self.user.username}"


class UserAddress(models.Model):
    """User delivery addresses"""
    ADDRESS_TYPE_CHOICES = [
        ('home', 'Home'),
        ('work', 'Work'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    
    # Address Info
    address_type = models.CharField(max_length=20, choices=ADDRESS_TYPE_CHOICES, default='home')
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    
    # Address Details
    street_address = models.CharField(max_length=500)
    apartment = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100, default='India')
    
    # Additional
    landmark = models.CharField(max_length=255, blank=True)
    delivery_instructions = models.TextField(blank=True)
    
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "User Addresses"

    def __str__(self):
        return f"{self.get_address_type_display()} - {self.user.username} - {self.city}"


class PaymentMethod(models.Model):
    """Saved payment methods"""
    PAYMENT_TYPE_CHOICES = [
        ('upi', 'UPI'),
        ('card', 'Credit/Debit Card'),
        ('wallet', 'Digital Wallet'),
        ('netbanking', 'Net Banking'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_methods')
    
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES)
    
    # UPI Details
    upi_id = models.CharField(max_length=100, blank=True, null=True)
    
    # Card Details (Encrypted)
    card_last_four = models.CharField(max_length=4, blank=True)
    card_holder_name = models.CharField(max_length=255, blank=True)
    card_brand = models.CharField(max_length=50, blank=True)  # Visa, Mastercard, etc
    card_expiry = models.CharField(max_length=10, blank=True)  # MM/YY format
    
    # Wallet Details
    wallet_name = models.CharField(max_length=100, blank=True)
    wallet_identifier = models.CharField(max_length=100, blank=True)
    
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.payment_type == 'upi':
            return f"UPI - {self.upi_id}"
        elif self.payment_type == 'card':
            return f"{self.card_brand} - ****{self.card_last_four}"
        else:
            return f"{self.get_payment_type_display()} - {self.user.username}"


class Order(models.Model):
    """Complete order information"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready'),
        ('on_way', 'On the way'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('failed', 'Payment Failed'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    
    # Order Details
    order_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    
    # Delivery Address
    delivery_address = models.ForeignKey(UserAddress, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Payment Method Used
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Pricing
    subtotal = models.IntegerField(default=0)
    delivery_fee = models.IntegerField(default=0)
    taxes = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    coupon_code = models.CharField(max_length=50, blank=True)
    total = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    delivered_at = models.DateTimeField(blank=True, null=True)
    
    # Additional Info
    notes = models.TextField(blank=True)
    rating = models.IntegerField(null=True, blank=True, choices=[(i, i) for i in range(1, 6)])
    feedback = models.TextField(blank=True)

    def __str__(self):
        return f"Order {self.order_number} - {self.user.username}"


class OrderItem(models.Model):
    """Individual items in an order"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    
    # Item Details
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100, blank=True)
    price = models.IntegerField()
    qty = models.IntegerField(default=1)
    image = models.CharField(max_length=512, blank=True)
    
    # Customizations/Notes
    special_instructions = models.TextField(blank=True)
    
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.qty}x {self.name} in Order {self.order.order_number}"


class SavedItem(models.Model):
    """User's favorite/saved items"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_items')
    
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    category = models.CharField(max_length=100, blank=True)
    image = models.CharField(max_length=512, blank=True)
    restaurant = models.CharField(max_length=255, blank=True)
    
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Saved: {self.name} ({self.user.username})"


class CartItem(models.Model):
    """Shopping cart items"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    qty = models.IntegerField(default=1)
    image = models.CharField(max_length=512, blank=True)
    
    # Additional Info
    category = models.CharField(max_length=100, blank=True)
    restaurant = models.CharField(max_length=255, blank=True)
    special_instructions = models.TextField(blank=True)
    
    added_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'name', 'restaurant')

    def __str__(self):
        return f"CartItem: {self.qty}x {self.name} ({self.user.username})"


class UserActivity(models.Model):
    """Track user actions and activities"""
    ACTIVITY_TYPE_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('signup', 'Sign Up'),
        ('order_placed', 'Order Placed'),
        ('order_cancelled', 'Order Cancelled'),
        ('address_added', 'Address Added'),
        ('payment_added', 'Payment Method Added'),
        ('profile_updated', 'Profile Updated'),
        ('password_changed', 'Password Changed'),
        ('search', 'Search'),
        ('view_item', 'View Item'),
        ('add_to_cart', 'Add to Cart'),
        ('remove_from_cart', 'Remove from Cart'),
        ('save_item', 'Save Item'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_TYPE_CHOICES)
    
    # Activity Details
    description = models.TextField(blank=True)
    related_order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    related_address = models.ForeignKey(UserAddress, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Metadata
    ip_address = models.CharField(max_length=45, blank=True)
    user_agent = models.TextField(blank=True)
    
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "User Activities"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.get_activity_type_display()} - {self.created_at}"
