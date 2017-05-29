from reports.models import *
from reports.constants import *
from leads.models import *
from deals.models import *
from django.db.models import Count, Sum
import uuid
from djqscsv import write_csv
from datetime import datetime,tzinfo,timedelta
from django.conf import settings
import tinys3
import os

class Zone(tzinfo):
    def __init__(self,offset,isdst,name):
        self.offset = offset
        self.isdst = isdst
        self.name = name

    def utcoffset(self, dt):
        return timedelta(hours=self.offset) + self.dst(dt)

    def dst(self, dt):
            return timedelta(hours=1) if self.isdst else timedelta(0)

    def tzname(self,dt):
         return self.name

WIB_ZONE = 7

def upload_to_s3(filename):
    s3_access_key = settings.S3_ACCESS_KEY
    s3_secret_key = settings.S3_SECRET_KEY
    s3_endpoint = settings.S3_ENDPOINT
    s3_bucket = settings.S3_BUCKET
    conn = tinys3.Connection(s3_access_key, s3_secret_key, endpoint=s3_endpoint, tls=True)
    f = open(filename,'rb')
    conn.upload(filename, f, s3_bucket)

    s3_url = 'https://' + s3_endpoint + '/' + s3_bucket + '/' + filename

    return s3_url

def generate_lead_csv(report, filename):
    queryset = Lead.objects.filter(entity=report.entity).filter(is_deleted=False)
    if report.employee:
        queryset = queryset.filter(employee=report.employee)
    ranged_queryset = queryset.filter(created_at__range=(report.start_date, report.end_date))
    ordered_queryset = ranged_queryset.order_by('status', 'lead_source')
    values_queryset = ordered_queryset.values('first_name', 'last_name', 'status', 'lead_source', 'company_name', 'phone', 'mobile_phone',
                                              'email', 'fax', 'position', 'employee__user__first_name', 'street', 'city',
                                              'state', 'country', 'pos_code', 'description', 'created_at')

    field_header_map={'employee__user__first_name': 'employee name'}
    status_dict = {'O': 'Open', 'C': 'Closed', 'CV': 'Converted', '': ''}
    lead_source_dict= {'OFA': 'Offline Ads', 'ONA': 'Online Ads', 'CC': 'Cold Call', 'IR': 'Internal Referral',
                       'ER': 'External Referral', 'P': 'Partner', 'S': 'Sales', 'TS': 'Trade Show',
                       'SR': 'Seminar', '': ''}
    WIB = Zone(WIB_ZONE, False, 'WIB')
    field_serializer_map = {'status': (lambda x: status_dict[x]), 'lead_source': (lambda x: lead_source_dict[x]),
                            'created_at': (lambda x: x.now(WIB).strftime('%d/%m/%Y %H:%M:%S %Z'))}

    with open(filename, 'w') as csv_file:
        write_csv(values_queryset, csv_file, field_header_map=field_header_map, field_serializer_map=field_serializer_map)


def generate_lead_meta(report):
    meta = {}

    if report.employee:
        employee = report.employee.user.first_name + ' ' + report.employee.user.last_name
        results = Lead.objects.filter(entity=report.entity).filter(is_deleted=False).filter(employee=report.employee).\
            filter(created_at__range=(report.start_date, report.end_date)).values('status').annotate(total=Count('status')).order_by('status')
        summary = {}
        for result in results:
            summary[result['status']] = result['total']
        meta['employee'] = employee
        meta['summary'] = summary
    else:
        employee = 'All Employee'
        results = Lead.objects.filter(entity=report.entity).filter(is_deleted=False).\
            filter(created_at__range=(report.start_date, report.end_date)).values('status').\
            annotate(total=Count('status')).order_by('status')
        summary = {}
        for result in results:
            summary[result['status']] = result['total']

        employee_summary = {}
        employee_results = Lead.objects.filter(entity=report.entity).filter(is_deleted=False).\
            filter(created_at__range=(report.start_date, report.end_date)).\
            values('status', 'employee__user__first_name', 'employee__user__last_name').\
            annotate(total=Count('status')).order_by('status')
        for employee_result in employee_results:
            name = employee_result['employee__user__first_name'] + ' ' + employee_result['employee__user__last_name']
            if employee_summary.get(name, '') == '':
                employee_summary[name] = {}
            employee_summary[name][employee_result['status']] = employee_result['total']

        meta['employee'] = employee
        meta['summary'] = summary
        meta['employee_summary'] = employee_summary

    return meta

