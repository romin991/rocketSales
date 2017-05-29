from deals.constants import *
from deals.models import *

def create_deal_verb(created, status):
    verb = 'updated'
    if created:
        verb = 'created'

    if status == DealConstant.CLOSED_WON:
        verb = 'won'
    elif status == DealConstant.CLOSED_LOST:
        verb = 'lost'

    return verb

def get_summary(entity_id):
    active_deal = Deal.objects.filter(entity=entity_id).filter(is_deleted=False)
    open_deal = active_deal.filter(status=DealConstant.OPEN).count()
    progress_deal = active_deal.filter(status=DealConstant.PROGRESS).count()
    won_deal = active_deal.filter(status=DealConstant.CLOSED_WON).count()
    lost_deal = active_deal.filter(status=DealConstant.CLOSED_LOST).count()

    result = {'open_deal': open_deal, 'progress_deal': progress_deal, 'won_deal': won_deal, 'lost_deal': lost_deal}
    return result