from django.db import models


# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=60)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10000)
    created_at = models.DateTimeField(auto_now_add=True)
    sold = models.BooleanField(default=False)
    original_owner = models.ForeignKey('auth.User', related_name='products', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    liked_by = models.ManyToManyField('auth.User')

    def __str__(self):
        return "%s : %s" % (self.title, self.description)

    class Meta:
        unique_together = ("title", "original_owner")


class Trade(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    seller = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    buyer_email = models.EmailField(max_length=254)
    observation = models.CharField(max_length=60, blank=True, null=True)

class Report(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    reporter = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    description = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(blank=True, null=True)