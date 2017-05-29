from leads.models import *
from django.db import transaction
import csv

#This is poorly written, need to be rewrite in the future
class LeadModelImporter():
    FIELDS = ['first_name', 'last_name', 'company_name', 'phone', 'mobile_phone', 'email', 'fax', 'position',
              'street', 'city', 'state', 'country', 'pos_code']

    def __init__(self, entity, employee, fields=FIELDS):
        self.entity = entity
        self.employee = employee
        self.fields = fields

    @transaction.atomic
    def import_data(self, file_data):
        is_header = True
        leads = []
        reader = csv.reader(file_data)
        column_mapping = {}
        for row in reader:
            if is_header:
                for field in self.fields:
                    column_mapping[field] = row.index(field)
                is_header = False
                continue
            first_name = row[column_mapping['first_name']] or ''
            last_name = row[column_mapping['last_name']] or ''
            company_name = row[column_mapping['company_name']] or ''
            phone = row[column_mapping['phone']] or ''
            mobile_phone = row[column_mapping['mobile_phone']] or ''
            email = row[column_mapping['email']] or ''
            fax = row[column_mapping['fax']] or ''
            position = row[column_mapping['position']] or ''

            street = row[column_mapping['street']] or ''
            city = row[column_mapping['city']] or ''
            state = row[column_mapping['state']] or ''
            country = row[column_mapping['country']] or ''
            pos_code = row[column_mapping['pos_code']] or ''

            lead = Lead.objects.create(first_name=first_name, last_name=last_name, company_name=company_name, phone=phone,
                            mobile_phone=mobile_phone, email=email, fax=fax, position=position, street=street, city=city,
                            state=state, country=country, pos_code=pos_code, entity=self.entity, employee=self.employee)
            leads.append(lead)

        return leads


