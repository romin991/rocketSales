class ReportConstant(object):
    LEAD = 'L'
    TASK = 'T'
    EVENT = 'E'
    DEAL = 'DL'

    QUEUE = 'Q'
    PROGRESS = 'P'
    DONE = 'D'
    ERROR = 'E'

    REPORT_TYPE = (
        (LEAD, 'Lead'),
        (TASK, 'Task'),
        (EVENT, 'Event'),
        (DEAL, 'Deal'),
    )

    REPORT_STATUS = (
        (QUEUE, 'Queue'),
        (PROGRESS, 'Progress'),
        (DONE, 'Done'),
        (ERROR, 'Error'),
    )