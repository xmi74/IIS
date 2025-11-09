from enum import Enum

class ScheduleState(Enum):
    FREE = 'Free'
    RESERVED = 'Reserved'
    CONFIRMED = 'Confirmed'
    IN_PROGRESS = 'In Progress'
    COMPLETED = 'Completed'