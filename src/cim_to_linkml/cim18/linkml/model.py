from enum import Enum
from urllib.parse import quote

type URI = str
type CURIE = str

CIM_PREFIX = "cim"
CIM_BASE_URI = "https://cim.ucaiug.io/ns#"
CIM_MODEL_LICENSE = "https://www.apache.org/licenses/LICENSE-2.0.txt"


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
