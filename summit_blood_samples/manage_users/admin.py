from django.contrib import admin
from .models import ManageRoles, UserRoles  # Role, UserRoles, User
# from django.contrib.auth.models import User, AbstractUser
# from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
# User._meta.get_field('email').blank = False
# User._meta.get_field('email').null = False
# User._meta.get_field('email')._unique = True
admin.site.unregister(Site)
admin.site.unregister(Group)

# Unregister the provided model admin
admin.site.unregister(User)


# admin.site.register(ManageRoles)

# admin.site.register(UserRoles)


class RoleAdmin(admin.TabularInline):
    list_display = ('name')
    list_filter = ['name']
    model = UserRoles
    extra = 1
    max_num = 1
    min_num = 1
    can_delete = False

class EmailRequiredMixin(object):
    def __init__(self, *args, **kwargs):
        super(EmailRequiredMixin, self).__init__(*args, **kwargs)
        # make user email field required
        self.fields['email'].required = True


class MyUserCreationForm(EmailRequiredMixin, UserCreationForm):
    pass


class MyUserChangeForm(EmailRequiredMixin, UserChangeForm):
    pass

class UserAdmin(admin.ModelAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    inlines = [RoleAdmin, ]
    fields = ('first_name', 'last_name', 'username', 'email', 'is_active',)
    exclude = ('password1', 'password2',)
    list_display = ('username', 'first_name', 'last_name',
                    'email', 'is_active', 'role')
    list_per_page = 20
    search_fields = ['first_name', 'last_name', 'username', 'email']
    list_filter = ['is_active']
    unique_together = ('email',)
    def role(self, obj):
        return UserRoles.objects.filter(user_id=obj.id).first()
    role.admin_order_field = 'role_id__name'
    # def save_model(self, request, obj, form, change):
    #     import ipdb;ipdb.set_trace()
    #     if form.data['email']=="":
    #         messages.add_message(request, messages.ERROR, 'This field is required.')
        #super(UserAdmin, self).save_model(request, obj, form, change)
    # def get_form(self, request, obj=None, **kwargs):
    #     form = super().get_form(request, obj, **kwargs)
    #     form.fields['email'].required = True
    #     # if not is_my_friend(request.user):
    #     #     form.fields['email'].required = True
    #     return form

admin.site.register(User, UserAdmin)
