from django.db import models

# Create your models here.
# models.py
from django.db import models

class DataEntry(models.Model):
    # Define your model fields here
    field1 = models.CharField(max_length=100)
    field2 = models.IntegerField()