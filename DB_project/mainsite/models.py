from django.db import models

# Create your models here.

class student_info(models.Model):
    major=models.TextField(blank=True)
    name=models.TextField(blank=True)
    number=models.CharField(max_length=10)
