from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('blog-home')


class Rebort(models.Model):
    city = models.CharField(max_length=100)
    location_latitude = models.FloatField()
    location_longitude = models.FloatField()
    explanation = models.TextField()
    image = models.ImageField(upload_to='rebort_images/')
    solution = models.TextField()
    data_rebort=models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False, null=True)  # Set a default value
    response = models.TextField(blank=True, null=True)
    

    def save(self, *args, **kwargs):
        if self.deleted is None:
            self.deleted = False  # Set default value if None
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.city
    
    def get_absolute_url(self):
        return reverse('blog-myreborts')