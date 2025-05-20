from itertools import groupby
from operator import itemgetter
from typing import Iterator

from cim_to_linkml.cim18.uml.class_.model import Attribute, AttributeStereotype, AttributeID, Class, ClassStereotype
from cim_to_linkml.cim18.uml.multiplicity.parse import parse_multiplicity_val
from cim_to_linkml.cim18.uml.utils import parse_iso_datetime_val


def parse_uml_class_attribute(attr: dict) -> Attribute:
    try:
        stereotype = AttributeStereotype(attr["attr_stereotype"])
    except ValueError:
        stereotype = None

    return Attribute(
        id=int(attr["attr_id"]),
        class_=int(attr["class_id"]),
        name=attr["attr_name"],
        lower_bound=parse_multiplicity_val(attr["attr_lower_bound"]),
        upper_bound=parse_multiplicity_val(attr["attr_upper_bound"]),
        type=attr["attr_type"],
        default=attr["attr_default"],
        notes=attr["attr_notes"],
        stereotype=stereotype,
    )

def parse_uml_attributes(rows: list[dict]) -> dict[AttributeID, Attribute]:
    return {attr_id: parse_uml_class_attribute(attr)
            for _, attr_ in groupby(rows, itemgetter("attr_name"))
            if (attr := next(attr_))
            if attr["attr_id"] is not None
            if (attr_id := int(attr["attr_id"]))}


# TODO: Improve type signature. `Iterator` says too little.
def parse_uml_class(class_rows: Iterator) -> Class:
    class_rows = [dict(row) for row in class_rows]  # Materialize.

    try:
        stereotype = ClassStereotype(class_rows[0]["class_stereotype"])
    except ValueError:
        stereotype = None

    return Class(
        id=int(class_rows[0]["class_id"]),
        name=class_rows[0]["class_name"],
        author=class_rows[0]["class_author"],
        package=int(class_rows[0]["class_package_id"]),
        attributes=parse_uml_attributes(class_rows),
        created_date=parse_iso_datetime_val(class_rows[0]["class_created_date"]),
        modified_date=parse_iso_datetime_val(class_rows[0]["class_modified_date"]),
        note=class_rows[0]["class_note"],
        stereotype=stereotype,
    )
