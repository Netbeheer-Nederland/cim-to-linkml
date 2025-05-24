from cim_to_linkml.cim18.linkml.cardinality.generate import is_slot_required, is_slot_multivalued
from cim_to_linkml.cim18.linkml.class_.model import Class as LinkMLClass
from cim_to_linkml.cim18.linkml.model import EnumName as LinkMLEnumName, TypeName as LinkMLTypeName
from cim_to_linkml.cim18.linkml.slot.model import Slot as LinkMLSlot
from cim_to_linkml.cim18.linkml.type_.generate import (
    map_primitive_datatype,
    PrimitiveType as LinkMLPrimitiveType,
    generate_curie,
)
from cim_to_linkml.cim18.uml.class_.model import Attribute as UMLAttribute, ClassStereotype as UMLClassStereotype
from cim_to_linkml.cim18.uml.class_.model import Class as UMLClass
from cim_to_linkml.cim18.uml.project.model import Project as UMLProject
from cim_to_linkml.cim18.uml.type_.model import CIMPrimitive


def _generate_attribute_range(
    uml_attribute: UMLAttribute, uml_project: UMLProject
) -> LinkMLPrimitiveType | LinkMLEnumName | LinkMLTypeName:
    uml_attribute_type_class = uml_project.classes.by_name(uml_attribute.type)

    match uml_attribute_type_class.stereotype:
        case UMLClassStereotype.PRIMITIVE:
            range_ = map_primitive_datatype(CIMPrimitive(uml_attribute.type)).value
        case UMLClassStereotype.ENUMERATION | UMLClassStereotype.CIM_DATATYPE | UMLClassStereotype.COMPOUND:
            range_ = uml_attribute.type
        case _:
            raise TypeError("Range of class attribute must be either a primitive, a CIM data type, or an enumeration.")

    return range_


def generate_attribute(uml_attribute: UMLAttribute, uml_project: UMLProject) -> LinkMLSlot:
    uml_owning_class = uml_project.classes[uml_attribute.class_]

    linkml_slot = LinkMLSlot(
        slot_uri=generate_curie(f"{uml_owning_class.name}.{uml_attribute.name}"),
        range=_generate_attribute_range(uml_attribute, uml_project),
        description=uml_attribute.notes,
        required=is_slot_required(uml_attribute.multiplicity.lower_bound),
        multivalued=is_slot_multivalued(uml_attribute.multiplicity.lower_bound),
    )

    return linkml_slot


def generate_class(uml_class: UMLClass, uml_project: UMLProject) -> LinkMLClass:
    uml_package_name = uml_project.packages[uml_class.package].name
    linkml_class = LinkMLClass(
        class_uri=generate_curie(f"{uml_class.name}"),
        is_a=None,  # NOTE: Filled later when generating relations.
        description=uml_class.note,
        annotations={"ea_guid": uml_class.id},
        attributes={attr.name: generate_attribute(attr, uml_project) for attr in uml_class.attributes.values()},
        in_subset=[
            uml_package_name
        ],  # NOTE: Just the immediate package, not the ancestors. That can be derived by logic.
    )
    linkml_class._name = uml_class.name

    return linkml_class
