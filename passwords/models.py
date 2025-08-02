from django.db import models
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
from django.conf import settings
import base64

class PasswordEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    website_name = models.CharField(max_length=200)
    username = models.CharField(max_length=200, blank=True, null=True)  # Made optional
    encrypted_password = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        if self.username:
            return f"{self.website_name} - {self.username}"
        else:
            return f"{self.website_name}"

    def set_password(self, raw_password):
        """Encrypt and store password"""
        # Ensure secret key is exactly 32 bytes for Fernet
        secret_key = settings.SECRET_KEY.encode()
        if len(secret_key) < 32:
            secret_key = secret_key.ljust(32, b'0')
        elif len(secret_key) > 32:
            secret_key = secret_key[:32]
        
        key = base64.urlsafe_b64encode(secret_key)
        fernet = Fernet(key)
        self.encrypted_password = fernet.encrypt(raw_password.encode()).decode()

    def get_password(self):
        """Decrypt and return password"""
        # Ensure secret key is exactly 32 bytes for Fernet
        secret_key = settings.SECRET_KEY.encode()
        if len(secret_key) < 32:
            secret_key = secret_key.ljust(32, b'0')
        elif len(secret_key) > 32:
            secret_key = secret_key[:32]
            
        key = base64.urlsafe_b64encode(secret_key)
        fernet = Fernet(key)
        return fernet.decrypt(self.encrypted_password.encode()).decode()
