from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .models import UserRoles


def user_is_entry_admin(func):
    def checkPermission(request, *args, **kwargs):
        if UserRoles.objects.get(user_id=request.user).role_id.id in [1]:
            return func(request, *args, **kwargs)
        raise PermissionError('You are not authorized to access this page')
    return checkPermission
