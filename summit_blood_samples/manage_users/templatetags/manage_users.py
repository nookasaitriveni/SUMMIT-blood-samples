from django import template
from django.conf import settings
from manage_users.models import UserRoles

register = template.Library()


@register.simple_tag
def user_is_entry_admin_tag(user):
    return user.is_authenticated and UserRoles.objects.get(user_id=user).role_id.id in [1]
