from django import forms
# from Company.models import Department, GroupDetails, CompanyDetails, UserCompanyMap, GroupCompanyMap, CompanyDepartmentMap
from django.contrib.auth.models import Group, User
from django.db.models import Q
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError
from django.conf import settings
from .models import Role
# import magic


# class GetUserGroupType:

#     @staticmethod
#     def getThegrpoups(user_id):
#         u = User.objects.get(pk=user_id)
#         user_grp = u.groups.all()[0].id
#         if user_grp == 1:
#             # groups = Group.objects.filter(~Q(pk=user_grp))
#             groups = Group.objects.all()
#         else:
#             groups = Group.objects.filter(~Q(pk__in=[1, 2]))
#         grps = []
#         for g in groups:
#             grps.append((g.id, g.name))
#         return grps


# class Departments:

#     @staticmethod
#     def getTheDepartments(CC=None):
#         departments = []
#         if CC is None:
#             department = Department.objects.all().order_by('name')
#             for d in department:
#                 departments.append((d.id, f'{d.name}'))
#         else:
#             department = CompanyDepartmentMap.objects.filter(company=CC).order_by('department__name')
#             for d in department:
#                 departments.append((d.department.id, f'{d.department.name}'))
#         if len(departments) == 0:
#             departments.append(('', 'No department(s) added'))
#         return departments


# class Company:

#     @staticmethod
#     def getTheCompany(c_id=None):
#         if c_id is None:
#             comps = CompanyDetails.objects.filter(company_status=1).order_by('company_name')
#         else:
#             # comps = CompanyDetails.objects.filter(pk__in=c_id, company_status=1).order_by('company_name')
#             comps = c_id
#         companies = [('', 'Select Company')]
#         for c in comps:
#             companies.append((c.id, c.company_name))
#         if len(companies) == 0:
#             companies.append(('', 'No company is added'))
#         # companies.insert(0, ('', 'Select Company'))
#         # companies.insert(0, ('', ''))
#         return companies


# class CompanyGroup:

#     @staticmethod
#     def getTheGroups(CC=None):
#         groups = []
#         if CC is None:
#             grps = GroupDetails.objects.all().order_by('name')
#             for g in grps:
#                 groups.append((g.id, g.name))
#         else:
#             grps = GroupCompanyMap.objects.filter(company=CC).order_by('group__name')
#             for g in grps:
#                 groups.append((g.group.id, g.group.name))
#         if len(groups) == 0:
#             groups.append(('', 'No group is added'))
#         return groups


# def CheckImageFile(value):
#     mime = magic.from_buffer(value.read(), mime=True)
#     if mime not in settings.ALLOWED_LOGO_MIME.values():
#         raise ValidationError('Invalid image type')


class AddUserForm(forms.Form):

    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'required': True, 'class': 'form-control',
                   'placeholder': 'First Name'}
        ),
        label='First Name'
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'required': True, 'class': 'form-control',
                   'placeholder': 'Last Name'}
        ),
        label='Last Name'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'required': True, 'class': 'form-control',
                   'placeholder': 'Email'}
        ),
        label='Email'
    )
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'required': True, 'class': 'form-control',
                   'placeholder': 'Username'}
        ),
        label='Username'
    )
    # password = forms.CharField(
    #     widget=forms.PasswordInput(
    #         attrs={'class': 'form-control', 'placeholder': 'Password'}
    #     ),
    #     label='Password'
    # )
    password = forms.CharField(label='Password')

    role = forms.CharField(
        widget=forms.Select(
            attrs={'required': True, 'class': 'form-control select2 custom-select2 company_select',
                   'style': 'width: 100%;', 'placeholder': 'Select Company'},
            choices=Role.objects.all()
        ),
        label='Role',
        required=True
    )

    def __init__(self, *args, **kwargs):

        self.user_id = kwargs.pop('user_id')
        self.request = kwargs.pop('request')
        # grp = Group.objects.filter(user=User.objects.get(pk=self.user_id))
        # if grp.id == 2:
        #     self.fields.
        try:
            self.task = kwargs.pop('task')
        except:
            self.task = None
        super(AddUserForm, self).__init__(*args, **kwargs)
        # self.fields['user_type'].widget = forms.Select(
        #     attrs={'required': True, 'class': 'form-control select2 custom-select2 user_type',
        #            'style': 'width: 100%;'},
        #     choices=GetUserGroupType.getThegrpoups(self.user_id)
        # )
        # if self.task is not None:
        #     self.fields['password'].widget = forms.PasswordInput(
        #         attrs={'class': 'form-control',
        #                'required': False, 'placeholder': 'Password'}
        #     )
        #     self.fields['password'].required = False
        # else:
        #     self.fields['password'].widget = forms.PasswordInput(
        #         attrs={'class': 'form-control',
        #                'required': True, 'placeholder': 'Password'}
        #     )
        #     self.fields['password'].required = True
        # self.fields['company'].widget = forms.Select(
        #     attrs={'required': True, 'class': 'form-control select2 custom-select2 company_select',
        #            'style': 'width: 100%;'},
        #     choices=Company.getTheCompany(
        #         self.request.company if self.request.user.groups.all()[0].id != 1 else None)
        # )
        # if self.initial and self.initial['company']:
        #     try:
        #         self.fields['manager'].queryset = User.objects.filter(pk__in=UserCompanyMap.objects.filter(
        #             company=self.initial['company']).values_list('user')).order_by('first_name')
        #         self.fields['groups'].widget.choices = CompanyGroup.getTheGroups(
        #             CC=self.initial['company'])
        #         self.fields['department'].widget.choices = Departments.getTheDepartments(
        #             CC=self.initial['company'])
        #     except:
        #         pass

        # else:
        #     self.fields['manager'].queryset = User.objects.filter(pk__in=UserCompanyMap.objects.filter(
        #         company=self.request.current_company).values_list('user')).order_by('first_name')
        #     self.fields['groups'].widget.choices = CompanyGroup.getTheGroups(
        #         CC=self.request.current_company)
        #     self.fields['department'].widget.choices = Departments.getTheDepartments(
        #         CC=self.request.current_company)
        # if self.data.get('company'):
        #     try:
        #         company_id = int(self.data.get('company'))
        #         self.fields['manager'].queryset = User.objects.filter(pk__in=UserCompanyMap.objects.filter(
        #             company=company_id).values_list('user')).order_by('first_name')
        #     except (ValueError, TypeError):
        #         pass  # invalid input from the client; ignore and fallback to empty City queryset


