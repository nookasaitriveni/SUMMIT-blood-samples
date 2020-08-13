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
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
import os
import math
import re
import datetime
import pandas as pd
from .models import *
from manage_users.models import *
from django.core.files.storage import FileSystemStorage
import time

import psycopg2
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.db import connection
cursor = connection.cursor()
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
        day, days = self.get_dayformated_and_days(request)
        shownextday = datetime.datetime.today().strftime(
            '%d%b%y') in [i.strftime('%d%b%y') for i in days]

        blood_samples_loaded = BloodSample.objects.filter(
            CreatedAt__range=(day.replace(hour=0, minute=0, second=0, microsecond=0), day.replace(
                hour=23, minute=59, second=59, microsecond=0)))

        blood_samples_imported = BloodSampleImport.objects.filter(
            CreatedAt__range=(day.replace(hour=0, minute=0, second=0, microsecond=0), day.replace(
                hour=23, minute=59, second=59, microsecond=0)))
        blood_samples_imported_cnt = BloodSample.objects.filter(
            ImportId__in=blood_samples_imported.values_list('id', flat=True)[::1]).count()
        try:
            reviewed = blood_samples_imported.last().Reviewed
        except:
            reviewed = False

        manifest_imported = ManifestImports.objects.filter(
            CreatedAt__range=(day.replace(hour=0, minute=0, second=0, microsecond=0), day.replace(
                hour=23, minute=59, second=59, microsecond=0)))
        no_of_files_uploaded = manifest_imported.count()
        manifest_imported_cnt = ManifestRecords.objects.filter(
            ImportId__in=manifest_imported.values_list('id', flat=True)[::1]).count()

        manifest_loaded = ManifestRecords.objects.filter(
            CollectionDateTime__range=(day.replace(hour=0, minute=0, second=0, microsecond=0), day.replace(
                hour=23, minute=59, second=59, microsecond=0)))

        receipt_imported = ReceiptImports.objects.filter(
            CreatedAt__range=(day.replace(hour=0, minute=0, second=0, microsecond=0), day.replace(
                hour=23, minute=59, second=59, microsecond=0)))
        receipt_imported_cnt = ReceiptRecords.objects.filter(
            ImportId__in=receipt_imported.values_list('id', flat=True)[::1]).count()

        receipt_loaded = ReceiptRecords.objects.filter(
            DateTimeTaken__range=(day.replace(hour=0, minute=0, second=0, microsecond=0), day.replace(
                hour=23, minute=59, second=59, microsecond=0)))

        processed_imported = ProcessedImports.objects.filter(
            CreatedAt__range=(day.replace(hour=0, minute=0, second=0, microsecond=0), day.replace(
                hour=23, minute=59, second=59, microsecond=0)))
        processed_imported_cnt = ProcessedReport.objects.filter(
            ImportId__in=processed_imported.values_list('id', flat=True)[::1]).count()

        return render(request, self.template_name, {
            "days": days,
            "blood_samples_cnt": blood_samples_loaded.count(),
            "blood_samples_imported": blood_samples_imported_cnt,
            'manifest_imported': manifest_imported_cnt,
            'manifest_loaded_count': manifest_loaded.count(),
            'receipt_imported': receipt_imported_cnt,
            "receipt_loaded_cnt": receipt_loaded.count(),
            'processed_imported': processed_imported_cnt,
            'active': day,
            'shownextday': shownextday,
            'reviewed': reviewed,
            'class': 'uploadDay',
            'no_of_files_uploaded': no_of_files_uploaded,
        })

    def get_dayformated_and_days(self, request):
        if 'prev' in request.GET.get('day', ''):
            day = request.GET.get('day')
            day = day.split('-')[1].split(',')
            try:
                day = datetime.datetime.strptime(
                    day[0]+','+day[1], '%B %d, %Y')
            except:
                day = datetime.datetime.strptime(
                    day[0].split(' ')[0][:3]+' '+day[0].split(' ')[1]+','+day[1], '%b %d, %Y')

            days = [(day - datetime.timedelta(days=x))
                    for x in range(4)]
            days.reverse()
        elif 'next' in request.GET.get('day', ''):
            day = request.GET.get('day')
            day = day.split('-')[1].split(',')
            try:
                day = datetime.datetime.strptime(
                    day[0]+','+day[1], '%B %d, %Y')
            except:
                day = datetime.datetime.strptime(
                    day[0].split(' ')[0][:3]+' '+day[0].split(' ')[1]+','+day[1], '%b %d, %Y')

            days = [(day + datetime.timedelta(days=x))
                    for x in range(4)]
        else:
            try:
                day = request.GET.get(
                    'day', datetime.datetime.today().strftime('%B %d, %Y'))
            except:
                day = request.GET.get(
                    'day', datetime.datetime.today().strftime('%b. %d, %Y'))
            try:
                day = datetime.datetime.today().strftime(
                    '%B %d, %Y') if day == 'undefined' else day
            except:
                day = datetime.datetime.today().strftime(
                    '%b. %d, %Y') if day == 'undefined' else day
            if 'middle' in day:
                firstday = day.split('-')[1]
                firstday = firstday.split(',')
                try:
                    firstday = datetime.datetime.strptime(
                        firstday[0]+','+firstday[1], '%B %d, %Y')
                except:
                    firstday = datetime.datetime.strptime(
                        firstday[0].split(' ')[0][:3]+' '+firstday[0].split(' ')[1]+','+firstday[1], '%b %d, %Y')
                days = [(firstday - datetime.timedelta(days=x))
                        for x in range(4)]
                days.reverse()
                current_day = day.split('-')[2]
                current_day = current_day.split(',')
                try:
                    day = datetime.datetime.strptime(
                        current_day[0]+','+current_day[1], '%B %d, %Y')
                except:
                    day = datetime.datetime.strptime(
                        current_day[0].split(' ')[0][:3]+' '+current_day[0].split(' ')[1]+','+current_day[1], '%b %d, %Y')
            else:
                day = day.split(',')
                try:
                    day = datetime.datetime.strptime(
                        day[0]+','+day[1], '%B %d, %Y')
                except:
                    day = datetime.datetime.strptime(
                        day[0].split(' ')[0][:3]+' '+day[0].split(' ')[1]+','+day[1], '%b %d, %Y')
                days = [(day - datetime.timedelta(days=x))
                        for x in range(4)]
                days.reverse()
        return day, days


