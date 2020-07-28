from django.shortcuts import render
from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
# from .forms import ResetPasswordForm, SetThePasswordForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
import os
import re
import datetime
import pandas as pd
from django.conf import settings
from .models import *
from django.core.files.storage import FileSystemStorage
import time
import psycopg2
# from datetime import datetime
# Create your views here.


class HomeView(LoginRequiredMixin, View):
    """
    Class for login functionality
    """

    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        """
        Method to get the login form or redirect to Dashboard if session exists
        :param request: request object
        :return: HttpResponse object
        """
        return render(request, self.template_name)


class UploadView(LoginRequiredMixin, View):
    """
    Class for login functionality
    """

    template_name = 'upload.html'

    def get(self, request, *args, **kwargs):
        """
        Method to get the login form or redirect to Dashboard if session exists
        :param request: request object
        :return: HttpResponse object
        """

        if 'prev' in request.GET.get('day', ''):
            day = request.GET.get('day')
            day = day.split('-')[1].split(',')
            day = datetime.datetime.strptime(
                day[0]+','+day[1], '%B %d, %Y')

            days = [(day - datetime.timedelta(days=x))
                    for x in range(4)]
            days.reverse()
        elif 'next' in request.GET.get('day', ''):
            day = request.GET.get('day')
            day = day.split('-')[1].split(',')
            day = datetime.datetime.strptime(
                day[0]+','+day[1], '%B %d, %Y')
            days = [(day + datetime.timedelta(days=x))
                    for x in range(4)]
        else:
            day = request.GET.get(
                'day', datetime.datetime.today().strftime('%B %d, %Y'))
            day = datetime.datetime.today().strftime(
                '%B %d, %Y') if day == 'undefined' else day
            if 'middle' in day:
                firstday = day.split('-')[1]
                firstday = firstday.split(',')
                firstday = datetime.datetime.strptime(
                    firstday[0]+','+firstday[1], '%B %d, %Y')
                days = [(firstday - datetime.timedelta(days=x))
                        for x in range(4)]
                days.reverse()
                current_day = day.split('-')[2]
                current_day = current_day.split(',')
                day = datetime.datetime.strptime(
                    current_day[0]+','+current_day[1], '%B %d, %Y')
            else:
                day = day.split(',')
                day = datetime.datetime.strptime(
                    day[0]+','+day[1], '%B %d, %Y')
                days = [(day - datetime.timedelta(days=x))
                        for x in range(4)]
                days.reverse()
        shownextday = datetime.datetime.today().strftime(
            '%d%b%y') in [i.strftime('%d%b%y') for i in days]
        blood_samples_imported = BloodSampleImport.objects.filter(
            CreatedAt__range=(day.replace(hour=0, minute=0, second=0, microsecond=0), day.replace(
                hour=23, minute=59, second=59, microsecond=0)))
        blood_samples_imported_cnt = 0
        for i in blood_samples_imported:
            blood_samples_imported_cnt += BloodSample.objects.filter(
                ImportId=i).count()
        manifest_imported = ManifestImports.objects.filter(
            CreatedAt__range=(day.replace(hour=0, minute=0, second=0, microsecond=0), day.replace(
                hour=23, minute=59, second=59, microsecond=0)))
        manifest_imported_cnt = 0
        for i in manifest_imported:
            manifest_imported_cnt += ManifestRecords.objects.filter(
                ImportId=i).count()

        return render(request, self.template_name, {
            "days": days,
            "blood_samples_imported": blood_samples_imported_cnt,
            'manifest_imported': manifest_imported_cnt,
            'active': day,
            'shownextday': shownextday
        })


