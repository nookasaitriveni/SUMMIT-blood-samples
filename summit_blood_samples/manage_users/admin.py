from django.contrib import admin
from .models import ManageRoles, UserRoles  # Role, UserRoles, User
# from django.contrib.auth.models import User, AbstractUser
# from django.contrib.auth.admin import UserAdmin


# class MyUserAdmin(UserAdmin):

#     model = User
#     list_display = ['username', 'email', 'is_active']
#     list_filter = ('email', 'is_active')

#     fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'is_active')}
#          ),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'is_active')}
#          ),
#     )

#     search_fields = ('email',)
#     ordering = ('email',)


# admin.site.register(User, MyUserAdmin)


admin.site.register(ManageRoles)
admin.site.register(UserRoles)
