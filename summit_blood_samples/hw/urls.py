from .views import *
from django.urls import path
app_name = 'hw'

urlpatterns = [
    path('', hw.as_view(), name='hw'),

]

