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
    path('upload_processed', UploadProcessedView.as_view(),
         name='UploadProcessed'),
    path('download_blood_sample', DownloadBloodSampleView.as_view(),
         name='DownloadBloodSample'),
    path('filter_options', FilterOptionsView.as_view(),
         name='filterOptions'),
    path('settings_options', SettingsOptionsView.as_view(),
         name='SettingsOptions'),
    path('download_aliquots', DownloadAliquotsView.as_view(),
         name='DownloadAliquots'),
    path('filter_aliquots', FilterAliquotsView.as_view(),
         name='FilterAliquots'),
    path('settings_aliquots', SettingsAliquotsView.as_view(),
         name='SettingsAliquots'),
    path('review', ReviewView.as_view(),
         name='Review'),
    path('edit_blood_sample', EditBloodSampleView.as_view(),
         name='EditBloodSample'),

]