class DownloadBloodSampleView(LoginRequiredMixin, View):
    template_name = 'download-blood-sample.html'

    def get(self, request, *args, **kwargs):
        req = dict(request.GET)
        if len(req) == 0:
            req = dict(Date=[''], Site=[''], Room=[''], Visit=[''])
        if 'Date' in req:
            receipt_barcode = RecieptRecords.objects.all().values('Barcode')
            reciept_records = RecieptRecords.objects.all().values_list('SampleId', 'Clinic')
            if req['Site'] != [''] and req['Room'] != [''] and req['Visit'] != ['']:
                ids = ManifestRecords.objects.filter(
                    Site__in=req['Site'], Barcode__in=receipt_barcode).values_list('id', flat=True)[::1]
                ids += ManifestRecords.objects.filter(
                    Room__in=req['Room'], Barcode__in=receipt_barcode).values_list('id', flat=True)[::1]
                ids += ManifestRecords.objects.filter(
                    Visit__in=req['Visit'], Barcode__in=receipt_barcode).values_list('id', flat=True)[::1]
                manifest_cohort_id = ManifestRecords.objects.filter(
                    pk__in=ids, Barcode__in=receipt_barcode).values_list('CohortId')
                manifest_records = ManifestRecords.objects.filter(
                    pk__in=ids, Barcode__in=receipt_barcode).values_list('Visit', 'Site', 'Room', 'Barcode')
            elif req['Site'] == [''] and req['Room'] != [''] and req['Visit'] != ['']:
                ids = ManifestRecords.objects.filter(
                    Room__in=req['Room'], Barcode__in=receipt_barcode).values_list('id', flat=True)[::1]
                ids += ManifestRecords.objects.filter(
                    Visit__in=req['Visit'], Barcode__in=receipt_barcode).values_list('id', flat=True)[::1]
                manifest_cohort_id = ManifestRecords.objects.filter(
                    pk__in=ids, Barcode__in=receipt_barcode).values_list('CohortId')
                manifest_records = ManifestRecords.objects.filter(
                    pk__in=ids, Barcode__in=receipt_barcode).values_list('Visit', 'Site', 'Room', 'Barcode')
            elif req['Site'] != [''] and req['Room'] == [''] and req['Visit'] != ['']:
                ids = ManifestRecords.objects.filter(
                    Site__in=req['Site'], Barcode__in=receipt_barcode).values_list('id', flat=True)[::1]
                ids += ManifestRecords.objects.filter(
                    Visit__in=req['Visit'], Barcode__in=receipt_barcode).values_list('id', flat=True)[::1]
                manifest_cohort_id = ManifestRecords.objects.filter(
                    pk__in=ids, Barcode__in=receipt_barcode).values_list('CohortId')
                manifest_records = ManifestRecords.objects.filter(
                    pk__in=ids, Barcode__in=receipt_barcode).values_list('Visit', 'Site', 'Room', 'Barcode')
            elif req['Site'] != [''] and req['Room'] != [''] and req['Visit'] == ['']:
                ids = ManifestRecords.objects.filter(
                    Site__in=req['Site'], Barcode__in=receipt_barcode).values_list('id', flat=True)[::1]
                ids += ManifestRecords.objects.filter(
                    Room__in=req['Room'], Barcode__in=receipt_barcode).values_list('id', flat=True)[::1]
                manifest_cohort_id = ManifestRecords.objects.filter(
                    pk__in=ids, Barcode__in=receipt_barcode).values_list('CohortId')
                manifest_records = ManifestRecords.objects.filter(
                    pk__in=ids, Barcode__in=receipt_barcode).values_list('Visit', 'Site', 'Room', 'Barcode')
            elif req['Site'] != [''] and req['Room'] == [''] and req['Visit'] == ['']:
                ids = ManifestRecords.objects.filter(
                    Site__in=req['Site'], Barcode__in=receipt_barcode).values_list('id', flat=True)[::1]
                manifest_cohort_id = ManifestRecords.objects.filter(
                    pk__in=ids, Barcode__in=receipt_barcode).values_list('CohortId')
                manifest_records = ManifestRecords.objects.filter(
                    pk__in=ids, Barcode__in=receipt_barcode).values_list('Visit', 'Site', 'Room', 'Barcode')
            elif req['Site'] == [''] and req['Room'] != [''] and req['Visit'] == ['']:
                ids = ManifestRecords.objects.filter(
                    Room__in=req['Room'], Barcode__in=receipt_barcode).values_list('id', flat=True)[::1]
                manifest_cohort_id = ManifestRecords.objects.filter(
                    pk__in=ids, Barcode__in=receipt_barcode).values_list('CohortId')
                manifest_records = ManifestRecords.objects.filter(
                    pk__in=ids, Barcode__in=receipt_barcode).values_list('Visit', 'Site', 'Room', 'Barcode')
            elif req['Site'] == [''] and req['Room'] == [''] and req['Visit'] != ['']:
                ids = ManifestRecords.objects.filter(
                    Visit__in=req['Visit'], Barcode__in=receipt_barcode).values_list('id', flat=True)[::1]
                manifest_cohort_id = ManifestRecords.objects.filter(
                    pk__in=ids, Barcode__in=receipt_barcode).values_list('CohortId')
                manifest_records = ManifestRecords.objects.filter(
                    pk__in=ids, Barcode__in=receipt_barcode).values_list('Visit', 'Site', 'Room', 'Barcode')
            elif req['Site'] == [''] and req['Room'] == [''] and req['Visit'] == ['']:
                manifest_cohort_id = ManifestRecords.objects.filter(
                    Barcode__in=receipt_barcode).values_list('CohortId')
                manifest_records = ManifestRecords.objects.filter(
                    Barcode__in=receipt_barcode).values_list('Visit', 'Site', 'Room', 'Barcode')
            if req['Date'] != ['']:
                date = req['Date'][0]
                for_ids_dates = BloodSample.objects.filter(
                    CohortId__in=manifest_cohort_id).values_list('id', 'CreatedAt')
                date_ids = [dat[0] for dat in for_ids_dates if dat[1].strftime(
                    "%Y-%m-%d") == date]
                Blood_sample_records = BloodSample.objects.filter(pk__in=date_ids, CohortId__in=manifest_cohort_id).order_by('id')[
                    :20].values_list('id', 'CohortId', 'Comments')
            else:
                Blood_sample_records = BloodSample.objects.filter(CohortId__in=manifest_cohort_id).order_by('id')[
                    :20].values_list('id', 'CohortId', 'Comments')
            Blood_sample_records = list(Blood_sample_records)
            manifest_records = list(manifest_records)
            reciept_records = list(reciept_records)
            for data in range(len(Blood_sample_records)):
                Blood_sample_records[data] = list(Blood_sample_records[data])
                manifest_records[data] = list(manifest_records[data])
                reciept_records[data] = list(reciept_records[data])
                reciept_records[data].append('Whole Blood')
                Blood_sample_records[data] += manifest_records[data]
                Blood_sample_records[data] += reciept_records[data]
                Blood_sample_records[data] = tuple(Blood_sample_records[data])

            Blood_sample_records.insert(0, ('ID', 'COHORT ID', 'COMMENTS', 'VISIT',
                                            'SITE', 'ROOM', 'BARCODE', 'PARTICIPANT ID', 'CLINIC', 'SAMPLE TYPE'))
            context = {'db_data': Blood_sample_records}
        else:
            for key, val in req.items():
                req[key] = val[0].split(',')
            conn = psycopg2.connect(database="summit_blood_samples",
                                    user='postgres', password='root', host='127.0.0.1', port='5432')
            # Creating a cursor object using the cursor() method
            cursor = conn.cursor()
            # Executing an SQL function using the execute() method
            query = """ SELECT """
            headers = []
            for table, columns in req.items():
                for column in columns:
                    if column != '':
                        headers.append(column)
                    if table == 'BloodSample' and column != '':
                        query += "bs.\""+column+"\", "
                    if table == 'Manifest' and column != '':
                        query += "mr.\""+column+"\", "
                    if table == 'Receipt' and column != '':
                        query += "rr.\""+column+"\", "
                    # if table == 'Processed' and column != '':
                    #     query += "pr.\""+column+"\", "
            query = query[:-2]
            query += """ from blood_sample_recieptrecords as rr 
                        left join blood_sample_manifestrecords as mr on rr."Barcode" = mr."Barcode"
                        left join blood_sample_bloodsample as bs on bs."CohortId" = mr."CohortId"
                    """
            # right JOIN blood_sample_processedreport AS pr ON 'rr.Barcode' = 'pr.Barcode' AND 'rr.Barcode' in (SELECT pr."Barcode" FROM blood_sample_processedreport)
            cursor.execute(query)
            # Fetch rows using fetchall() method.
            data = cursor.fetchall()
            # Closing the connection
            conn.close()
            data.insert(0, headers)
            context = {'db_data': data}
        return render(request, self.template_name, context)


