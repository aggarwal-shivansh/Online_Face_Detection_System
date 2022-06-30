from django.db import models

# Create your models here.

class SignUp(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, primary_key=True)
    username = models.CharField(max_length=10)
    password = models.CharField(max_length=10)
    face_shot = models.ImageField(upload_to='profile_images',blank=True)
    date = models.DateField()
    def __str__(self):
        return self.username