from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Accommodation(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    services = models.ManyToManyField(Service)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
