from customers.models import *
from customers.indexs import *
from leads.models import *
from leads.indexs import *
from companies.models import *
from companies.indexs import *
from tasks.models import *
from tasks.indexs import *
from events.indexs import *
from deals.index import *

class AlgoliaConstant(object):
    MODEL_DICT = {Customer._meta.object_name: CustomerIndex, Lead._meta.object_name: LeadIndex,
                  Company._meta.object_name: CompanyIndex, Task._meta.object_name: TaskIndex,
                  Event._meta.object_name: EventIndex, Deal._meta.object_name: DealIndex}