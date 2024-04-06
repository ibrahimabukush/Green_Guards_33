from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone
from django.urls import reverse

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class Contact(models.Model):
    name= models.CharField(max_length=30)
    email = models.EmailField()
    report=models.CharField(max_length=2048)
    def __str__(self):
        return self.name
class Feedback(models.Model):
    name = models.CharField(max_length=20)
    stars = models.IntegerField()
    text = models.CharField(max_length=500)

    def __str__(self):
        return self.name