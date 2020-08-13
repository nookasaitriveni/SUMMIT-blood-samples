from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class BloodSampleImport(models.Model):
    FilePath = models.CharField(max_length=500)
    OriginalFileName = models.CharField(max_length=500)
    CreatedBy = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='BloodSampleCreatedBy')
    CreatedAt = models.DateTimeField()
    Deleted = models.BooleanField()
    Reviewed = models.BooleanField()

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)


STATECHOICE = [
    (0, 'ACTIVE'),
    (1, 'UNABLE_TO_DRAW'),
    (2, 'UNABLE_TO_PROCESS'),
    (3, 'PROCESSED_ON_TIME'),
    (4, 'PROCESSED_NOT_ON_TIME'),
]


class BloodSample(models.Model):
    id = models.BigIntegerField(primary_key=True)
    CohortId = models.CharField(max_length=7)
    Barcode = models.CharField(max_length=10)
    AppointmentId = models.BigIntegerField()
    SiteNurseEmail = models.CharField(max_length=255)
    ImportId = models.ForeignKey(
        BloodSampleImport, on_delete=models.CASCADE, related_name='BloodSampleImportImportId')
    Comments = models.CharField(max_length=5000)
    CreatedAt = models.DateTimeField()
    State = models.CharField(
        max_length=1,
        choices=STATECHOICE,
        default=0
    )

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def state_verbose(self):
        return '' if self.State == '' else dict(STATECHOICE)[int(self.State)]


class BloodSampleChanges(models.Model):
    Field = models.CharField(max_length=50)
    FromValue = models.CharField(max_length=5000)
    ChangedBy = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='BloodSampleChangedBy')
    ChangedAt = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)


class ManifestImports(models.Model):
    FilePath = models.CharField(max_length=500)
    OriginalFileName = models.CharField(max_length=500)
    CreatedBy = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='ManifestRecordCreatedBy')
    CreatedAt = models.DateTimeField()
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
#     created = models.DateTimeField(auto_now=True, editable=False)
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


class ReceiptImports(models.Model):
    FilePath = models.CharField(max_length=500)
    OriginalFileName = models.CharField(max_length=500)
    CreatedBy = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='RecieptRecordsCreatedBy')
    CreatedAt = models.DateTimeField()
    Deleted = models.BooleanField()

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)


class ReceiptRecords(models.Model):
    Barcode = models.CharField(max_length=10)
    Clinic = models.CharField(max_length=50)
    DateTimeTaken = models.DateTimeField()
    SampleId = models.CharField(max_length=8)
    TissueSubType = models.CharField(max_length=4)
    ReceivedDateTime = models.DateTimeField()
    Volume = models.CharField(max_length=500)
    VolumeUnit = models.CharField(max_length=4)
    Condition = models.CharField(max_length=500)
    ImportId = models.ForeignKey(
        ReceiptImports, on_delete=models.CASCADE, related_name='RecieptRecordsImportId')

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    # def get_absolute_url(self):
    #     return reverse("blood_sample_RecieptRecords_detail", args=(self.pk,))

    # def get_update_url(self):
    #     return reverse("blood_sample_RecieptRecords_update", args=(self.pk,))


class ProcessedImports(models.Model):
    FilePath = models.CharField(max_length=500)
    OriginalFileName = models.CharField(max_length=500)
    CreatedBy = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='ProcessedImportsCreatedBy')
    CreatedAt = models.DateTimeField()
    Deleted = models.BooleanField()

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)


class ProcessedReport(models.Model):
    Barcode = models.CharField(max_length=10)
    ParentId = models.CharField(max_length=8)
    TissueSubType = models.CharField(max_length=4)
    ReceivedDateTime = models.DateTimeField(null=True)
    ProcessedDateTime = models.DateTimeField(null=True)
    Volume = models.CharField(max_length=500)
    VolumeUnit = models.CharField(max_length=2)
    NumberOfChildren = models.CharField(max_length=500)
    ImportId = models.ForeignKey(
        ProcessedImports, on_delete=models.CASCADE, related_name='ProcessedImportsImportId')

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    # def get_absolute_url(self):
    #     return reverse("blood_sample_ProcessedRecords_detail", args=(self.pk,))

    # def get_update_url(self):
    #     return reverse("blood_sample_ProcessedRecords_update", args=(self.pk,))


PROCESSING_STATUS = [
    (0, 'Complete'),
    (1, 'Partial'),
    (2, 'Empty'),
    (3, 'Destroyed'),
    (4, 'Not applicable'),
]


class ProcessedAliquots(models.Model):
    SampleType = models.CharField(max_length=100)
    Volume = models.CharField(max_length=500)
    VolumeUnit = models.CharField(max_length=2)
    PostProcessingStatus = models.CharField(
        max_length=1,
        choices=PROCESSING_STATUS,
        default=0
    )
    SampleId = models.CharField(max_length=8)
    SampleIdFile = models.CharField(max_length=500)

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
#     created = models.DateTimeField(auto_now=True, editable=False)
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
#     created = models.DateTimeField(auto_now=True, editable=False)
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
#     created = models.DateTimeField(auto_now=True, editable=False)
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
#     created = models.DateTimeField(auto_now=True, editable=False)
#     changed_at = models.DateTimeField()

#     class Meta:
#         pass

#     def __str__(self):
#         return str(self.pk)

#     def get_absolute_url(self):
#         return reverse("blood_sample_ManifestChanges_detail", args=(self.pk,))

#     def get_update_url(self):
#         return reverse("blood_sample_ManifestChanges_update", args=(self.pk,))
