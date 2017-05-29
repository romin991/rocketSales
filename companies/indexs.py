from algolias.models import AlgoliaIndex
from companies.serializers import *

class CompanyIndex(AlgoliaIndex):
    serializer = CompanyAlgoliaSerializer
    settings = {'attributesToIndex': ['name'],
                'customRanking': ['desc(epoch_created_at)']}