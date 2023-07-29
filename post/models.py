from django.db import models
from django.contrib.auth.models import  User
# Create your models here.

class Post(models.Model):
  title = models.CharField(max_length= 255)
  post_type = models.CharField(max_length= 255)
  description = models.TextField(null=True, blank=True)
  image = models.ImageField(upload_to='image', blank=True,default='images/no-image.jpg')
  created_at = models.DateTimeField(auto_now_add=True)
  user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)

  def __str__(self):
    return self.title

  class Meta:
    ordering = ['-created_at']
  
  