def generate_lead_report(report):
    basename = 'lead' + str(report.start_date.strftime('%d%B%Y')) + '-' + str(report.end_date.strftime('%d%B%Y')) + '-' + str(report.entity) + str(uuid.uuid4())
    filename = basename + '.csv'

    meta = generate_lead_meta(report)
    generate_lead_csv(report, filename)

    csv_s3_url = upload_to_s3(filename)

    report.meta = meta
    report.url = csv_s3_url
    report.status = ReportConstant.DONE
    report.save()

    os.remove(filename)
    return


def generate_task_csv(report, filename):
    queryset = Task.objects.filter(entity=report.entity).filter(is_deleted=False)
    if report.employee:
        queryset = queryset.filter(employee=report.employee)
    ranged_queryset = queryset.filter(due_date__range=(report.start_date, report.end_date))
    ordered_queryset = ranged_queryset.order_by('status', 'due_date')
    values_queryset = ordered_queryset.values('subject', 'lead__first_name', 'lead__last_name', 'lead__company_name', 'customer__first_name',
                                              'customer__last_name', 'company__name', 'status', 'priority', 'due_date', 'deal__name',
                                              'employee__user__first_name', 'description', 'created_at', 'notes__note')
    field_header_map={'lead__first_name': 'lead first name', 'lead__last_name': 'lead last name', 'lead__company_name': 'lead company name',
                      'customer__first_name': 'customer last name', 'customer__last_name': 'customer last name', 'deal__name': 'deal name',
                      'employee__user__first_name': 'employee name', 'notes__note': 'note'}
    status_dict = {'O': 'Open', 'C': 'Closed', 'P': 'Progress', '': ''}
    priority_dict = {'H': 'High', 'M': 'Medium', 'L': 'Low', '': ''}

    WIB = Zone(WIB_ZONE, False, 'WIB')
    field_serializer_map = {'status': (lambda x: status_dict[x]), 'priority': (lambda x: priority_dict[x]),
                            'due_date': (lambda x: x.strftime('%d/%m/%Y')), 'created_at': (lambda x: x.now(WIB).strftime('%d/%m/%Y %H:%M:%S %Z'))}

    with open(filename, 'w') as csv_file:
        write_csv(values_queryset, csv_file, field_header_map=field_header_map, field_serializer_map=field_serializer_map)

def generate_task_meta(report):
    meta = {}

    if report.employee:
        employee = report.employee.user.first_name + ' ' + report.employee.user.last_name
        results = Task.objects.filter(entity=report.entity).filter(is_deleted=False).filter(employee=report.employee).\
            filter(due_date__range=(report.start_date, report.end_date)).values('status').annotate(total=Count('status')).order_by('status')
        summary = {}
        for result in results:
            summary[result['status']] = result['total']
        meta['employee'] = employee
        meta['summary'] = summary
    else:
        employee = 'All Employee'
        results = Task.objects.filter(entity=report.entity).filter(is_deleted=False).\
            filter(due_date__range=(report.start_date, report.end_date)).values('status').\
            annotate(total=Count('status')).order_by('status')
        summary = {}
        for result in results:
            summary[result['status']] = result['total']

        employee_summary = {}
        employee_results = Task.objects.filter(entity=report.entity).filter(is_deleted=False).\
            filter(due_date__range=(report.start_date, report.end_date)).\
            values('status', 'employee__user__first_name', 'employee__user__last_name').\
            annotate(total=Count('status')).order_by('status')
        for employee_result in employee_results:
            name = employee_result['employee__user__first_name'] + ' ' + employee_result['employee__user__last_name']
            if employee_summary.get(name, '') == '':
                employee_summary[name] = {}
            employee_summary[name][employee_result['status']] = employee_result['total']

        meta['employee'] = employee
        meta['summary'] = summary
        meta['employee_summary'] = employee_summary

    return meta

def generate_task_report(report):
    basename = 'task' + str(report.start_date.strftime('%d%B%Y')) + '-' + str(report.end_date.strftime('%d%B%Y')) + '-' + str(report.entity) + str(uuid.uuid4())
    filename = basename + '.csv'

    meta = generate_task_meta(report)
    generate_task_csv(report, filename)

    csv_s3_url = upload_to_s3(filename)

    report.meta = meta
    report.url = csv_s3_url
    report.status = ReportConstant.DONE
    report.save()

    os.remove(filename)
    return

