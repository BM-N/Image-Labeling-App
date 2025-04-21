from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Images(models.Model):
    image = models.ImageField(upload_to="images/")
    # img_path = models.CharField(max_length=200)
    # img_size = models.DecimalField(max_digits=5, decimal_places=4)
    uploaded_at = models.DateTimeField("Date uploaded", auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'image')
    
    def __str__(self):
        return self.image
    
    def save(self, *args, **kwargs):
        if self.image:
            self.img_path = f"images/{self.image.name}"
        super().save(*args, **kwargs)

class Labels(models.Model):
    label = models.CharField(max_length=200)
    image_id = models.OneToOneField(Images, on_delete=models.CASCADE, related_name='label')
    confidence = models.DecimalField(max_digits=5, decimal_places=4)
    uploaded_at = models.DateTimeField("Date uploaded", auto_now_add=True)
    image = models.CharField(max_length=200)
    
    def __str__(self):
        return f'Image: {self.image_id.image.name} / Label:{self.label} / Confidence: {self.confidence}'