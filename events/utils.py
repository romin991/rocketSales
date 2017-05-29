
def create_event_verb(created):
    verb = 'updated'
    if created:
        verb = 'created'

    return verb