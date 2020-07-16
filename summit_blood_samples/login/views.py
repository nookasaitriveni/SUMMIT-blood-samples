from django.shortcuts import render
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_text
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate
from django.contrib import messages
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from login.models import UserRole
# from .forms import ResetPasswordForm, SetThePasswordForm

from django.contrib.auth.decorators import login_required
from login.decorators import *
from django.core.paginator import Paginator, EmptyPage, InvalidPage, PageNotAnInteger
from .forms import AddUserForm


class ManageUsers(LoginRequiredMixin, View):
    """
    Class for User management, where Admin can add/block/delete a user.
    """
    login_url = '/'
    redirect_field_name = 'next'
    template_name = 'manageUser.html'
    pageActive = 'users'
    form_class = AddUserForm

    @method_decorator(user_is_entry_admin, name='get')
    def get(self, request, *args, **kwargs):
        """
        Method for GET Request
        :param request: Request
        :param args: args
        :param kwargs: kwargs
        :return: HttpResponse object
        """
        users = UserRole.objects.all().order_by(
            'user__first_name').order_by('user_id__username')

        page = request.GET.get('page', 1)
        paginator = Paginator(users, settings.PAGINATION_PER_PAGE)
        try:
            users = paginator.get_page(page)
        except InvalidPage:
            users = paginator.get_page(0)
        except PageNotAnInteger:
            users = paginator.get_page(0)
        except EmptyPage:
            users = paginator.get_page(0)
        value = int(page) - 1
        value = value*10
        return render(request, self.template_name,
                      {
                          'users': users,
                          'value': value,
                      })
