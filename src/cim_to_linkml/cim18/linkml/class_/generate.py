from cim_to_linkml.cim18.linkml.cardinality.generate import is_slot_required, is_slot_multivalued
from cim_to_linkml.cim18.linkml.class_.model import Class as LinkMLClass
from cim_to_linkml.cim18.linkml.generate import generate_curie
from cim_to_linkml.cim18.linkml.slot.model import Slot as LinkMLSlot
from cim_to_linkml.cim18.linkml.type_.generate import map_primitive_data_type
from cim_to_linkml.cim18.uml.class_.model import Attribute as UMLAttribute, ClassStereotype
from cim_to_linkml.cim18.uml.class_.model import Class as UMLClass


def generate_attribute(uml_attribute: UMLAttribute, uml_class: UMLClass) -> LinkMLSlot:
    return LinkMLSlot(
        name=uml_attribute.name,
        range=map_primitive_data_type(uml_attribute.type) if uml_attribute.type .stereotype == ClassStereotype.PRIMITIVE .type else None,
        description=uml_attribute.notes,
        required=is_slot_required(uml_attribute.multiplicity.lower_bound),
        multivalued=is_slot_multivalued(uml_attribute.multiplicity.lower_bound),
        slot_uri=generate_curie(f"{uml_class.name}.{uml_attribute.name}"),
    )


def generate_class(uml_class: UMLClass) -> LinkMLClass:
    return LinkMLClass(
        name=uml_class.name,
        description=uml_class.note,
        annotations={"ea_guid": str(uml_class.id)},
        attributes={attr.name: generate_attribute(attr, uml_class) for attr in uml_class.attributes.values()},
    )