from enum import IntEnum


class OrderStatus(IntEnum):
    OPEN = 1
    PENDING = 2
    CANCELLED = 3
    ACCEPTED = 4
    DELIVERED = 5

    @classmethod
    def choices(cls):
        return [(key.value, key.name.capitalize()) for key in cls]
