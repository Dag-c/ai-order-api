from enum import Enum

class OrderStatus(str, Enum):

    PENDING = "PENDING"

    PREPARING = "PREPARING"

    DELIVERING = "DELIVERING"