class DownloadBloodSampleCSVView(LoginRequiredMixin, View):
    template_name = 'download-blood-sample.html'

    def get(self, request, *args, **kwargs):
        """
        Method to download Blood Sample CSV 
        """
        receipt_barcode = RecieptRecords.objects.all().values('Barcode')
        reciept_records = RecieptRecords.objects.all().values_list('SampleId', 'Clinic')
        manifest_cohort_id = ManifestRecords.objects.filter(
            Barcode__in=receipt_barcode).values_list('CohortId')
        manifest_records = ManifestRecords.objects.filter(
            Barcode__in=receipt_barcode).values_list('Visit', 'Site', 'Room', 'Barcode')
        Blood_sample_records = BloodSample.objects.filter(CohortId__in=manifest_cohort_id).order_by('id')[
            :20].values_list('id', 'CohortId', 'Comments')

        Blood_sample_records = list(Blood_sample_records)
        manifest_records = list(manifest_records)
        reciept_records = list(reciept_records)
        for data in range(len(Blood_sample_records)):
            Blood_sample_records[data] = list(Blood_sample_records[data])
            manifest_records[data] = list(manifest_records[data])
            reciept_records[data] = list(reciept_records[data])
            reciept_records[data].append('Whole Blood')
            Blood_sample_records[data] += manifest_records[data]
            Blood_sample_records[data] += reciept_records[data]
            Blood_sample_records[data] = tuple(Blood_sample_records[data])

        Blood_sample_records.insert(0, ('ID', 'COHORT ID', 'COMMENTS', 'VISIT',
                                        'SITE', 'ROOM', 'BARCODE', 'PARTICIPANT ID', 'CLINIC', 'SAMPLE TYPE'))
        context = {'db_data': Blood_sample_records}
        return render(request, self.template_name, context)


