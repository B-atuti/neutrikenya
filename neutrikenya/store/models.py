from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories', blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('name',)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('store:category_detail', args=[self.slug])

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # For sales/discounts
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    is_available = models.BooleanField(default=True)
    stock = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    featured = models.BooleanField(default=False)
    product_line = models.CharField(max_length=100, blank=True)  # e.g., "Vitamin C", "Retinol"
    skin_concern = models.CharField(max_length=100, blank=True)  # e.g., "Acne Skin", "Dry Skin"
    
    class Meta:
        ordering = ('-created_at',)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug])

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products')
    is_main = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Image for {self.product.name}"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Cart {self.id}"
    
    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())
    
    @property
    def item_count(self):
        return sum(item.quantity for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    @property
    def total_price(self):
        return self.product.price * self.quantity

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    
    PAYMENT_METHOD_CHOICES = (
        ('mpesa', 'M-Pesa'),
        ('card', 'Credit/Debit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('cash_on_delivery', 'Cash on Delivery'),
    )
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='mpesa')
    payment_status = models.CharField(max_length=20, default='pending',
                                     choices=(
                                         ('pending', 'Pending'),
                                         ('processing', 'Processing'),
                                         ('completed', 'Completed'),
                                         ('failed', 'Failed'),
                                         ('refunded', 'Refunded'),
                                     ))
    delivery_instructions = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Order {self.id}"
    
    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Save price at time of purchase
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    @property
    def total_price(self):
        return self.price * self.quantity

class UserProfile(models.Model):
    """Extended user profile information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # Contact information
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    # Primary address (shipping)
    address = models.CharField(max_length=200, blank=True, null=True)
    address_line2 = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state_province = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, default="Kenya", blank=True, null=True)
    
    # Optional alternative shipping address
    alt_address = models.CharField("Alternative Address", max_length=200, blank=True, null=True)
    alt_address_line2 = models.CharField("Alternative Address Line 2", max_length=200, blank=True, null=True)
    alt_city = models.CharField("Alternative City", max_length=100, blank=True, null=True)
    alt_state_province = models.CharField("Alternative State/Province", max_length=100, blank=True, null=True)
    alt_postal_code = models.CharField("Alternative Postal Code", max_length=20, blank=True, null=True)
    alt_country = models.CharField("Alternative Country", max_length=100, default="Kenya", blank=True, null=True)
    
    # Payment information
    default_payment_method = models.CharField(max_length=100, blank=True, null=True, 
                                             choices=[
                                                 ('card', 'Credit/Debit Card'),
                                                 ('mpesa', 'M-Pesa'),
                                                 ('paypal', 'PayPal'),
                                                 ('cash', 'Cash on Delivery')
                                             ])
    
    # M-Pesa specific details
    mpesa_phone = models.CharField("M-Pesa Phone Number", max_length=20, blank=True, null=True, 
                                   help_text="Phone number registered with M-Pesa")
    
    # Card details (last 4 digits only for reference)
    card_last_four = models.CharField(max_length=4, blank=True, null=True)
    card_type = models.CharField(max_length=50, blank=True, null=True,
                                choices=[
                                    ('visa', 'Visa'),
                                    ('mastercard', 'Mastercard'),
                                    ('amex', 'American Express'),
                                    ('other', 'Other')
                                ])
    card_expiry = models.CharField(max_length=7, blank=True, null=True, 
                                  help_text="MM/YYYY format")
    
    # Preferences
    receive_newsletter = models.BooleanField(default=True)
    preferred_currency = models.CharField(max_length=3, default="KES", 
                                         choices=[
                                             ('KES', 'Kenyan Shilling'),
                                             ('USD', 'US Dollar'),
                                             ('EUR', 'Euro'),
                                             ('GBP', 'British Pound')
                                         ])
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Profile for {self.user.username}"
    
    def get_full_address(self):
        """Return formatted full address"""
        parts = [self.address]
        if self.address_line2:
            parts.append(self.address_line2)
        if self.city:
            parts.append(self.city)
        if self.state_province:
            parts.append(self.state_province)
        if self.postal_code:
            parts.append(self.postal_code)
        if self.country:
            parts.append(self.country)
        return ", ".join(filter(None, parts))
    
    def has_complete_shipping_info(self):
        """Check if user has completed minimum shipping information"""
        return all([self.address, self.city, self.phone])
    
    def has_complete_payment_info(self):
        """Check if user has a valid payment method set up"""
        if not self.default_payment_method:
            return False
        if self.default_payment_method == 'mpesa' and not self.mpesa_phone:
            return False
        if self.default_payment_method == 'card' and not self.card_last_four:
            return False
        return True

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """Create or update user profile when user is created/updated"""
    if created:
        UserProfile.objects.create(user=instance)
    else:
        if not hasattr(instance, 'profile'):
            UserProfile.objects.create(user=instance)
