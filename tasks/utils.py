from tasks.constants import *

def create_task_verb(created, status):
    verb = 'updated'
    if created:
        verb = 'created'

    if status == TaskConstant.CLOSED:
        verb = 'closed'

    return verb