class DownloadBloodSampleView(LoginRequiredMixin, View):
    template_name = 'download-blood-sample.html'
    download_blood_table_template = 'download-blood-sample-table.html'

    def get(self, request, *args, **kwargs):
        request_data = dict(request.GET)
        csv = False
        if 'csv' in request_data:
            csv = True
        if 'settings' not in request_data:
            settings_options = dict(BS=request_data['BloodSample'], MR=request_data['Manifest'],
                                    RR=request_data['Receipt'], PR=request_data['Processed'])
            for table, columns in settings_options.items():
                for column in columns:
                    settings_options[table] = column.split(',')
        else:
            settings_options = eval(request_data['settings'][0])
        if 'filters' not in request_data:
            filter_options = dict(DF=request_data['DateFrom'], DT=request_data['DateTo'], Site=request_data['Site'],
                                  Room=request_data['Room'], Visit=request_data['Visit'], State=request_data['State'])
        else:
            filter_options = eval(request_data['filters'][0])
        # Creating a cursor object using the cursor() method
        settings = settings_options
        bs_len = len(settings['BS'])
        if bs_len == 1 and settings['BS'][0] == '':
            bs_len = 0
        mr_len = len(settings['MR'])
        if mr_len == 1 and settings['MR'][0] == '':
            mr_len = 0
        rr_len = len(settings['RR'])
        if rr_len == 1 and settings['RR'][0] == '':
            rr_len = 0
        pr_len = len(settings['PR'])
        if pr_len == 1 and settings['PR'][0] == '':
            pr_len = 0
        # Executing an SQL function using the execute() method
        query = """ SELECT """
        headers = []
        for table, columns in settings.items():
            for column in columns:
                if column != '':
                    headers.append(column)
                if table == 'BS' and column != '':
                    query += "bs.\""+column+"\", "
                if table == 'MR' and column != '':
                    query += "mr.\""+column+"\", "
                if table == 'RR' and column != '':
                    query += "rr.\""+column+"\", "
                if table == 'PR' and column != '':
                    query += "pr.\""+column+"\", "
        query = query[:-2]
        query += """from blood_sample_processedreport as pr
                    right join blood_sample_receiptrecords as rr on pr."ParentId" = rr."SampleId"
                    right join blood_sample_manifestrecords as mr on rr."Barcode" = mr."Barcode"
                    right join blood_sample_bloodsample as bs on bs."CohortId" = mr."CohortId"
                """
        state_status = {'0': 'ACTIVE', '1': 'UNABLE_TO_DRAW', '2': 'UNABLE_TO_PROCESS',
                        '3': 'PROCESSED_ON_TIME', '4': 'PROCESSED_NOT_ON_TIME'}
        extra = ' WHERE '
        date_start = filter_options['DF'][0]
        date_end = filter_options['DT'][0]
        # processed_parentid = ProcessedReport.objects.all().values('ParentId')
        # receipt_barcode = ReceiptRecords.objects.filter(
        #     SampleId__in=processed_parentid).values('Barcode')
        # manifest_cohort_id = ManifestRecords.objects.filter(
        #     Barcode__in=receipt_barcode).values('CohortId')
        date_id = BloodSample.objects.all().values_list('id', 'CreatedAt')
        dateids = []
        if date_start == '':
            date_start = '1900-01-01'
        if date_end == '':
            date_end = datetime.datetime.now().strftime("%Y-%m-%d")
        dateids = [date[0] for date in date_id if date_start <=
                   date[1].strftime("%Y-%m-%d") <= date_end]
        for filt, value in filter_options.items():
            if filt == 'Site' and value[0] != '':
                extra += "mr.\"Site\"='" + value[0]+"' AND "
            if filt == 'Room' and value[0] != '':
                extra += "mr.\"Room\"='" + value[0]+"' AND "
            if filt == 'Visit' and value[0] != '':
                extra += "mr.\"Visit\"='" + value[0]+"' AND "
            if filt == 'State' and value[0] != '':
                val = list(state_status.keys())[
                    list(state_status.values()).index(value[0])]
                extra += "bs.\"State\"='" + val+"' AND "
        if len(dateids) != 1:
            extra += "bs.\"id\" in " + str(tuple(dateids)) + " AND "
        elif len(dateids) == 1:
            extra += "bs.\"id\" in " + '(%s)' % dateids[0] + " AND "
        extra = extra[0:-4]
        if extra != ' WH':
            query += extra
        query += ' order by bs.id, mr.\"Barcode\"'

        cursor.execute(query)
        # Fetch rows using fetchall() method.
        data = cursor.fetchall()

        state_status = {'0': 'ACTIVE', '1': 'UNABLE_TO_DRAW', '2': 'UNABLE_TO_PROCESS',
                        '3': 'PROCESSED_ON_TIME', '4': 'PROCESSED_NOT_ON_TIME'}
        if 'State' in settings['BS']:
            ind = headers.index('State')
            for row in range(len(data)):
                data[row] = list(data[row])
                data[row][ind] = state_status[data[row][ind]]
                data[row] = tuple(data[row])
        row_headers = {'CohortId': 'Cohort id', 'AppointmentId': 'Appointment id', 'SiteNurseEmail': 'Site Nurse Email',
                       'CreatedAt': 'Appointment date', 'CollectionDateTime': 'Collection Date Time', 'DateTimeTaken': 'Date Time Taken',
                       'SampleId': 'Sample id', 'TissueSubType': 'Tissue Sub Type', 'ReceivedDateTime': 'Received Date Time',
                       'VolumeUnit': 'Volume Unit', 'ParentId': 'Parent id', 'ProcessedDateTime': 'Processed Date Time', 'NumberOfChildren': 'Number Of Children', 'id': 'Id'}
        for i in range(len(headers)):
            if headers[i] in row_headers:
                headers[i] = row_headers[headers[i]]

        #data.insert(0, headers)
        if csv and len(data) != 0:
            response = HttpResponse(content_type='text/csv')
            data.insert(0, tuple(headers))
            from django.template.loader import get_template
            template = get_template('csv_download.txt')
            csv_data = data
            # for i in range(len(csv_data)):
            #     for j in range(len(csv_data[i])):
            #         if type(csv_data[i][j]) is datetime.datetime:
            #             print(str(csv_data[i][j]), '------------------------ BEFORE')
            #             csv_data[i] = list(csv_data[i])
            #             csv_data[i][j] = csv_data[i][j].strftime("%c")
            #             csv_data[i] = tuple(csv_data[i])
            #             print(csv_data[i][j], '------------------------ AFTER')
            # csv_data[i] = str(csv_data[i])[1:-1]
            c = {
                'data': csv_data,
            }
            filename = 'BloodSamples_' + datetime.datetime.now().strftime("%Y%m%d%H%M%S")+'.csv'
            content = "attachment; filename=%s" % (filename)
            response['Content-Disposition'] = content
            response.write(template.render(c))
            return response
        if len(data) == 0:
            data = 'No Records to Display'
        page = int(request.GET.get('page', 1))
        table = request.GET.get('table', 'False')
        from django.conf import settings as django_settings
        total_pages = math.ceil(len(data)/django_settings.ITEMS_PER_PAGE)
        items_per_page = django_settings.ITEMS_PER_PAGE
        record_start = (page-1) * items_per_page
        record_end = page * items_per_page
        if table == "True":
            return render(request, self.download_blood_table_template, {
                "objects": [headers]+data[record_start:record_end],
                "current_page": page,
                "total_pages": total_pages,
                'db_data': data,
                'bs_len': bs_len,
                'mr_len': mr_len, 'rr_len': rr_len,
                'pr_len': pr_len, 'settings': settings_options, 'filters': filter_options
            })
        # headers
        context = {
            "current_page": page,
            "total_pages": total_pages,
            'db_data': data,
            'bs_len': bs_len,
            'mr_len': mr_len, 'rr_len': rr_len,
            'pr_len': pr_len, 'settings': settings_options, 'filters': filter_options}
        return render(request, self.template_name, context)


