from typing import Iterator

from cim_to_linkml.cim18.uml.class_.model import Attribute, Attributes, AttributeStereotype, Class, ClassStereotype
from cim_to_linkml.cim18.uml.multiplicity.model import Multiplicity
from cim_to_linkml.cim18.uml.multiplicity.parse import parse_multiplicity_val
from cim_to_linkml.cim18.uml.type_.parse import parse_iso_datetime_val


def parse_uml_class_attribute(attr: dict) -> Attribute:
    return Attribute(
        class_=attr["class_id"],
        id=attr["attr_id"],
        name=attr["attr_name"],
        type=attr["attr_type"],
        multiplicity=Multiplicity(lower_bound=parse_multiplicity_val(attr["attr_lower_bound"]),
                                  upper_bound=parse_multiplicity_val(attr["attr_upper_bound"])),
        default=attr["attr_default"],
        notes=attr["attr_notes"],
        stereotype=AttributeStereotype(attr["attr_stereotype"]),
    )


# TODO: Improve type signature. `Iterator` says too little.
def parse_uml_class(class_rows: Iterator) -> Class:
    class_rows = [dict(row) for row in class_rows]  # Materialize.

    # TODO: Fix false positive type check error.
    return Class(
        id=class_rows[0]["class_id"],
        name=class_rows[0]["class_name"],
        package=class_rows[0]["class_package_id"],
        attributes=Attributes({attr["attr_id"]: parse_uml_class_attribute(attr)
                    for attr in class_rows
                    if attr["attr_id"] is not None}),
        created_date=parse_iso_datetime_val(class_rows[0]["class_created_date"]),
        modified_date=parse_iso_datetime_val(class_rows[0]["class_modified_date"]),
        author=class_rows[0]["class_author"],
        note=class_rows[0]["class_note"],
        stereotype=ClassStereotype(class_rows[0]["class_stereotype"]),
    )
