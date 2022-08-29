from django.db import models

# Create your models here.
class Content(models.Model):
  image = models.FileField(upload_to='images/', name='content', max_length=255, null=True)
  created_at = models.DateTimeField(auto_now_add=True)

class Style(models.Model):
  image = models.FileField(upload_to='images/', name='style', max_length=255, null=True)
  created_at = models.DateTimeField(auto_now_add=True)

class Generated(models.Model):
  image = models.FileField(upload_to='images/', name='generated', max_length=255, null=True)
  created_at = models.DateTimeField(auto_now_add=True)