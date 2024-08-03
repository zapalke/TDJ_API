from django.db import models
from django.utils import timezone

class ApiKeys(models.Model):
    """
    Model that stores API keys along with thier along with their expiration date
    """
    api_key = models.CharField(max_length=100, unique=True)
    valid_from = models.DateTimeField(default=timezone.now())
    valid_to = models.DateTimeField(blank=False)

    def __str__(self):
        return f'{self.api_key} valid from {self.valid_from} to {self.valid_to}'

class RequestLog(models.Model):
    """
    Model that stores request from clients with thier IP adresses.
    """
    ip = models.CharField(max_length=45)
    request_time = models.DateTimeField(auto_now=True)
    api_key = models.ForeignKey(ApiKeys, on_delete=models.SET_NULL, to_field='api_key', blank=True, null=True)

    def __str__(self):
        return f'{self.ip} at {self.request_time}'
    
