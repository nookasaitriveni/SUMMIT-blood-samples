from .views import *
from django.urls import path
app_name = 'ManageUsers'

urlpatterns = [
    path('', ManageUsers.as_view(), name='ManageUsers'),

]
