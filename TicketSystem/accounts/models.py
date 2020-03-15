from django.db import models
from django.contrib.auth.models import User
# Create your models here.


'''
User Profile model with fields for filtering and adding information about customer.
For user request access. In new release - > 0.0000000000000002
'''


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.CharField(max_length=200, blank=True, null=True)
    company = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.user.username

