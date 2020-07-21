from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.utils.http import (
    url_has_allowed_host_and_scheme, urlsafe_base64_decode,
)
# import the logging library
import logging
from django.http import HttpResponseRedirect
# Get an instance of a logger
logger = logging.getLogger(__name__)


def get_user(uidb64):
    try:
        # urlsafe_base64_decode() decodes to bytestring
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)

        # user = authenticate(request, username=username, password=password)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist, ValidationError):
        logger.error('Something went wrong in getting User')
        user = None
    return user


def reset_password_done(request):
    user = get_user(request.headers['Referer'].split('reset')[1].split('/')[1])
    if user is not None:
        login(request, user)
        return HttpResponseRedirect("/")
