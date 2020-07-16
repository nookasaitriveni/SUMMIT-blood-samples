# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string
# from django.conf import settings
# from django.utils.html import strip_tags
# from Login.models import UserHeadMap, UserDetails
# from Company.models import GroupDetails
# from django.core.exceptions import ObjectDoesNotExist
# from django.contrib.auth.models import User
# # from OnPointSettings.models import Settings
# from Login.models import UserHeadMap

# import threading
# import time


# def threaded(func):
#     def wrap(*args, **kwargs):
#         thread = threading.Thread(target=func, args=args, kwargs=kwargs)
#         thread.start()
#         return thread
#     return wrap

# class SendMail():
#     template_user = 'mail/default.html'
#     template_boss = 'mail/default_boss.html'
#     template_private = 'mail/default_private.html'

#     @classmethod
#     def mailTemplate(cls, template_user=None, template_boss=None):
#         if template_user is not None:
#             cls.template_user = template_user
#         if template_boss is not None:
#             cls.template_boss = template_boss
#         return cls

#     def send_mail(self, request, *args, **kwargs):
#         subject = kwargs['subject']
#         context = {
#             'type': kwargs['type'],
#             'objtitle': kwargs['objtitle'],
#             'created_or_updated': kwargs['created_or_updated'],
#             'boss': kwargs['boss'] if 'boss' in kwargs else None
#         }
#         body = render_to_string(kwargs['template'], context, request)
#         html_content = body
#         text_content = strip_tags(body)
#         frommail = settings.EMAIL_FROM
#         tomail = kwargs['email'] if isinstance(kwargs['email'], list) else [kwargs['email']]
#         email = EmailMultiAlternatives(
#             subject,
#             text_content,
#             frommail,
#             tomail
#         )
#         email.attach_alternative(html_content, 'text/html')
#         email.send()

#     @threaded
#     def sendTheMail(self, request, *args, **kwargs):
#         return
#         try:
#             kwargs['template'] = self.template_user
#             kwargs['email'] = request.user.email
#             self.send_mail(request, *args, **kwargs)################confirmation mail
#             chk = ['private', 'public']
#             for i in chk:
#                 if i in kwargs:
#                     continue
#                 else:
#                     kwargs[i] = False
#             kwargs['template'] = self.template_boss
#             if kwargs['private']:
#                 kwargs['public'] = False
#                 kwargs['template'] = self.template_private
#                 self.sendThePrivateMail(request, *args, **kwargs)
#                 kwargs['template'] = self.template_boss
#                 self.send_mail_to_boss(request, *args, **kwargs)
#             elif kwargs['public']:
#                 self.send_mail_to_boss(request, *args, **kwargs)
#             if kwargs['type'].lower() == 'key result':
#                 fld = [('owner', 'mail/default_cascade.html'), ('updater', 'mail/default_contributors.html')]
#                 for i, t in fld:
#                     kwargs['field'] = i
#                     kwargs['template'] = t
#                     self.sendThePrivateMail(request, *args, **kwargs)
#             if kwargs['type'].lower() == 'initiative':
#                 fld = [('owner', 'mail/default_cascade.html'), ('contributors', 'mail/default_contributors.html')]
#                 for i, t in fld:
#                     kwargs['field'] = i
#                     kwargs['template'] = t
#                     self.sendThePrivateMail(request, *args, **kwargs)
#         except Exception as e:
#             pass

#     def send_mail_to_boss(self, request, *args, **kwargs):
#         try:
#             boss = UserHeadMap.objects.filter(user=request.user)
#             if boss.exists():
#                 for i in boss:
#                     boss_boss = UserHeadMap.objects.filter(user=i.head)
#                     for j in boss_boss:
#                         if isinstance(j.head, User):
#                             kwargs['email'] = j.head.email
#                             kwargs['section'] = 'public' if kwargs['public'] else 'private'
#                             kwargs['boss'] = j.head
#                             if self.checkForEmailNotification(request, *args, **kwargs):
#                                 self.send_mail(request, *args, **kwargs)
#                     if isinstance(i.head, User):
#                         kwargs['email'] = i.head.email
#                         kwargs['section'] = 'public' if kwargs['public'] else 'private'
#                         kwargs['boss'] = i.head
#                         if self.checkForEmailNotification(request, *args, **kwargs):
#                             self.send_mail(request, *args, **kwargs)
#         except Exception as e:
#             pass

#     def checkForEmailNotification(self, request, *args, **kwargs):
#         try:
#             if kwargs['section'].lower() == 'private':
#                 onpoint_settings = Settings.objects.get(user=kwargs['boss'], private=True)
#             else:
#                 onpoint_settings = Settings.objects.get(user=kwargs['boss'], public=True)
#             return True
#         except Exception as e:
#             return False


#     @threaded
#     def sendThePrivateMail(self, request, *args, **kwargs):
#         # kwargs['template'] = self.template_user
#         kwargs['section'] = 'public'
#         try:
#             if 'field' in kwargs:
#                 fld = kwargs['field']
#             else:
#                 fld = 'viewable'
#             for i in request.POST.getlist(fld):
#                 if i.startswith('u_'):
#                     kwargs['email'] = User.objects.get(pk=int(i[2:])).email
#                     if fld == 'viewable':
#                         kwargs['section'] = 'private'
#                     kwargs['boss'] = User.objects.get(pk=int(i[2:]))
#                     if self.checkForEmailNotification(request, *args, **kwargs):
#                         self.send_mail(request, *args, **kwargs)
#                 elif i.startswith('g_'):
#                     users = UserDetails.groupDetails.through.objects.filter(groupdetails=GroupDetails.objects.get(pk=int(i[2:])))
#                     kwargs['email'] = [x.userdetails.user.email for x in users]
#                     if fld == 'viewable':
#                         kwargs['section'] = 'private'
#                     for j in kwargs['email']:
#                         kwargs['boss'] = User.objects.get(email__iexact=j)
#                         if self.checkForEmailNotification(request, *args, **kwargs):
#                             self.send_mail(request, *args, **kwargs)
#                 else:
#                     try:
#                         kwargs['email'] = User.objects.get(pk=int(i)).email
#                         if fld == 'viewable':
#                             kwargs['section'] = 'private'
#                         kwargs['boss'] = User.objects.get(pk=int(i))
#                         if self.checkForEmailNotification(request, *args, **kwargs):
#                             self.send_mail(request, *args, **kwargs)
#                     except:
#                         pass
#         except Exception as e:
#             pass
