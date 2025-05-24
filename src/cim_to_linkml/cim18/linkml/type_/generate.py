from urllib.parse import quote

from cim_to_linkml.cim18.linkml.model import CIM_PREFIX
from cim_to_linkml.cim18.linkml.type_.model import CIMDataType as LinkMLCIMDataType, UCUMCode, QuantityKind
from cim_to_linkml.cim18.linkml.type_.model import PrimitiveType, Unit
from cim_to_linkml.cim18.uml.class_.model import Class as UMLClass
from cim_to_linkml.cim18.uml.project.model import Project as UMLProject
from cim_to_linkml.cim18.uml.type_.model import CIMPrimitive, CIMUnitSymbol, CIMUnitMultiplier


def map_primitive_datatype(val: CIMPrimitive):
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


def map_cim_dt_to_ucum_code(unit: CIMUnitSymbol, multiplier: CIMUnitMultiplier) -> UCUMCode:
    ...


def map_cim_dt_to_quantity_kind(uml_class: UMLClass) -> QuantityKind:
    ...


def generate_unit(uml_class: UMLClass) -> Unit:
    return Unit(
        ucum_code=UCUMCode.DEG,
        has_quantity_kind=QuantityKind.ANGLEDEGREES
    )


def generate_cim_datatype(uml_class: UMLClass, uml_project: UMLProject) -> LinkMLCIMDataType:
    uml_package_name = uml_project.packages[uml_class.package].name

    linkml_datatype = LinkMLCIMDataType(
        description=uml_class.note,
        annotations={"ea_guid": uml_class.id},
        in_subset=[uml_package_name],
        uri=generate_curie(f"{uml_class.name}"),
        typeof=map_primitive_datatype(CIMPrimitive(uml_class.attributes.by_name("value").type)),
        unit=generate_unit(uml_class)
    )
    linkml_datatype._name = uml_class.name

    return linkml_datatype


def generate_curie(name: str, prefix: str = CIM_PREFIX) -> str:
    return f"{prefix}:{quote(name)}"
