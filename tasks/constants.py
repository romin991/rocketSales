class TaskConstant(object):
    OPEN = 'O'
    CLOSED = 'C'
    PROGRESS= 'P'
    HIGH = 'H'
    MEDIUM = 'M'
    LOW = 'L'

    TASK_PRIORITY = (
        (HIGH, 'High'),
        (MEDIUM, 'Medium'),
        (LOW, 'Low'),
    )

    TASK_STATUS = (
        (OPEN, 'Open'),
        (PROGRESS, 'Progress'),
        (CLOSED, 'Closed'),
    )
