from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# from manage_users.models import CustomUser
# CATEGORIES = (
#     (1, 'Category one'),
#     (2, 'Category two'),
#     (3, 'Category three'),

# )


class BloodSampleImport(models.Model):
    FilePath = models.CharField(max_length=255)
    CreatedBy = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='BloodSampleCreatedBy')
    CreatedAt = models.DateTimeField(auto_now_add=True, editable=False)
    Deleted = models.BooleanField()

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    # def get_absolute_url(self):
    #     return reverse("blood_sample_BloodReportImports_detail", args=(self.pk,))

    # def get_update_url(self):
    #     return reverse("blood_sample_BloodReportImports_update", args=(self.pk,))


class BloodSample(models.Model):
    id = models.BigIntegerField(primary_key=True)
    CohortId = models.CharField(max_length=7)
    Barcode = models.CharField(max_length=10)
    AppointmentId = models.BigIntegerField()
    # Appointment_date = models.DateTimeField()
    SiteNurseEmail = models.CharField(max_length=255)
    ImportId = models.ForeignKey(
        BloodSampleImport, on_delete=models.CASCADE, related_name='BloodSampleImportImportId')
    Comments = models.CharField(max_length=5000)
    CreatedAt = models.DateTimeField()

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    # def get_absolute_url(self):
    #     return reverse("blood_sample_BloodReportRecords_detail", args=(self.pk,))

    # def get_update_url(self):
    #     return reverse("blood_sample_BloodReportRecords_update", args=(self.pk,))


class ManifestImports(models.Model):
    FilePath = models.CharField(max_length=255)
    CreatedBy = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='ManifestRecordCreatedBy')
    CreatedAt = models.DateTimeField(auto_now_add=True, editable=False)
    Deleted = models.BooleanField()

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    # def get_absolute_url(self):
    #     return reverse("blood_sample_ManifestImports_detail", args=(self.pk,))

    # def get_update_url(self):
    #     return reverse("blood_sample_ManifestImports_update", args=(self.pk,))


class ManifestRecords(models.Model):
    Visit = models.CharField(max_length=10)
    ImportId = models.ForeignKey(
        ManifestImports, on_delete=models.CASCADE, related_name='ManifestRecordsImportId')
    Site = models.CharField(max_length=100)
    Room = models.CharField(max_length=20)
    CohortId = models.CharField(max_length=7)
    Barcode = models.CharField(max_length=10)
    CollectionDateTime = models.DateTimeField()

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    # def get_absolute_url(self):
    #     return reverse("blood_sample_ManifestRecords_detail", args=(self.pk,))

    # def get_update_url(self):
    #     return reverse("blood_sample_ManifestRecords_update", args=(self.pk,))


# class RecieptReportChanges(models.Model):

#     # Fields
#     from_value = models.CharField(max_length=500)
#     created = models.DateTimeField(auto_now_add=True, editable=False)
#     field = models.CharField(max_length=50)
#     record_id = models.IntegerField()
#     changed_at = models.DateTimeField()
#     changed_by = models.CharField(max_length=255)
#     last_updated = models.DateTimeField(auto_now=True, editable=False)

#     class Meta:
#         pass

#     def __str__(self):
#         return str(self.pk)

#     def get_absolute_url(self):
#         return reverse("blood_sample_RecieptReportChanges_detail", args=(self.pk,))

#     def get_update_url(self):
#         return reverse("blood_sample_RecieptReportChanges_update", args=(self.pk,))


class RecieptRecords(models.Model):
    Barcode = models.CharField(max_length=10)
    Clinic = models.CharField(max_length=50)
    DateTimeTaken = models.DateTimeField()
    SampleId = models.CharField(max_length=8)
    TissueSubType = models.CharField(max_length=4)
    ReceivedDateTime = models.DateTimeField()
    Volume = models.CharField(max_length=500)
    VolumeUnit = models.CharField(max_length=4)
    Condition = models.CharField(max_length=10)
    # ImportId=

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    # def get_absolute_url(self):
    #     return reverse("blood_sample_RecieptRecords_detail", args=(self.pk,))

    # def get_update_url(self):
    #     return reverse("blood_sample_RecieptRecords_update", args=(self.pk,))


