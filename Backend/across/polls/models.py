from django.contrib.auth.backends import ModelBackend
from django.db import models


## MODEL CLASS LIKE THIS IN DATABASE TABLE COLUMNS WILL BE FORMED
class UserProfile(models.Model):
    email = models.CharField(max_length=255, unique=True)
    full_name = models.TextField()
    password = models.CharField(max_length=255)
    university_name = models.TextField(null=True)
    signup_using = models.TextField()
    role = models.TextField()

    def __str__(self):
        return self.email