class SettingsOptionsView(LoginRequiredMixin, View):
    template_name = 'settings_bloodsample.html'

    def get(self, request, *args, **kwargs):
        """
        Method to return settings columns columns
        """
        context = {'db_data': 'Hello World'}
        return render(request, self.template_name, context)


class FilterOptionsView(LoginRequiredMixin, View):
    template_name = 'filter_bloodsample.html'

    def get(self, request, *args, **kwargs):
        """
        Method to Return Filter Options
        """
        receipt_barcode = RecieptRecords.objects.all().values_list('Barcode')
        # manifest_cohort_id = ManifestRecords.objects.filter(Barcode__in=receipt_barcode).values('CohortId')
        # dates = BloodSample.objects.filter(CohortId__in=manifest_cohort_id).values('CreatedAt').distinct()
        # dist_dates = []
        # for date in dates:
        #     date_val = list(date.values())[0].strftime("%d-%m-%Y")
        #     if date_val not in dist_dates:
        #         dist_dates.append(date_val)
        visits = ManifestRecords.objects.filter(
            Barcode__in=receipt_barcode).values('Visit').distinct()
        dist_visits = []
        for visit in visits:
            dist_visits += list(visit.values())
        sites = ManifestRecords.objects.filter(
            Barcode__in=receipt_barcode).values('Site').distinct()
        dist_sites = []
        for site in sites:
            dist_sites += list(site.values())
        rooms = ManifestRecords.objects.filter(
            Barcode__in=receipt_barcode).values('Room').distinct()
        dist_rooms = []
        for room in rooms:
            dist_rooms += list(room.values())
        context = {'sites': dist_sites,
                   'visits': dist_visits, 'rooms': dist_rooms}
        print(context)
        return render(request, self.template_name, context)


