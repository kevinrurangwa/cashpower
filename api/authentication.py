from django.contrib.auth.backends import BaseBackend
from django.db.models import Q
from django.contrib.auth.hashers import check_password
from .models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class MultiModelBackend(BaseBackend):
    # def admin_auth(self, username=None, password=None, **kwargs):
    #     user = User.objects.filter(Q(email=username) | Q(username=username)).first()

    #     if user and self.check_user_password(user, password):
    #         return user
    #     return None
    
    # def check_user_password(self, user, password):
    #     if isinstance(user, User):
    #         return check_password(password, user.password)
    #     return False
    
    # def client_auth(self, username=None, password=None, **kwargs):        
    #     client = Client.objects.filter(Q(email=username) | Q(phone_number=username)).first()

    #     if client and self.check_client_password(client, password):
    #         return client
    #     return None


    # def check_client_password(self, user, password):
    #     if isinstance(user, Client):
    #         return check_password(password, user.password)
    #     return False
    
    
    # def get_user(self, user_id):
    #     try:
    #         return User.objects.get(pk=user_id)
    #     except User.DoesNotExist:
    #         return None

    # def get_client(self, user_id):
    #     try:
    #         return Client.objects.get(pk=user_id)
    #     except Client.DoesNotExist:
    #         return None
    
    
     def authenticate(self, username=None, password=None):
        try:
            user = User.objects.filter(Q(email=username) | Q(username=username)).first()

            if user and user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None
