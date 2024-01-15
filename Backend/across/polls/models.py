from django.contrib.auth.backends import ModelBackend
from django.db import models


## MODEL CLASS LIKE THIS IN DATABASE TABLE COLUMNS WILL BE FORMED
class UserProfile(models.Model):
    email = models.CharField(max_length=255, unique=True)
    full_name = models.TextField()
    password = models.CharField(max_length=255)
    university_name = models.TextField(default=None)
    signup_using = models.TextField()
    role = models.TextField()

    def __str__(self):
        return self.email

class UserData(models.Model):
    # Define email as a foreign key
    email = models.ForeignKey(UserProfile, to_field='email', on_delete=models.CASCADE)

    # Other Fields
    university_name =  models.TextField()
    course_name = models.TextField()
    completed_modules = models.TextField()

    def __str__(self):
        return f"{self.email} - University: {self.university_name}, Course: {self.course_name}, Completed Modules: {self.completed_modules}"