class UploadBloodSampleView(LoginRequiredMixin, View):
    template_name = 'upload-blood-sample.html'
    blood_sample_confirm_template = 'confirm-blood-sample.html'
    blood_sample_success_template = 'success-blood-sample.html'

    def get(self, request, *args, **kwargs):
        """
        Method to get the login form or redirect to Dashboard if session exists
        :param request: request object
        :return: HttpResponse object
        """
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        test_file = request.FILES.get(u'file')
        df = pd.read_csv(test_file)
        # Fields Check
        if not set(['Id', 'CohortId', 'AppointmentId', 'Barcode', 'User', 'CreatedAt']).issubset(df.columns):
            return JsonResponse({'status': 412, 'message': 'Column names not matching'})
        if BloodSample.objects.count() >= df.shape[0]:
            return JsonResponse({'status': 412, 'message': 'The uploaded file has less number of records compared to database records'})

        try:
            df['CreatedAt'] = df['CreatedAt'].apply(lambda x: datetime.datetime.strptime(
                x, "%Y-%m-%dT%H:%M:%SZ").date())
        except:
            return JsonResponse({'status': 412, 'message': 'CreatedAt column values are not in expected format'})

        # if True in (df['CreatedAt'].map(type) != datetime.datetime).tolist():
        #     return JsonResponse({'status': 412, 'message': 'CollectionDateTime columns value are not in same format'})
        if request.GET.get('confirm', '') == 'True':
            report_ids = BloodSample.objects.values_list('id', flat=True)[
                ::1]
            excel_ids = df.Id.values.tolist()
            new_records = list(set(excel_ids).difference(report_ids))
            df = df[df['Id'].isin(new_records)]

            # Storing file
            fs = FileSystemStorage(
                location=settings.UPLOAD_ROOT+'\\CurrentAppointmentBlood')
            filename = fs.save(test_file.name.split(
                '.')[0]+time.strftime("%d%m%Y-%H%M%S")+'.'+test_file.name.split('.')[1], test_file)
            # End of storing file

            ImportId = BloodSampleImport.objects.create(
                FilePath="CurrentAppointmentBlood\\"+filename,
                CreatedBy=request.user,
                Deleted=False
            )

            model_instances = [
                BloodSample(
                    id=record['Id'],
                    CohortId=record['CohortId'],
                    Barcode=record['Barcode'] if re.match(
                        r"^(E[0-9]{6})+$", record['Barcode']) else "",
                    Comments="" if re.match(
                        r"^(E[0-9]{6})+$", record['Barcode']) else record['Barcode'],
                    AppointmentId=record['AppointmentId'],
                    SiteNurseEmail=record['User'],
                    ImportId=ImportId,
                    CreatedAt=record['CreatedAt'],
                ) for index, record in df.iterrows()
            ]
            BloodSample.objects.bulk_create(model_instances)
            return render(request, self.blood_sample_success_template, {"new_records": len(new_records)})

        report_ids = BloodSample.objects.values_list('id', flat=True)[
            ::1]
        excel_ids = df.Id.values.tolist()
        new_records = set(excel_ids).difference(report_ids)

        # full_filename = os.path.join(settings.BASE_DIR,'uploads', test_file.name)
        # df.to_csv(full_filename, sep='\t', encoding='utf-8')

        # abc = fileData.read()

        return render(request, self.blood_sample_confirm_template, {"new_records": len(new_records)})