class ProcessedReport(models.Model):
    Barcode = models.CharField(max_length=10)
    ParentId = models.ForeignKey(
        RecieptRecords, on_delete=models.CASCADE, related_name='RecieptRecordsSampleId')
    TissueSubType = models.CharField(max_length=4)
    ReceivedDateTime = models.DateTimeField()
    ProcessedDateTime = models.DateTimeField()
    Volume = models.CharField(max_length=500)
    VolumeUnit = models.CharField(max_length=2)
    NumberOfChildren = models.CharField(max_length=500)
    SiteHeld = models.CharField(max_length=100)
    # ImportId=

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    # def get_absolute_url(self):
    #     return reverse("blood_sample_ProcessedRecords_detail", args=(self.pk,))

    # def get_update_url(self):
    #     return reverse("blood_sample_ProcessedRecords_update", args=(self.pk,))


class ProcessedAliquots(models.Model):
    SampleType = models.CharField(max_length=100)
    Volume = models.CharField(max_length=500)
    VolumeUnit = models.CharField(max_length=2)
    PostProcessingStatus = models.CharField(max_length=500)
    # SampleId

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    # def get_absolute_url(self):
    #     return reverse("blood_sample_Aliquots_detail", args=(self.pk,))

    # def get_update_url(self):
    #     return reverse("blood_sample_Aliquots_update", args=(self.pk,))

# class AliquotChanges(models.Model):

#     # Fields
#     from_value = models.CharField(max_length=30)
#     changed_by = models.CharField(max_length=255)
#     field = models.CharField(max_length=50)
#     created = models.DateTimeField(auto_now_add=True, editable=False)
#     record_id = models.IntegerField()
#     changed_at = models.DateTimeField()
#     last_updated = models.DateTimeField(auto_now=True, editable=False)

#     class Meta:
#         pass

#     def __str__(self):
#         return str(self.pk)

#     def get_absolute_url(self):
#         return reverse("blood_sample_AliquotChanges_detail", args=(self.pk,))

#     def get_update_url(self):
#         return reverse("blood_sample_AliquotChanges_update", args=(self.pk,))


# class ProcessedReportImports(models.Model):

#     # Fields
#     deleted = models.BooleanField()
#     file_type = models.IntegerField(choices=CATEGORIES)
#     created = models.DateTimeField(auto_now_add=True, editable=False)
#     created_by = models.CharField(max_length=100)
#     last_updated = models.DateTimeField(auto_now=True, editable=False)
#     file_path = models.CharField(max_length=255)

#     class Meta:
#         pass

#     def __str__(self):
#         return str(self.pk)

#     def get_absolute_url(self):
#         return reverse("blood_sample_ProcessedReportImports_detail", args=(self.pk,))

#     def get_update_url(self):
#         return reverse("blood_sample_ProcessedReportImports_update", args=(self.pk,))


# class ProcessedChanges(models.Model):

#     # Fields
#     record_id = models.IntegerField()
#     last_updated = models.DateTimeField(auto_now=True, editable=False)
#     changed_by = models.CharField(max_length=255)
#     created = models.DateTimeField(auto_now_add=True, editable=False)
#     field = models.CharField(max_length=50)
#     from_value = models.CharField(max_length=500)
#     changed_at = models.DateTimeField()

#     class Meta:
#         pass

#     def __str__(self):
#         return str(self.pk)

#     def get_absolute_url(self):
#         return reverse("blood_sample_ProcessedChanges_detail", args=(self.pk,))

#     def get_update_url(self):
#         return reverse("blood_sample_ProcessedChanges_update", args=(self.pk,))


# class ManifestChanges(models.Model):

#     # Fields
#     field = models.CharField(max_length=50)
#     changed_by = models.CharField(max_length=255)
#     record_id = models.IntegerField()
#     last_updated = models.DateTimeField(auto_now=True, editable=False)
#     from_value = models.CharField(max_length=500)
#     created = models.DateTimeField(auto_now_add=True, editable=False)
#     changed_at = models.DateTimeField()

#     class Meta:
#         pass

#     def __str__(self):
#         return str(self.pk)

#     def get_absolute_url(self):
#         return reverse("blood_sample_ManifestChanges_detail", args=(self.pk,))

#     def get_update_url(self):
#         return reverse("blood_sample_ManifestChanges_update", args=(self.pk,))
