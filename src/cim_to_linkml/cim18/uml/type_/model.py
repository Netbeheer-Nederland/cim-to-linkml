from enum import Enum


class CIMPrimitive(Enum):
    Float = "float"
    Integer = "integer"
    DateTime = "date"
    String = "string"
    Boolean = "boolean"
    Decimal = "double"  # Is this right?
    MonthDay = "date"  # Is this right?
    Date = "date"
    Time = "time"
    Duration = "integer"