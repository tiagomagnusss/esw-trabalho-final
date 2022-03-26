from django.db import models

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=60)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10000)
    created_at = models.DateTimeField(auto_now_add=True)
    sold = models.BooleanField(default=False)
    original_owner = models.ForeignKey('auth.User', related_name='products', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', blank=True, null=True)