from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpRequest
from django.contrib.auth.forms import PasswordResetForm
# from django.conf import settings


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        form = PasswordResetForm({'email': instance.email})

        if form.is_valid():
            current_site = get_current_site(request=None)
            request = HttpRequest()
            request.META['HTTP_HOST'] = current_site.domain
            # if settings.DEBUG:
            #     request.META['HTTP_HOST'] = '127.0.0.1:8000'
            # else:
            #     request.META['HTTP_HOST'] = 'www.mysite.com'
            form.save(
                request=request,
                use_https=False,
                from_email="krishna.n@valuelabs.com",
                html_email_template_name='registration/new_user_html_password_reset_email.html')
