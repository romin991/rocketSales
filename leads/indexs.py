from algolias.models import AlgoliaIndex
from leads.serializers import *

class LeadIndex(AlgoliaIndex):
    serializer = LeadAlgoliaSerializer
    settings = {'attributesToIndex': ['first_name', 'last_name', 'email', 'phone', 'company_name'],
                'customRanking': ['desc(epoch_created_at)'],
                'attributesForFaceting': ['status']}