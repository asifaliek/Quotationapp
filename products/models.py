from django.db import models
import uuid


from customer.models import Customer

# Create your models here.
class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    qty = models.PositiveIntegerField()
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Quotation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, limit_choices_to={'is_deleted':False})
    date = models.DateField()
    subtotal = models.DecimalField(default=0, max_digits=10, decimal_places=2,blank=True, null=True)
    discount = models.DecimalField(default=0, max_digits=10, decimal_places=2,blank=True, null=True)
    total = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.customer

class QuotationItem(models.Model):
    quotation = models.ForeignKey(Quotation,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, limit_choices_to={'is_deleted':False})
    qty = models.PositiveIntegerField()
    is_deleted = models.BooleanField(default=False)

    def subtotal(self):
        return (self.qty * self.product.price)
    def __str__(self):
        return self.quotation.total