# class AddUserTypeForm(forms.Form):
#     type_name = forms.CharField(
#         widget=forms.TextInput(
#             attrs={'required': True, 'class': 'form-control', 'placeholder': 'Type Name'}
#         ),
#         label='User Type'
#     )


# class AddDepartmentForm(forms.Form):
#     department_name = forms.CharField(
#         widget=forms.TextInput(
#             attrs={'required': True, 'class': 'form-control', 'placeholder': 'Department Name','autofocus':'autofocus'}
#         ),
#         label='Department Name'
#     )
#     code = forms.CharField(
#         widget=forms.TextInput(
#             attrs={'class': 'form-control', 'placeholder': 'Short Name'}
#         ),
#         label='Alias',
#         required=False
#     )
#     users = forms.MultipleChoiceField(
#         widget=forms.SelectMultiple(
#             attrs={'class': 'form-control select2 custom-select2 assign-users-select-main', 'style': 'width: 100%','placeholder':'Select'},
#         ),
#         label='User(s)',
#         choices=[],
#         required=False
#     )
#     def __init__(self, *args, **kwargs):
#         '''
#         init method to override fields
#         '''
#         super(AddDepartmentForm, self).__init__(*args, **kwargs)

#         try:
#             rq = kwargs['initial']['request']
#             # print(kwargs['initial']['request']['contributors'])
#             if rq.method == 'POST':
#                 users = kwargs['initial']['request'].POST.getlist('users')
#                 users = list(zip(users, users))
#                 self.fields['users'].choices = users
#         except:
#             pass

# class AddCompanyForm(forms.Form):
#     company_name = forms.CharField(
#         widget=forms.TextInput(
#             attrs={'required': True, 'class': 'form-control', 'placeholder': 'Company Name', 'autofocus': 'autofocus'}
#         ),
#         label='Company Name'
#     )
#     company_address = forms.CharField(
#         widget=forms.Textarea(
#             attrs={'class': 'form-control', 'placeholder': 'Address', 'rows': 3}
#         ),
#         label='Address'
#     )
#     company_logo = forms.FileField(
#         widget=forms.ClearableFileInput(
#             attrs={'required': False, 'class': 'form-control'}
#         ),
#         label='Logo',
#         required=False,
#     )
#     users = forms.MultipleChoiceField(
#         widget=forms.SelectMultiple(
#             attrs={'class': 'form-control select2 custom-select2 assign-users-select-main', 'style': 'width: 100%','placeholder':'Select'},
#         ),
#         label='User(s)',
#         choices=[],
#         required=False
#     )

#     def __init__(self, *args, **kwargs):
#         '''
#         init method to override fields
#         '''
#         super(AddCompanyForm, self).__init__(*args, **kwargs)

#         try:
#             rq = kwargs['initial']['request']
#             # print(kwargs['initial']['request']['contributors'])
#             if rq.method == 'POST':
#                 users = kwargs['initial']['request'].POST.getlist('users')
#                 users = list(zip(users, users))
#                 self.fields['users'].choices = users
#         except:
#             pass

# class AddGroupForm(forms.Form):
#     # def __init__(self, *args, **kwargs):
#     #     super(AddGroupForm, self).__init__(*args, **kwargs)
#     #     if kwargs['initial']:
#     #         self.fields['group_company'].choices = kwargs['initial'].company
#     group_name = forms.CharField(
#         widget=forms.TextInput(
#             attrs={'required': True, 'class': 'form-control', 'placeholder': 'Name','autofocus': 'autofocus'}
#         ),
#         label='Team Name'
#     )
#     group_code = forms.CharField(
#         widget=forms.TextInput(
#             attrs={'class': 'form-control', 'placeholder': 'Alias'}
#         ),
#         required=False,
#         label='Team Code (optional)',
#     )
#     group_image = forms.FileField(
#         widget=forms.ClearableFileInput(
#             attrs={'class': 'form-control'}
#         ),
#         label='Logo (optional)',
#         required=False
#     )
#     # group_company = forms.ChoiceField(
#     #     widget=forms.Select(
#     #         attrs={'class': 'form-control select2 custom-select2 cmp_select2', 'style': 'width: 100%;'},
#     #     ),
#     #     label='Company',
#     #     choices=[]
#     # )
#     users = forms.MultipleChoiceField(
#         widget=forms.SelectMultiple(
#             attrs={'class': 'form-control select2 custom-select2 assign-users-select-main', 'style': 'width: 100%','placeholder':'Select'},
#         ),
#         label='User(s)',
#         choices=[],
#         required=False
#     )

#     def __init__(self, *args, **kwargs):
#         '''
#         init method to override fields
#         '''
#         super(AddGroupForm, self).__init__(*args, **kwargs)

#         try:
#             rq = kwargs['initial']['request']
#             # print(kwargs['initial']['request']['contributors'])
#             if rq.method == 'POST':
#                 users = kwargs['initial']['request'].POST.getlist('users')
#                 users = list(zip(users, users))
#                 self.fields['users'].choices = users
#         except:
#             pass
