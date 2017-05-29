from algolias.models import AlgoliaIndex
from customers.serializers import *

class CustomerIndex(AlgoliaIndex):
    serializer = CustomerAlgoliaSerializer
    settings = {'attributesToIndex': ['first_name', 'last_name', 'email', 'phone', 'company_name'],
                'customRanking': ['desc(epoch_created_at)']}