class DownloadAliquotsView(LoginRequiredMixin, View):
    template_name = 'download-aliquots.html'

    def get(self, request, *args, **kwargs):
        get_data = dict(request.GET)
        if len(get_data) == 0:
            get_data = {'Sample': [''], 'Volume': [''], 'Status': ['']}
        if 'Sample' in get_data:
            if get_data['Sample'] != [''] and get_data['Volume'] != [''] and get_data['Status'] != ['']:
                ids = ProcessedAliquots.objects.filter(
                    SampleType__in=get_data['Sample']).values_list('id', flat=True)[::1]
                ids += ProcessedAliquots.objects.filter(
                    Volume__in=get_data['Volume']).values_list('id', flat=True)[::1]
                ids += ProcessedAliquots.objects.filter(
                    PostProcessingStatus__in=get_data['Status']).values_list('id', flat=True)[::1]
                aliquots_data = ProcessedAliquots.objects.filter(pk__in=ids).values_list(
                    'SampleType', 'Volume', 'VolumeUnit', 'PostProcessingStatus')
            elif get_data['Sample'] == [''] and get_data['Volume'] != [''] and get_data['Status'] != ['']:
                ids = ProcessedAliquots.objects.filter(
                    Volume__in=get_data['Volume']).values_list('id', flat=True)[::1]
                ids += ProcessedAliquots.objects.filter(
                    PostProcessingStatus__in=get_data['Status']).values_list('id', flat=True)[::1]
                aliquots_data = ProcessedAliquots.objects.filter(pk__in=ids).values_list(
                    'SampleType', 'Volume', 'VolumeUnit', 'PostProcessingStatus')
            elif get_data['Sample'] != [''] and get_data['Volume'] == [''] and get_data['Status'] != ['']:
                ids = ProcessedAliquots.objects.filter(
                    SampleType__in=get_data['Sample']).values_list('id', flat=True)[::1]
                ids += ProcessedAliquots.objects.filter(
                    PostProcessingStatus__in=get_data['Status']).values_list('id', flat=True)[::1]
                aliquots_data = ProcessedAliquots.objects.filter(pk__in=ids).values_list(
                    'SampleType', 'Volume', 'VolumeUnit', 'PostProcessingStatus')
            elif get_data['Sample'] != [''] and get_data['Volume'] != [''] and get_data['Status'] == ['']:
                ids = ProcessedAliquots.objects.filter(
                    SampleType__in=get_data['Sample']).values_list('id', flat=True)[::1]
                ids += ProcessedAliquots.objects.filter(
                    Volume__in=get_data['Volume']).values_list('id', flat=True)[::1]
                aliquots_data = ProcessedAliquots.objects.filter(pk__in=ids).values_list(
                    'SampleType', 'Volume', 'VolumeUnit', 'PostProcessingStatus')
            elif get_data['Sample'] != [''] and get_data['Volume'] == [''] and get_data['Status'] == ['']:
                ids = ProcessedAliquots.objects.filter(
                    SampleType__in=get_data['Sample']).values_list('id', flat=True)[::1]
                aliquots_data = ProcessedAliquots.objects.filter(pk__in=ids).values_list(
                    'SampleType', 'Volume', 'VolumeUnit', 'PostProcessingStatus')
            elif get_data['Sample'] == [''] and get_data['Volume'] != [''] and get_data['Status'] == ['']:
                ids = ProcessedAliquots.objects.filter(
                    Volume__in=get_data['Volume']).values_list('id', flat=True)[::1]
                aliquots_data = ProcessedAliquots.objects.filter(pk__in=ids).values_list(
                    'SampleType', 'Volume', 'VolumeUnit', 'PostProcessingStatus')
            elif get_data['Sample'] == [''] and get_data['Volume'] == [''] and get_data['Status'] != ['']:
                ids = ProcessedAliquots.objects.filter(
                    PostProcessingStatus__in=get_data['Status']).values_list('id', flat=True)[::1]
                aliquots_data = ProcessedAliquots.objects.filter(pk__in=ids).values_list(
                    'SampleType', 'Volume', 'VolumeUnit', 'PostProcessingStatus')
            elif get_data['Sample'] == [''] and get_data['Volume'] == [''] and get_data['Status'] == ['']:
                aliquots_data = ProcessedAliquots.objects.all().values_list(
                    'SampleType', 'Volume', 'VolumeUnit', 'PostProcessingStatus')
            aliquots_data = list(aliquots_data)
            aliquots_data.insert(
                0, ('Sample Type', 'Volume', 'Volume Unit', 'Post Processing Status'))
            context = {'db_data': aliquots_data}
        else:
            req = get_data
            for key, val in req.items():
                req[key] = val[0].split(',')

            # Executing an SQL function using the execute() method
            query = """SELECT """
            headers = []
            for column in req['Aliquots']:
                headers.append(column)
                query += "\""+column + "\", "
            if len(headers) == 0:
                query += """ "SampleType", "Volume", "VolumeUnit", "PostProcessingStatus"
                """
                headers = ('Sample Type', 'Volume', 'Volume Unit',
                           'Post Processing Status')
            else:
                query = query[:-2]
            query += """ from blood_sample_processedaliquots """
            cursor.execute(query)
            # Fetch rows using fetchall() method.
            data = cursor.fetchall()

            data.insert(0, headers)
            context = {'db_data': data}

        return render(request, self.template_name, context)