class UploadManifestView(LoginRequiredMixin, View):
    template_name = 'upload-manifest.html'
    blood_sample_confirm_template = 'confirm-manifest.html'
    blood_sample_success_template = 'success-manifest.html'

    def get(self, request, *args, **kwargs):
        """
        Method to get the login form or redirect to Dashboard if session exists
        :param request: request object
        :return: HttpResponse object
        """
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        test_file = request.FILES.get(u'file')
        df = pd.read_excel(test_file)

        # File validation
        if not 'Room' in df.iloc[2, 3] and df.iloc[2, 1] != 'Site' and df.iloc[4, 1] != 'Barcode ID' and df.iloc[4, 2] != 'Collection Date & Time' and df.iloc[4, 3] != 'Cohort ID':
            return JsonResponse({'status': 412, 'message': 'Column names not matching'})

        visit = request.POST.get('visit', '')
        room = int(df.iloc[2, 4]) if isinstance(
            df.iloc[2, 4], float) else df.iloc[2, 4]
        site = df.iloc[2, 2]
        df = df.iloc[5:-1, 1:-1].dropna()

        df = df.drop_duplicates()

        df.columns = ['Barcode', 'CollectionDateTime', 'CohortId']

        if True in (df['CollectionDateTime'].map(type) != datetime.datetime).tolist():
            return JsonResponse({'status': 412, 'message': 'CollectionDateTime column values are not in expected format'})
        if True in (df['CohortId'].map(len) != 7).tolist():
            return JsonResponse({'status': 412, 'message': 'CohortId column values length are not in expected format'})
        manifest_db_df = pd.DataFrame(
            list(ManifestRecords.objects.values('Barcode', 'CollectionDateTime', 'CohortId')))

        blood_sample_cohort = BloodSample.objects.values_list('CohortId', flat=True)[
            ::1]
        df_cohort = df['CohortId'].tolist()
        record_not_found_cnt = len(
            set(df_cohort).difference(blood_sample_cohort))
        duplicates_cnt = 0
        record_found_cnt = len(df_cohort)-record_not_found_cnt

        unique_df = df

        if not manifest_db_df.shape == (0, 0):
            # report_ids = manifest_db_df['CohortId'].tolist()

            unique_df = df[~df.Barcode.isin(manifest_db_df.Barcode.values) & ~df.CohortId.isin(
                manifest_db_df.CohortId.values) & ~df.CollectionDateTime.isin(manifest_db_df.CollectionDateTime.values)]
            duplicates_cnt = df.shape[0]-unique_df.shape[0]
            # record_not_found_cnt = len(
            #     set(unique_df['CohortId'].tolist()).difference(report_ids))
            # #
            # record_found_cnt = len(
            #     set(unique_df['CohortId'].tolist()))-record_not_found_cnt

        if request.GET.get('confirm', '') == 'True':
            # Storing file
            fs = FileSystemStorage(
                location=settings.UPLOAD_ROOT+'/Manifests')
            filename = fs.save(test_file.name.split(
                '.')[0]+time.strftime("%d%m%Y-%H%M%S")+'.'+test_file.name.split('.')[1], test_file)
            # End of storing file

            ImportId = ManifestImports.objects.create(
                FilePath="Manifests/"+filename,
                CreatedBy=request.user,
                Deleted=False
            )

            model_instances = [
                ManifestRecords(
                    Visit=visit,
                    ImportId=ImportId,
                    Site=site,
                    Room=room,
                    CohortId=record[2].strip(),
                    Barcode=record[0],
                    CollectionDateTime=record[1]
                ) for index, record in unique_df.iterrows()
            ]
            ManifestRecords.objects.bulk_create(model_instances)
            return render(request, self.blood_sample_success_template, {"duplicates_cnt": duplicates_cnt,
                                                                        "record_not_found_cnt": record_not_found_cnt,
                                                                        "record_found_cnt": record_found_cnt, })

        return render(request, self.blood_sample_confirm_template, {
            "duplicates_cnt": duplicates_cnt,
            "record_not_found_cnt": record_not_found_cnt,
            "record_found_cnt": record_found_cnt,
        })


