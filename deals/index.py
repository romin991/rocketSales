from algolias.models import AlgoliaIndex
from deals.serializers import *

class DealIndex(AlgoliaIndex):
    serializer = DealAlgoliaSerializer
    settings = {'attributesToIndex': ['name', 'customer_first_name', 'customer_last_name',
                                      'customer_email', 'customer_phone', 'company_name'],
                'customRanking': ['asc(epoch_expected_closing_date)', 'desc(epoch_created_at)'],
                'attributesForFaceting': ['status']}