from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    image=models.ImageField(default='default.jpg',upload_to='profile_pics')
    bio=models.TextField(default='',max_length=120)
    def __str__(self):
        return self.user.username
   
    def save(self,*args,**kargs):
        super().save(*args,**kargs)
        img=Image.open(self.image.path)
        if img.height>300 or img.width > 300:
            output_size=(300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)