class UploadReceiptView(LoginRequiredMixin, View):
    template_name = 'upload-receipt.html'
    blood_sample_confirm_template = 'confirm-receipt.html'
    blood_sample_success_template = 'success-receipt.html'

    def get(self, request, *args, **kwargs):
        """
        Method to get the login form or redirect to Dashboard if session exists
        :param request: request object
        :return: HttpResponse object
        """
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        test_file = request.FILES.get(u'file')
        df = pd.read_excel(test_file)

        # File validation
        if not 'Room' in df.iloc[2, 3] and df.iloc[2, 1] != 'Site' and df.iloc[4, 1] != 'Barcode ID' and df.iloc[4, 2] != 'Collection Date & Time' and df.iloc[4, 3] != 'Cohort ID':
            return JsonResponse({'status': 412, 'message': 'Column names not matching'})

        visit = request.POST.get('visit', '')
        room = int(df.iloc[2, 4]) if isinstance(
            df.iloc[2, 4], float) else df.iloc[2, 4]
        site = df.iloc[2, 2]
        df = df.iloc[5:-1, 1:-1].dropna()

        df = df.drop_duplicates()

        df.columns = ['Barcode', 'CollectionDateTime', 'CohortId']

        if True in (df['CollectionDateTime'].map(type) != datetime.datetime).tolist():
            return JsonResponse({'status': 412, 'message': 'CollectionDateTime column values are not in expected format'})
        if True in (df['CohortId'].map(len) != 7).tolist():
            return JsonResponse({'status': 412, 'message': 'CohortId column values length are not in expected format'})
        manifest_db_df = pd.DataFrame(
            list(ManifestRecords.objects.values('Barcode', 'CollectionDateTime', 'CohortId')))

        blood_sample_cohort = BloodSample.objects.values_list('CohortId', flat=True)[
            ::1]
        df_cohort = df['CohortId'].tolist()
        record_not_found_cnt = len(
            set(df_cohort).difference(blood_sample_cohort))
        duplicates_cnt = 0
        record_found_cnt = len(df_cohort)-record_not_found_cnt

        unique_df = df

        if not manifest_db_df.shape == (0, 0):
            # report_ids = manifest_db_df['CohortId'].tolist()

            unique_df = df[~df.Barcode.isin(manifest_db_df.Barcode.values) & ~df.CohortId.isin(
                manifest_db_df.CohortId.values) & ~df.CollectionDateTime.isin(manifest_db_df.CollectionDateTime.values)]
            duplicates_cnt = df.shape[0]-unique_df.shape[0]
            # record_not_found_cnt = len(
            #     set(unique_df['CohortId'].tolist()).difference(report_ids))
            # #
            # record_found_cnt = len(
            #     set(unique_df['CohortId'].tolist()))-record_not_found_cnt

        if request.GET.get('confirm', '') == 'True':
            # Storing file
            fs = FileSystemStorage(
                location=settings.UPLOAD_ROOT+'\\Manifests')
            filename = fs.save(test_file.name.split(
                '.')[0]+time.strftime("%d%m%Y-%H%M%S")+'.'+test_file.name.split('.')[1], test_file)
            # End of storing file

            ImportId = ManifestImports.objects.create(
                FilePath="Manifests\\"+filename,
                CreatedBy=request.user,
                Deleted=False
            )

            model_instances = [
                ManifestRecords(
                    Visit=visit,
                    ImportId=ImportId,
                    Site=site,
                    Room=room,
                    CohortId=record[2].strip(),
                    Barcode=record[0],
                    CollectionDateTime=record[1]
                ) for index, record in unique_df.iterrows()
            ]
            ManifestRecords.objects.bulk_create(model_instances)
            return render(request, self.blood_sample_success_template, {"duplicates_cnt": duplicates_cnt,
                                                                        "record_not_found_cnt": record_not_found_cnt,
                                                                        "record_found_cnt": record_found_cnt, })

        return render(request, self.blood_sample_confirm_template, {
            "duplicates_cnt": duplicates_cnt,
            "record_not_found_cnt": record_not_found_cnt,
            "record_found_cnt": record_found_cnt,
        })