class SettingsOptionsView(LoginRequiredMixin, View):
    template_name = 'settings_bloodsample.html'

    def get(self, request, *args, **kwargs):
        """
        Method to return settings columns columns
        """
        import json
        settings = eval(request.GET.get('settings'))
        filters = eval(request.GET.get('filters'))
        context = {'settings': settings, 'filters': filters}
        return render(request, self.template_name, context)


class SettingsAliquotsView(LoginRequiredMixin, View):
    template_name = 'settings_aliquots.html'

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
        filters = eval(request.GET.get('filters'))
        settings = eval(request.GET.get('settings'))
        date_from = filters['DF'][0]
        date_to = filters['DT'][0]
        receipt_barcode = ReceiptRecords.objects.all().values_list('Barcode')
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
        dist_state = ['ACTIVE', 'UNABLE_TO_DRAW', 'UNABLE_TO_PROCESS',
                      'PROCESSED_ON_TIME', 'PROCESSED_NOT_ON_TIME']
        context = {'sites': dist_sites,
                   'visits': dist_visits, 'rooms': dist_rooms, 'filters': filters, 'settings': settings, 'states': dist_state, 'from': date_from, 'to': date_to}
        return render(request, self.template_name, context)


class FilterAliquotsView(LoginRequiredMixin, View):
    template_name = 'filter_Aliquots.html'

    def get(self, request, *args, **kwargs):
        """
        Method to Return Filter Options
        """
        # ProcessedAliquots.objects.all().values('SampleType', 'Volume', 'VolumeUnit', 'PostProcessingStatus')
        samples = ProcessedAliquots.objects.all().values('SampleType').distinct()
        dist_sample = []
        for sample in samples:
            dist_sample += list(sample.values())
        volumes = ProcessedAliquots.objects.all().values('Volume').distinct()
        dist_volume = []
        for volume in volumes:
            dist_volume += list(volume.values())
        Units = ProcessedAliquots.objects.all().values('VolumeUnit').distinct()
        dist_unit = []
        for unit in Units:
            dist_unit += list(unit.values())
        status = ProcessedAliquots.objects.all().values(
            'PostProcessingStatus').distinct()
        dist_status = []
        for stat in status:
            dist_status += list(stat.values())
        context = {'samples': dist_sample, 'volumes': dist_volume,
                   'units': dist_unit, 'status': dist_status}
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

        df = df.drop_duplicates()
        # Fields Check
        if not set(['Id', 'CohortId', 'AppointmentId', 'Barcode', 'User', 'CreatedAt']).issubset(df.columns):
            return JsonResponse({'status': 412, 'message': 'Column names not matching'})
        if BloodSample.objects.count() >= df.shape[0]:
            return JsonResponse({'status': 412, 'message': 'The uploaded file has less than or equal number of records compared to database records'})

        try:
            df['CreatedAt'] = df['CreatedAt'].apply(lambda x: datetime.datetime.strptime(
                x, "%Y-%m-%dT%H:%M:%SZ"))
        except:
            return JsonResponse({'status': 412, 'message': 'CreatedAt column values are not in expected format'})

        # if True in (df['CreatedAt'].map(type) != datetime.datetime).tolist():
        #     return JsonResponse({'status': 412, 'message': 'CollectionDateTime columns value are not in same format'})
        if request.GET.get('confirm', '') == 'True':
            # Dropping duplicates
            report_ids = BloodSample.objects.values_list('id', flat=True)[
                ::1]
            excel_ids = df.Id.values.tolist()
            new_records = list(set(excel_ids).difference(report_ids))
            df = df[df['Id'].isin(new_records)]

            # Storing file
            fs = FileSystemStorage(
                location=settings.UPLOAD_ROOT+'/CurrentAppointmentBlood')
            filename = fs.save(test_file.name.split(
                '.')[0]+time.strftime("%d%m%Y-%H%M%S")+'.'+test_file.name.split('.')[1], test_file)
            # End of storing file

            day, days = UploadView.get_dayformated_and_days(self, request)
            ImportId = BloodSampleImport.objects.create(
                FilePath="CurrentAppointmentBlood/"+filename,
                OriginalFileName=test_file.name,
                CreatedBy=request.user,
                CreatedAt=day,
                Deleted=False,
                Reviewed=False,
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
                    State=0 if re.match(
                        r"^(E[0-9]{6})+$", record['Barcode']) else 1,
                ) for index, record in df.iterrows()
            ]
            BloodSample.objects.bulk_create(model_instances)
            return render(request, self.blood_sample_success_template, {"new_records": len(new_records)})

        report_ids = BloodSample.objects.values_list('id', flat=True)[
            ::1]
        excel_ids = df.Id.values.tolist()
        new_records = set(excel_ids).difference(report_ids)

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

        df['CohortId'] = df['CohortId'].apply(lambda x: x.strip())
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

            # Dropping duplicates
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

            day, days = UploadView.get_dayformated_and_days(self, request)
            ImportId = ManifestImports.objects.create(
                FilePath="Manifests/"+filename,
                OriginalFileName=test_file.name,
                CreatedBy=request.user,
                CreatedAt=day,
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
    receipt_confirm_template = 'confirm-receipt.html'
    receipt_success_template = 'success-receipt.html'

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

        df = df.drop_duplicates()
        if not set(['Participant ID', 'Clinic', 'DateTime Taken', 'Sample ID',
                    'Tissue sub-type', 'Received DateTime', 'Volume', 'Volume Unit',
                    'Condition']).issubset(df.columns):
            return JsonResponse({'status': 412, 'message': 'Column names not matching'})

        try:
            df['DateTime Taken'] = df['DateTime Taken'].apply(lambda x: datetime.datetime.strptime(
                x, "%d/%m/%Y %H:%M"))
        except:
            return JsonResponse({'status': 412, 'message': 'DateTime Taken column values are not in expected format'})
        try:
            df['Received DateTime'] = df['Received DateTime'].apply(lambda x: datetime.datetime.strptime(
                x, "%d/%m/%Y %H:%M"))
        except:
            return JsonResponse({'status': 412, 'message': 'Received DateTime column values are not in expected format'})

        if True in (df['Volume Unit'] != 'uL').tolist():
            return JsonResponse({'status': 412, 'message': 'Volume Unit column values are not an uL'})

        if True in (df['Tissue sub-type'] != 'EDTA').tolist():
            return JsonResponse({'status': 412, 'message': 'Tissue sub-type column values are not an EDTA'})

        clinic_mapping = {
            'uk biocentre signature': 'Manifest Signature',
            'uch - university college london hospital': 'UCLH',
            'mile end hospital': 'Mile End Hospital',
            'finchley memorial': 'FMH',
            'king george hospital ilford': 'KGH',
        }
        try:
            df['Clinic'] = df['Clinic'].apply(
                lambda x:
                    clinic_mapping[x.lower()])
        except:
            return JsonResponse({'status': 412, 'message': 'Clinic column values are not in expected format'})

        # TODO: Checking Receipt Date time along with Seconds also
        df['DateTime Taken compare'] = df['DateTime Taken'].apply(
            lambda x: x.strftime('%d/%m/%Y %H:%M'))
        manifest_db_df = pd.DataFrame(ManifestRecords.objects.all().values())
        manifest_db_df['CollectionDateTime'] = manifest_db_df['CollectionDateTime'].apply(
            lambda x: x.strftime('%d/%m/%Y %H:%M'))
        manifest_db_filtered = manifest_db_df[manifest_db_df['CohortId'].isin(BloodSample.objects.values_list(
            'CohortId', flat=True)[::1])]

        manifest_match = df[df['Participant ID'].isin(manifest_db_filtered.Barcode.values) & df['Clinic'].isin(
            manifest_db_filtered.Site.values) & df['DateTime Taken compare'].isin(manifest_db_filtered.CollectionDateTime.values)]
        record_found_cnt = manifest_match.shape[0]

        mismatch_site = df[df['Participant ID'].isin(manifest_db_df.Barcode.values) & ~df['Clinic'].isin(
            manifest_db_df.Site.values)]
        mismatch_site_found_cnt = mismatch_site.shape[0]

        mismatch_blood_draw = df[df['Participant ID'].isin(manifest_db_df.Barcode.values) & ~df['DateTime Taken compare'].isin(
            manifest_db_df.CollectionDateTime.values)]
        mismatch_blood_draw_found_cnt = mismatch_blood_draw.shape[0]

        # Checking number of Receipt records barcodes not existing in Manifest table
        reciept_barcode_existance = df[~df['Participant ID'].isin(
            manifest_db_df.Barcode.values)].shape[0]

        total_records = df.shape[0]
        if request.GET.get('confirm', '') == 'True':
            del df['DateTime Taken compare']

            fs = FileSystemStorage(
                location=settings.UPLOAD_ROOT+'/Receipt')
            filename = fs.save(test_file.name.split(
                '.')[0]+time.strftime("%d%m%Y-%H%M%S")+'.'+test_file.name.split('.')[1], test_file)
            # End of storing file

            day, days = UploadView.get_dayformated_and_days(self, request)
            ImportId = ReceiptImports.objects.create(
                FilePath="Receipt/"+filename,
                OriginalFileName=test_file.name,
                CreatedBy=request.user,
                CreatedAt=day,
                Deleted=False
            )

            # Dropping duplicates
            receipt_barcode = ReceiptRecords.objects.values_list('Barcode', flat=True)[
                ::1]
            df = df[~df['Participant ID'].isin(receipt_barcode)]

            model_instances = [
                ReceiptRecords(
                    Barcode=record['Participant ID'],
                    Clinic=record['Clinic'],
                    DateTimeTaken=record['DateTime Taken'],
                    SampleId=record['Sample ID'],
                    TissueSubType=record['Tissue sub-type'],
                    ReceivedDateTime=record['Received DateTime'],
                    Volume=record['Volume'],
                    VolumeUnit=record['Volume Unit'],
                    Condition=record['Condition'],
                    ImportId=ImportId,
                ) for index, record in df.iterrows()
            ]
            ReceiptRecords.objects.bulk_create(model_instances)

            return render(request, self.receipt_success_template, {
                "record_found_cnt": record_found_cnt,
                "mismatch_site_found_cnt": mismatch_site_found_cnt,
                "mismatch_blood_draw_found_cnt": mismatch_blood_draw_found_cnt,
                "reciept_barcode_existance": reciept_barcode_existance,
            })

        return render(request, self.receipt_confirm_template, {
            "total_records": total_records,
            "record_found_cnt": record_found_cnt,
            "mismatch_site_found_cnt": mismatch_site_found_cnt,
            "mismatch_blood_draw_found_cnt": mismatch_blood_draw_found_cnt,
            "reciept_barcode_existance": reciept_barcode_existance,
        })


class UploadProcessedView(LoginRequiredMixin, View):
    template_name = 'upload-processed.html'
    receipt_confirm_template = 'confirm-processed.html'
    receipt_success_template = 'success-processed.html'

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

        df = df.drop_duplicates()

        if not set(['Participant ID', 'Parent ID', 'Sample ID', 'Tissue Sub-Type',
                    'Sample Type', 'Received DateTime', 'Processed Date Time', 'Volume',
                    'Volume Unit', 'No. of Children']).issubset(df.columns):
            return JsonResponse({'status': 412, 'message': 'Column names not matching'})

        if set(df['Sample Type'].unique().tolist()) != set(['RBC', 'Plasma', 'BuffyCoat', 'Whole Blood']):
            return JsonResponse({'status': 412, 'message': 'Sample Type column values are not having expected values'})

        parent_df = df[df['Parent ID'] == 'No Parent']
        child_df = df[df['Parent ID'] != 'No Parent']

        try:
            parent_df['Processed Date Time'].apply(lambda x: datetime.datetime.strptime(
                x, "%d/%m/%Y %H:%M"))
        except:
            return JsonResponse({'status': 412, 'message': 'Processed Date Time column values are not in expected format'})

        try:
            parent_df['Received DateTime'].apply(lambda x: datetime.datetime.strptime(
                x, "%d/%m/%Y %H:%M"))
        except:
            return JsonResponse({'status': 412, 'message': 'Received DateTime column values are not in expected format'})

        if True in (parent_df['Volume Unit'] != 'uL').tolist():
            return JsonResponse({'status': 412, 'message': 'Volume Unit column with Parent ID, values are not an uL'})

        if True in (df[df['Parent ID'] != 'No Parent']['Volume Unit'] != 'ul').tolist():
            return JsonResponse({'status': 412, 'message': 'Volume Unit column with no Parent ID, values are not an ul'})

        if True in (parent_df['Sample Type'] != 'Whole Blood').tolist():
            return JsonResponse({'status': 412, 'message': 'Sample Type column with Parent ID, values are not an Whole Blood'})

        if set(df[df['Parent ID'] != 'No Parent']
                ['Sample Type'].unique().tolist()) != set(['RBC', 'Plasma', 'BuffyCoat']):
            return JsonResponse({'status': 412, 'message': 'Sample Type column with no Parent ID, values are not having expected values'})

        if True in (df['Tissue Sub-Type'] != 'EDTA').tolist():
            return JsonResponse({'status': 412, 'message': 'Tissue sub-type column values are not an EDTA'})

        if True in (df['No. of Children'].map(type) != int).tolist():
            return JsonResponse({'status': 412, 'message': 'No. of Children column values are not having expected values'})

        if True in (df['Volume'].map(type) != float).tolist():
            return JsonResponse({'status': 412, 'message': 'Volume column values are not having expected values'})

        total_records = parent_df.shape[0]

        manifest_db_df = pd.DataFrame(ManifestRecords.objects.filter(
            Barcode__in=parent_df['Participant ID'].tolist()).values())

        # Checking number of Parent records barcodes not existing in Manifest table
        reciept_barcode_existance = total_records - manifest_db_df.shape[0]

        # Comparing hours
        manifest_parent_df = parent_df[parent_df['Participant ID'].isin(
            manifest_db_df.Barcode.values)]
        manifest_db_df = manifest_db_df.rename(
            columns={'Barcode': 'Participant ID'})
        manifest_db_df = pd.merge(
            manifest_parent_df, manifest_db_df, on='Participant ID')
        manifest_db_df['Processed Date Time'] = manifest_db_df['Processed Date Time'].apply(lambda x: datetime.datetime.strptime(
            x, "%d/%m/%Y %H:%M"))
        manifest_db_df['CollectionDateTime'] = manifest_db_df['CollectionDateTime'].apply(lambda x: datetime.datetime.strftime(
            x, "%d/%m/%Y %H:%M"))
        manifest_db_df['CollectionDateTime'] = manifest_db_df['CollectionDateTime'].apply(lambda x: datetime.datetime.strptime(
            x, "%d/%m/%Y %H:%M"))

        manifest_db_df['greaterthan_48hrs'] = ''
        for index, row in manifest_db_df.iterrows():
            manifest_db_df.at[index, 'greaterthan_48hrs'] = True if (
                manifest_db_df['Processed Date Time'].iloc[index]-manifest_db_df['CollectionDateTime'].iloc[index]).total_seconds() // 3600 > 48 else False

        if request.GET.get('confirm', '') == 'True':
            fs = FileSystemStorage(
                location=settings.UPLOAD_ROOT+'/Processed')
            filename = fs.save(test_file.name.split(
                '.')[0]+time.strftime("%d%m%Y-%H%M%S")+'.'+test_file.name.split('.')[1], test_file)
            # End of storing file

            day, days = UploadView.get_dayformated_and_days(self, request)
            ImportId = ProcessedImports.objects.create(
                FilePath="Processed/"+filename,
                OriginalFileName=test_file.name,
                CreatedBy=request.user,
                CreatedAt=day,
                Deleted=False
            )

            # Dropping duplicates
            processed_barcode = ProcessedReport.objects.values_list('Barcode', flat=True)[
                ::1]
            parent_df = parent_df[~parent_df['Participant ID'].isin(
                processed_barcode)]

            parent_df['Processed Date Time'] = parent_df['Processed Date Time'].apply(
                lambda x: datetime.datetime.strptime(x, "%d/%m/%Y %H:%M"))
            parent_df['Received DateTime'] = parent_df['Received DateTime'].apply(
                lambda x: datetime.datetime.strptime(x, "%d/%m/%Y %H:%M"))
            model_instances = [
                ProcessedReport(
                    Barcode=record['Participant ID'],
                    ParentId=ReceiptRecords.objects.filter(
                        Barcode=record['Participant ID']).first().SampleId,
                    TissueSubType=record['Tissue Sub-Type'],
                    ReceivedDateTime=record['Received DateTime'],
                    ProcessedDateTime=record['Processed Date Time'],
                    Volume=record['Volume'],
                    VolumeUnit=record['Volume Unit'],
                    NumberOfChildren=record['No. of Children'],
                    ImportId=ImportId,
                ) for index, record in parent_df.iterrows()
            ]
            ProcessedReport.objects.bulk_create(model_instances)

            # Dropping duplicates
            processed_aliquots_barcode = ProcessedAliquots.objects.values_list('SampleIdFile', flat=True)[
                ::1]
            child_df = child_df[~child_df['Sample ID'].isin(
                processed_aliquots_barcode)]

            model_instances = [
                ProcessedAliquots(
                    SampleType=record["Sample Type"],
                    Volume=record['Volume'],
                    VolumeUnit=record['Volume Unit'],
                    PostProcessingStatus=0,
                    SampleId=ProcessedReport.objects.filter(
                        Barcode=record['Participant ID']).first().ParentId,
                    SampleIdFile=record['Sample ID'],
                ) for index, record in child_df.iterrows()
            ]
            ProcessedAliquots.objects.bulk_create(model_instances)

            manifest_db_df = manifest_db_df[manifest_db_df['Participant ID'].isin(
                parent_df['Participant ID'].tolist())]

            processed_not_on_time = 0
            for index, row in manifest_db_df.iterrows():
                blood_samples = BloodSample.objects.filter(
                    CohortId=row['CohortId'])
                for sample in blood_samples:
                    if row['greaterthan_48hrs'] == True:
                        sample.State = 4
                        sample.save()
                        processed_not_on_time += 1
                    elif row['greaterthan_48hrs'] == False:
                        sample.State = 3
                        sample.save()

            for index, row in parent_df[parent_df['No. of Children'] < 6].iterrows():
                blood_samples = BloodSample.objects.filter(
                    Barcode=row['Participant ID'])
                for sample in blood_samples:
                    sample.State = 2
                    sample.save()

            if processed_not_on_time > 0:
                msg_html = render_to_string(
                    'mail-aliquots-less.html', {'processed_not_on_time': processed_not_on_time,
                                                'referer': request.headers['Referer'][:-1]})
                send_mail(
                    'Blood Samples - Uploaded Processed records which are not processed under 48 hours',
                    msg_html,
                    settings.EMAIL_HOST_USER,
                    [i.user_id.email for i in UserRoles.objects.filter(role_id__in=[
                        1, 2])],  # This should be list of from users
                    html_message=msg_html,
                )
            return render(request, self.receipt_success_template, {
                "total_records": total_records,
                "processed_on_time": manifest_db_df.greaterthan_48hrs[manifest_db_df.greaterthan_48hrs == False].count(),
                "processed_not_on_time": manifest_db_df.greaterthan_48hrs[manifest_db_df.greaterthan_48hrs == True].count(),
                "less_aliquots_cnt": parent_df['No. of Children'][parent_df['No. of Children'] < 6].count(),
                "barcode_existance": reciept_barcode_existance,
            })
        return render(request, self.receipt_confirm_template, {
            "total_records": total_records,
            "processed_on_time": manifest_db_df.greaterthan_48hrs[manifest_db_df.greaterthan_48hrs == False].count(),
            "processed_not_on_time": manifest_db_df.greaterthan_48hrs[manifest_db_df.greaterthan_48hrs == True].count(),
            "less_aliquots_cnt": parent_df['No. of Children'][parent_df['No. of Children'] < 6].count(),
            "barcode_existance": reciept_barcode_existance,
        })


class ReviewView(LoginRequiredMixin, View):
    """
    Class for login functionality
    """

    blood_sample_review_template = 'review_blood_sample/blood-sample-review.html'
    blood_sample_review_table_template = 'review_blood_sample/blood-sample-table.html'
    manifest_review_template = 'review_manifest/manifest-review.html'
    manifest_review_table_template = 'review_manifest/manifest-table.html'

    def get(self, request, *args, **kwargs):
        """
        Method to get the login form or redirect to Dashboard if session exists
        :param request: request object
        :return: HttpResponse object
        """
        review_type = request.GET.get("type", "blood_sample")
        page = int(request.GET.get('page', 1))
        # try:
        #     day = request.GET.get(
        #         'day', datetime.datetime.today().strftime('%B %d, %Y'))
        # except:
        #     day = request.GET.get(
        #         'day', datetime.datetime.today().strftime('%b. %d, %Y'))
        table = request.GET.get('table', 'False')
        day, days = UploadView.get_dayformated_and_days(self, request)

        if review_type == "blood_sample":

            blood_samples_imported = BloodSampleImport.objects.filter(
                CreatedAt__range=(day.replace(hour=0, minute=0, second=0, microsecond=0), day.replace(
                    hour=23, minute=59, second=59, microsecond=0)))

            # Checking latest uploaded sample file is reviewed or not
            if blood_samples_imported.count() > 0:
                sample_import_latest = blood_samples_imported.last()
                if not sample_import_latest.Reviewed:
                    sample_import_latest.Reviewed = True
                    sample_import_latest.save()

            if request.GET.get('firstOpen', 'False') == "True":
                if not day < datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0):
                    day = BloodSample.objects.all().order_by('-CreatedAt').first().CreatedAt
                    days = [(day - datetime.timedelta(days=x))
                            for x in range(4)]
                    days.reverse()
            # import ipdb
            # ipdb.set_trace()
            query_results = BloodSample.objects.filter(
                CreatedAt__range=(day.replace(hour=0, minute=0, second=0, microsecond=0), day.replace(
                    hour=23, minute=59, second=59, microsecond=0))).order_by('CreatedAt', 'CohortId', 'Barcode')
            if query_results.count() == 0 and request.GET.get('firstOpen', 'False') == "True":
                day = BloodSample.objects.all().order_by('-CreatedAt').first().CreatedAt
                days = [(day - datetime.timedelta(days=x))
                        for x in range(4)]
                days.reverse()
                query_results = BloodSample.objects.filter(
                    CreatedAt__range=(day.replace(hour=0, minute=0, second=0, microsecond=0), day.replace(
                        hour=23, minute=59, second=59, microsecond=0))).order_by('CreatedAt', 'CohortId', 'Barcode')
            # query_results = BloodSample.objects.filter(
            #     ImportId__in=blood_samples_imported.values_list('id', flat=True)[::1]).order_by('id')

            paginator = Paginator(query_results, settings.ITEMS_PER_PAGE)

            if table == "True":
                try:
                    results = paginator.page(page)
                except PageNotAnInteger:
                    results = paginator.page(1)
                except EmptyPage:
                    results = paginator.page(paginator.num_pages)
                return render(request, self.blood_sample_review_table_template, {
                    "objects": results.object_list,
                    "current_page": page,
                    "class": 'reviewBloodDay',
                    "total_pages": paginator.num_pages
                })

            shownextday = datetime.datetime.today().strftime(
                '%d%b%y') in [i.strftime('%d%b%y') for i in days]
            return render(request, self.blood_sample_review_template, {
                "current_page": page,
                "total_pages": paginator.num_pages,
                "days": days,
                "active": day,
                "shownextday": shownextday,
                "class": 'reviewBloodDay',
            })

        if review_type == "manifest":
            manifest_imported = ManifestImports.objects.filter(
                CreatedAt__range=(day.replace(hour=0, minute=0, second=0, microsecond=0), day.replace(
                    hour=23, minute=59, second=59, microsecond=0)))

            query_results = ManifestRecords.objects.filter(
                ImportId__in=manifest_imported.values_list('id', flat=True)[::1]).order_by('id')

            paginator = Paginator(query_results, settings.ITEMS_PER_PAGE)

            if table == "True":
                try:
                    results = paginator.page(page)
                except PageNotAnInteger:
                    results = paginator.page(1)
                except EmptyPage:
                    results = paginator.page(paginator.num_pages)

                cursor.execute('''
                    SELECT * FROM "blood_sample_bloodsample"
                    INNER JOIN "blood_sample_manifestrecords" ON ( "blood_sample_bloodsample"."CohortId" = "blood_sample_manifestrecords"."CohortId" )
                    ''')

                # row = cursor.fetchall()
                columns = [col[0] for col in cursor.description]
                data = [
                    dict(zip(columns, row))
                    for row in cursor.fetchall()
                ]
                # import ipdb
                # ipdb.set_trace()
                # print(row)

                # BloodSample.objects.filter(
                #     CohortId__in=results.object_list.values_list('CohortId', flat=True)[::1])

                return render(request, self.manifest_review_table_template, {
                    "objects": results.object_list,
                    # "blood_sample_objects": BloodSample.objects.filter(
                    #     CohortId__in=results.object_list.values_list('CohortId', flat=True)[::1]),
                    "current_page": page,
                    "total_pages": paginator.num_pages
                })

            shownextday = datetime.datetime.today().strftime(
                '%d%b%y') in [i.strftime('%d%b%y') for i in days]
            return render(request, self.manifest_review_template, {
                "current_page": page,
                "total_pages": paginator.num_pages,
                "days": days,
                "active": day,
                "shownextday": shownextday,
                "class": 'reviewManifestDay',
            })


