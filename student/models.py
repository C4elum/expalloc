from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


def upload_location(instance, filename):
    return "student_pdfs/{name}/{filename}".format(name=instance.name, filename=filename)

class Student(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True) 
    branch = models.CharField(max_length=50)
    cgpa = models.FloatField()
    document = models.FileField(upload_to=upload_location)

    def _str_(self):
        return self.name

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message