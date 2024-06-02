from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.contrib.auth.hashers import make_password

class User(AbstractUser):
    class UserType(models.TextChoices):
        ADMIN = "ADM", "Admin"
        CLIENT = "CLT", "Client"
        
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=100, unique=True, null=True, blank=True)
    id_card_number = models.IntegerField(null=True, blank=True)
    phone_number = models.CharField(max_length=15)
    user_type = models.CharField(max_length = 20, choices=UserType.choices, default=UserType.CLIENT, unique=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'username']

    def save(self, *args, **kwargs):
        if not self.pk:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Request(models.Model):
    client = models.ForeignKey(User, on_delete=models.RESTRICT)
    requested_service = models.CharField(max_length=500)
    service_desc = models.CharField(max_length=500, null=True, blank=True)
    cashpower_number = models.CharField(max_length=50, null=True, blank=True)
    province = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    sector = models.CharField(max_length=50)
    cell = models.CharField(max_length=50)
    village = models.CharField(max_length=50)
    street_number = models.CharField(max_length=30, null=True, blank=True)
    house_number = models.CharField(max_length=30, null=True, blank=True)
    status = models.CharField(max_length=30, default='Pending')
    decision = models.CharField(max_length=100, null=True, blank=True)
    note = models.CharField(max_length=5000, null=True, blank=True)
    requested_on = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.client} - {self.requested_service} => {self.requested_on}"


class Upload(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    file = models.FileField(upload_to='files/')
    type = models.CharField(max_length=30)
    
    def __str__(self) -> str:
        return self.type
    

class RequestHandle(models.Model):
    request = models.ForeignKey(Request, on_delete=models.RESTRICT)
    handler = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    handled_on = models.DateTimeField(auto_now_add=True)


    
class Dispense(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    cash_power = models.CharField(max_length=100)
    done_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return self.cash_power
    