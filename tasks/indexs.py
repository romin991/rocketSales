from algolias.models import AlgoliaIndex
from tasks.serializers import *

class TaskIndex(AlgoliaIndex):
    serializer = TaskAlgoliaSerializer
    settings = {'attributesToIndex': ['subject', 'contact_first_name', 'contact_last_name',
                                      'contact_email', 'contact_phone', 'company_name', 'deal_name'],
                'customRanking': ['asc(epoch_due_date)', 'desc(epoch_created_at)'],
                'attributesForFaceting': ['status']}