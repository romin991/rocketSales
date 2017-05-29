from algolias.models import AlgoliaIndex
from events.serializers import *

class EventIndex(AlgoliaIndex):
    serializer = EventAlgoliaSerializer
    settings = {'attributesToIndex': ['subject', 'contact_first_name', 'contact_last_name',
                                      'contact_email', 'contact_phone', 'company_name', 'deal_name'],
                'customRanking': ['asc(epoch_start_time)']}