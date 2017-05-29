from customers.models import *
from leads.models import *
from django.conf import settings
from deals.models import *
import threading
from django.core.mail import send_mail

def get_model_meta():
    model_dict = {}
    customer_object_name = Customer._meta.object_name.lower()
    lead_object_name = Lead._meta.object_name.lower()
    company_object_name = Company._meta.object_name.lower()
    task_object_name = Task._meta.object_name.lower()
    event_object_name = Event._meta.object_name.lower()
    deal_object_name = Deal._meta.object_name.lower()
    model_dict[customer_object_name] = ContentType.objects.get(model=customer_object_name).id
    model_dict[lead_object_name] = ContentType.objects.get(model=lead_object_name).id
    model_dict[company_object_name] = ContentType.objects.get(model=company_object_name).id
    model_dict[task_object_name] = ContentType.objects.get(model=task_object_name).id
    model_dict[event_object_name] = ContentType.objects.get(model=event_object_name).id
    model_dict[deal_object_name] = ContentType.objects.get(model=deal_object_name).id
    return model_dict

def get_cloudinary_meta():
    cloudinary_dict = {}
    params = getattr(settings, 'CLOUDINARY', None)
    cloudinary_dict['endpoint'] = params['ENDPOINT']
    cloudinary_dict['preset'] = params['PRESET']

    return cloudinary_dict

class EmailThread(threading.Thread):
    def __init__(self, name, email, phone, message):
        threading.Thread.__init__(self)
        self.name = name
        self.email = email
        self.phone = phone
        self.message = message

    def run(self):
        SUBJECT = 'Hi from ' + self.name + '(' + self.email + ', ' + self.phone + ')'
        my_email = 'hello@zahaya.com'
        send_mail(SUBJECT, self.message , my_email, [my_email], fail_silently=False)