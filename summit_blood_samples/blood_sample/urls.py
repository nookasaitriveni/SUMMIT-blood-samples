from django.urls import path
from .views import *

app_name = 'Blood Sample'

urlpatterns = [
    path('', HomeView.as_view(), name='Home'),

]
