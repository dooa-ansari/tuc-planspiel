from django.db import models
from user import models as userModels

class TransferCredits(models.Model):
    # Define email as a foreign key
    email = models.ForeignKey(userModels.UserProfile, to_field='email', on_delete=models.CASCADE)

    # Other Fields
    status = models.TextField()
    fromModules = models.JSONField(null=True)
    toModules = models.JSONField(null=True)
    # Timestamp fields
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.email} - Status: {self.status}, Created At: {self.created_at}, Updated At: {self.updated_at}"
