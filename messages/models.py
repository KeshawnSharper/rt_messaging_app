from django.db import models

# Create your models here.
class Messages(models.Model):
  receiver_email = models.CharField(max_length=255)
  sender_email = models.CharField(max_length=255)
  text = models.CharField(max_length=255)
  date = models.DateTimeField(max_length=255)