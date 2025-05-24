from cim_to_linkml.cim18.linkml.cardinality.generate import is_slot_required, is_slot_multivalued
from cim_to_linkml.cim18.linkml.slot.model import Slot as LinkMLSlot
from cim_to_linkml.cim18.linkml.type_.generate import generate_curie
from cim_to_linkml.cim18.uml.project.model import Project as UMLProject
from cim_to_linkml.cim18.uml.relation.model import Relation as UMLRelation


def generate_relation_slots(uml_relation: UMLRelation, uml_project: UMLProject) -> tuple[LinkMLSlot, LinkMLSlot]:
    source_class = uml_project.classes[uml_relation.source_class]
    dest_class = uml_project.classes[uml_relation.dest_class]

    source_slot_name = f"{source_class.name}.{uml_relation.dest_role or dest_class.name}"
    dest_slot_name = f"{dest_class.name}.{uml_relation.source_role or source_class.name}"

    source_slot = LinkMLSlot(
        description=uml_relation.dest_role_note,
        slot_uri=generate_curie(f"{source_class.name}.{uml_relation.dest_role or dest_class.name}"),
        range=dest_class.name,
        required=is_slot_required(uml_relation.dest_card.lower_bound),
        multivalued=is_slot_multivalued(uml_relation.dest_card.upper_bound),
        in_subset=[uml_project.packages[source_class.package].name],
        annotations={"ea_guid": uml_relation.id},
        inverse=dest_slot_name,
        alias=uml_relation.dest_role or dest_class.name,
    )
    source_slot._name = source_slot_name

    dest_slot = LinkMLSlot(
        description=uml_relation.source_role_note,
        slot_uri=generate_curie(f"{dest_class.name}.{uml_relation.source_role or source_class.name}"),
        range=source_class.name,
        required=is_slot_required(uml_relation.source_card.lower_bound),
        multivalued=is_slot_multivalued(uml_relation.source_card.upper_bound),
        in_subset=[uml_project.packages[dest_class.package].name],
        annotations={"ea_guid": uml_relation.id},
        inverse=source_slot_name,
        alias=uml_relation.source_role or source_class.name,
    )
    dest_slot._name = dest_slot_name

    return source_slot, dest_slot

    # alias: str | None = Field(None)
