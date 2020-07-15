from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.conf import settings
from django.contrib.auth.hashers import check_password


class Role(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.name)


class UserRole(models.Model):
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='userrole_user')
    role_id = models.ForeignKey(
        Role, on_delete=models.CASCADE, related_name='userrole_role')

    class Meta:
        pass

    def __str__(self):
        return str(f'{self.user_id.username} | {self.role_id.name}')
