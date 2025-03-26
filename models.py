import datetime
import os
import uuid
from django.db import models
from django.contrib.auth.models import User

# Function to generate unique filenames
def getFileName(request, filename):
    unique_id = uuid.uuid4().hex  # Generate a unique identifier
    now_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # Fixed format issue
    new_filename = "%s_%s_%s" % (now_time, unique_id, filename)
    return os.path.join('uploads/', new_filename)


# Category Model
class Category(models.Model):
    ACTIVE = 'A'
    INACTIVE = 'I'
    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
    ]
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=getFileName, null=True, blank=True)
    description = models.TextField(max_length=500, null=False, blank=False)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=INACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


# Product Model
class Product(models.Model):
    ACTIVE = 'A'
    INACTIVE = 'I'
    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
    ]
    DEFAULT = 'D'
    TRENDING = 'T'
    TRENDING_CHOICES = [
        (DEFAULT, 'Default'),
        (TRENDING, 'Trending'),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # ForeignKey to Category
    name = models.CharField(max_length=150, null=False, blank=False)
    vendor = models.CharField(max_length=150, null=False, blank=False)
    product_image = models.ImageField(upload_to=getFileName, null=True, blank=True)
    quantity = models.IntegerField(null=False, blank=False)
    original_price = models.FloatField(null=False, blank=False)
    selling_price = models.FloatField(null=False, blank=False)
    description = models.TextField(max_length=500, null=False, blank=False)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=INACTIVE)
    trending = models.CharField(max_length=1, choices=TRENDING_CHOICES, default=DEFAULT)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # Show newest products first
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name

    @property
    def total_cost(self):
        return self.quantity * self.selling_price


# Cart Model
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_qty = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_cost(self):
        return self.product_qty * self.product.selling_price


# Favourite Model
class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
