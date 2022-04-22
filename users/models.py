from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Branch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    
    
    def __str__(self):
        return self.name
    
class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    acno = models.CharField(max_length=255)
    balance = models.IntegerField()
    opened = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.acno
    
class Loans(models.Model):
    ammount = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    given = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f'{self.user}'
     
