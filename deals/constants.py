class DealConstant(object):
    OPEN = 'O'
    PROGRESS = 'P'
    CLOSED_WON = 'CW'
    CLOSED_LOST = 'CL'

    DEAL_STATUS = (
        (OPEN, 'Open'),
        (PROGRESS, 'Progress'),
        (CLOSED_WON, 'ClosedWon'),
        (CLOSED_LOST, 'ClosedLost'),
    )