class EditBloodSampleView(LoginRequiredMixin, View):
    """
    Class for login functionality
    """

    blood_sample_review_template = 'review_blood_sample/blood-sample-edit.html'

    def get(self, request, *args, **kwargs):
        """
        Method to get the login form or redirect to Dashboard if session exists
        :param request: request object
        :return: HttpResponse object
        """
        return render(request, self.blood_sample_review_template, {
            "object": BloodSample.objects.get(id=int(request.GET.get('id'))),
            "STATECHOICE": dict(STATECHOICE)
        })

    def post(self, request, *args, **kwargs):
        object = BloodSample.objects.get(id=int(request.GET.get('id')))

        data_edit = request.GET.dict()
        data_edit = {key: data_edit[key]
                     for key in ['CohortId', 'Comments', 'Barcode', 'State', 'AppointmentId', 'CreatedAt']}

        data_object = object.__dict__
        data_object = {key: data_object[key]
                       for key in ['CohortId', 'Comments', 'Barcode', 'State', 'AppointmentId', 'CreatedAt']}
        diffs = [(k, (v, data_edit[k]))
                 for k, v in data_object.items() if v != data_edit[k]]
        for i in diffs:
            setattr(object, i[0], i[1][1])
            BloodSampleChanges.objects.create(
                Field=i[0],
                FromValue=i[1][0],
                ChangedBy=request.user,
            )
        object.save()
        return JsonResponse({'status': 200, 'message': f'{request.GET.get("id")} sample updated successfully'})
