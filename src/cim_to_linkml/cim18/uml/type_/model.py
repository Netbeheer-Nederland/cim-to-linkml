from enum import Enum


class CIMPrimitive(Enum):
    FLOAT = "Float"
    INTEGER = "Integer"
    DATETIME = "DateTime"
    STRING = "String"
    BOOLEAN = "Boolean"
    DECIMAL = "Decimal"
    MONTHDAY = "MonthDay"
    DATE = "Date"
    TIME = "Time"
    DURATION = "Duration"
    IRI = "IRI"