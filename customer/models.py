from django.db import models
import uuid

# Create your models here.
class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    phone = models.CharField(max_length=10,unique=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

