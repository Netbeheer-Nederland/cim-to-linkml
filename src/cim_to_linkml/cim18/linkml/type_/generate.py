from cim_to_linkml.cim18.linkml.type_.model import Enum as LinkMLType
from cim_to_linkml.cim18.linkml.type_.model import PrimitiveType
from cim_to_linkml.cim18.uml.class_.model import Class as UMLClass
from cim_to_linkml.cim18.uml.type_.model import CIMPrimitive


def map_primitive_data_type(val: CIMPrimitive):
    try:
        return {
            CIMPrimitive.FLOAT: PrimitiveType.FLOAT,
            CIMPrimitive.INTEGER: PrimitiveType.INTEGER,
            CIMPrimitive.DATETIME: PrimitiveType.DATE,
            CIMPrimitive.STRING: PrimitiveType.STRING,
            CIMPrimitive.BOOLEAN: PrimitiveType.BOOLEAN,
            CIMPrimitive.DECIMAL: PrimitiveType.DOUBLE,  # Is this right?
            CIMPrimitive.MONTHDAY: PrimitiveType.DATE,  # Is this right?
            CIMPrimitive.DATE: PrimitiveType.DATE,
            CIMPrimitive.TIME: PrimitiveType.TIME,
            CIMPrimitive.DURATION: PrimitiveType.INTEGER,
            CIMPrimitive.IRI: PrimitiveType.IRI,
        }[val]
    except KeyError:
        raise TypeError(f"Data type `{val}` is not a CIM Primitive.")


def generate_type(uml_class: UMLClass) -> LinkMLType:
    ...
