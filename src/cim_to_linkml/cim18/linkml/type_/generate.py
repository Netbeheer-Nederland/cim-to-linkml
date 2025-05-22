from cim_to_linkml.cim18.linkml.type_.model import Enum as LinkMLType
from cim_to_linkml.cim18.uml.class_.model import Class as UMLClass


def map_primitive_data_type(val):
    try:
        return {
            "Float": "float",
            "Integer": "integer",
            "DateTime": "date",
            "String": "string",
            "Boolean": "boolean",
            "Decimal": "double",  # Is this right?
            "MonthDay": "date",  # Is this right?
            "Date": "date",
            "Time": "time",
            "Duration": "integer",
        }[val]
    except KeyError:
        raise TypeError(f"Data type `{val}` is not a CIM Primitive.")


def generate_type(uml_class: UMLClass) -> LinkMLType:
    ...
