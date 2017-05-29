from tasks.models import *
from tasks.constants import *
from events.models import *
from leads.models import *
from leads.constants import *
from deals.models import *
from deals.constants import *
def get_summary(entity_id):
    open_task = Task.objects.filter(entity=entity_id).filter(is_deleted=False).filter(status=TaskConstant.OPEN).count()
    open_event = Event.objects.filter(entity=entity_id).filter(is_deleted=False).filter(start_time__gte=timezone.now()).count()
    open_lead = Lead.objects.filter(entity=entity_id).filter(is_deleted=False).filter(status=LeadConstant.OPEN).count()
    open_deal = Deal.objects.filter(entity=entity_id).filter(is_deleted=False).filter(status=DealConstant.OPEN).count()

    result = {'open_task': open_task, 'open_event': open_event, 'open_lead': open_lead, 'open_deal': open_deal}
    return result