def generate_event_report(report):
    pass

def generate_deal_csv(report, filename):
    queryset = Deal.objects.filter(entity=report.entity).filter(is_deleted=False)
    if report.employee:
        queryset = queryset.filter(employee=report.employee)
    ranged_queryset = queryset.filter(expected_closing_date__range=(report.start_date, report.end_date))
    ordered_queryset = ranged_queryset.order_by('status', 'expected_closing_date')
    values_queryset = ordered_queryset.values('name', 'customer__first_name', 'customer__last_name', 'company__name',
                                              'status', 'expected_closing_date', 'expected_revenue',
                                              'employee__user__first_name', 'description', 'created_at')
    field_header_map={'customer__first_name': 'customer first name' ,'customer__last_name': 'customer last name',
                      'company__name': 'company name', 'employee__user__first_name': 'employee name'}
    status_dict = {'O': 'Open', 'P': 'Progress', 'CW': 'Won', 'CL':'Lost', '': ''}
    WIB = Zone(WIB_ZONE, False, 'WIB')
    field_serializer_map = {'status': (lambda x: status_dict[x]), 'expected_closing_date': (lambda x: x.strftime('%d/%m/%Y')),
                            'created_at': (lambda x: x.now(WIB).strftime('%d/%m/%Y %H:%M:%S %Z'))}

    with open(filename, 'w') as csv_file:
        write_csv(values_queryset, csv_file, field_header_map=field_header_map, field_serializer_map=field_serializer_map)


def generate_deal_meta(report):
    meta = {}

    if report.employee:
        employee = report.employee.user.first_name + ' ' + report.employee.user.last_name
        results = Deal.objects.filter(entity=report.entity).filter(is_deleted=False).filter(employee=report.employee).\
            filter(expected_closing_date__range=(report.start_date, report.end_date)).values('status').\
            annotate(total=Count('status'), sum=Sum('expected_revenue')).order_by('status')
        summary = {}
        for result in results:
            summary[result['status']] = result['total']
            summary['revenue_' + result['status']] = result['sum']
        meta['employee'] = employee
        meta['summary'] = summary
    else:
        employee = 'All Employee'
        results = Deal.objects.filter(entity=report.entity).filter(is_deleted=False).\
            filter(expected_closing_date__range=(report.start_date, report.end_date)).values('status').\
            annotate(total=Count('status'), sum=Sum('expected_revenue')).order_by('status')
        summary = {}
        for result in results:
            summary[result['status']] = result['total']
            summary['revenue_' + result['status']] = result['sum']

        employee_summary = {}
        employee_results = Deal.objects.filter(entity=report.entity).filter(is_deleted=False).\
            filter(expected_closing_date__range=(report.start_date, report.end_date)).\
            values('status', 'employee__user__first_name', 'employee__user__last_name').\
            annotate(total=Count('status'), sum=Sum('expected_revenue')).order_by('status')
        for employee_result in employee_results:
            name = employee_result['employee__user__first_name'] + ' ' + employee_result['employee__user__last_name']
            if employee_summary.get(name, '') == '':
                employee_summary[name] = {}
            employee_summary[name][employee_result['status']] = employee_result['total']
            employee_summary[name]['revenue_' + employee_result['status']] = employee_result['sum']
        meta['employee'] = employee
        meta['summary'] = summary
        meta['employee_summary'] = employee_summary

    return meta

def generate_deal_report(report):
    basename = 'deal' + str(report.start_date.strftime('%d%B%Y')) + '-' + str(report.end_date.strftime('%d%B%Y')) + '-' + str(report.entity) + str(uuid.uuid4())
    filename = basename + '.csv'

    meta = generate_deal_meta(report)
    generate_deal_csv(report, filename)

    csv_s3_url = upload_to_s3(filename)

    report.meta = meta
    report.url = csv_s3_url
    report.status = ReportConstant.DONE
    report.save()

    os.remove(filename)
    return

def generate_report(pk):
    report = Report.objects.get(pk=pk)
    report_type = report.type
    report.status = ReportConstant.PROGRESS
    if report_type == ReportConstant.LEAD:
        generate_lead_report(report)
    elif report_type == ReportConstant.TASK:
        generate_task_report(report)
    elif report_type == ReportConstant.EVENT:
        generate_event_report(report)
    elif report_type ==  ReportConstant.DEAL:
        generate_deal_report(report)
    return