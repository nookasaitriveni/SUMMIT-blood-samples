from django.urls import path
from .views import *

app_name = 'Blood Sample'

urlpatterns = [
    path('', HomeView.as_view(), name='Home'),
    path('upload', UploadView.as_view(),
         name='Upload'),
    path('upload_blood_sample', UploadBloodSampleView.as_view(),
         name='UploadBloodSample'),
    path('upload_manifest', UploadManifestView.as_view(),
         name='UploadManifest'),
    path('upload_receipt', UploadReceiptView.as_view(),
         name='UploadManifest'),
    path('download_blood_sample_csv', DownloadBloodSampleCSVView.as_view(),
         name='DownloadBloodSampleCSV'),
    path('download_blood_sample', DownloadBloodSampleView.as_view(),
         name='DownloadBloodSample'),
    path('filter_options', FilterOptionsView.as_view(),
         name='filterOptions'),
    path('settings_options', SettingsOptionsView.as_view(),
         name='SettingsOptions'),
]
