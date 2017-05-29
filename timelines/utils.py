import datetime


def model_content_type(cls):
    return '%s.%s' % (cls._meta.app_label, cls._meta.object_name)

def model_type(cls):
    return '%s' % (cls._meta.object_name)


def build_timeline_dict(object, verb, action, employee, time=datetime.datetime.now()):
    object_type = model_type(object)
    object_content_type = model_content_type(object)
    object_title = object.get_timeline_title()
    object_id = str(object.id)

    action_type = model_type(action)
    action_content_type = model_content_type(action)
    action_title = action.get_timeline_title()
    action_id = str(action.id)

    employee_title = employee.get_timeline_title()
    employee_id = str(employee.pk)

    timeline = dict(
        object_type=object_type,
        object_content_type=object_content_type,
        object_title=object_title,
        object_id=object_id,
        action_type=action_type,
        action_content_type=action_content_type,
        action_title=action_title,
        action_id=action_id,
        employee_title=employee_title,
        employee_id=employee_id,
        verb=verb,
        time=str(time)
    )
    return timeline

def create_timeline(instance, contact, verb, action, employee):
    if instance:
        instance_timeline = instance.timeline.first()
        instance_timeline.add_timeline_content(contact, verb, action, employee)