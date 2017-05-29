from leads.models import *
from leads.constants import *

def get_summary(entity_id):
    active_lead = Lead.objects.filter(entity=entity_id).filter(is_deleted=False)
    open_lead = active_lead.filter(status=LeadConstant.OPEN).count()
    converted_lead = active_lead.filter(status=LeadConstant.CONVERTED).count()
    closed_lead = active_lead.filter(status=LeadConstant.CLOSED).count()

    result = {'open_lead': open_lead, 'converted_lead': converted_lead, 'closed_lead': closed_lead}
    return result