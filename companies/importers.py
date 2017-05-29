from companies.models import *
from django.db import transaction
import csv

#This is poorly written, need to be rewrite in the future
class CompanyModelImporter():
    FIELDS = ['name', 'industry', 'employee_num', 'annual_revenue']

    FIELDS = ['name', 'phone', 'email', 'fax', 'industry', 'company_website', 'billing_street', 'billing_city', 'billing_state',
              'billing_country', 'billing_pos_code', 'shipping_street', 'shipping_city', 'shipping_state',
              'shipping_country', 'shipping_pos_code']

    def __init__(self, entity, employee, fields=FIELDS):
        self.entity = entity
        self.employee = employee
        self.fields = fields

    @transaction.atomic
    def import_data(self, file_data):
        is_header = True
        companies = []
        reader = csv.reader(file_data)
        column_mapping = {}
        for row in reader:
            if is_header:
                for field in self.fields:
                    column_mapping[field] = row.index(field)
                is_header = False
                continue
            name = row[column_mapping['name']] or ''
            phone = row[column_mapping['phone']] or ''
            email = row[column_mapping['email']] or ''
            fax = row[column_mapping['fax']] or ''
            industry = row[column_mapping['industry']] or ''
            company_website = row[column_mapping['company_website']] or ''

            street = row[column_mapping['billing_street']] or ''
            city = row[column_mapping['billing_city']] or ''
            state = row[column_mapping['billing_state']] or ''
            country = row[column_mapping['billing_country']] or ''
            pos_code = row[column_mapping['billing_pos_code']] or ''

            shipping_street = row[column_mapping['shipping_street']] or ''
            shipping_city = row[column_mapping['shipping_city']] or ''
            shipping_state = row[column_mapping['shipping_state']] or ''
            shipping_country = row[column_mapping['shipping_country']] or ''
            shipping_pos_code = row[column_mapping['shipping_pos_code']] or ''

            company = Company.objects.create(name=name, phone=phone, email=email, fax=fax, industry=industry,
                            company_website=company_website, street=street, city=city, state=state, country=country, pos_code=pos_code,
                            shipping_street=shipping_street ,shipping_city=shipping_city, shipping_state=shipping_state,
                            shipping_country=shipping_country, shipping_pos_code=shipping_pos_code,
                            entity=self.entity, employee=self.employee)
            companies.append(company)

        return companies