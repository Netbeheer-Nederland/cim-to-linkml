import sqlite3

from cim_to_linkml.cim18.uml.multiplicity.parse import parse_multiplicity
from cim_to_linkml.cim18.uml.relation.model import Relation, RelationType, RelationDirection


def parse_uml_relation(relation_row: sqlite3.Cursor) -> Relation:
    uml_relation = dict(relation_row)

    try:
        direction = RelationDirection(uml_relation["direction"])
    except ValueError:
        direction = None

    return Relation(
        id=uml_relation["id"],
        type=RelationType(uml_relation["type"]),
        source_class=uml_relation["start_object_id"],
        dest_class=uml_relation["end_object_id"],
        direction=direction,
        source_card=parse_multiplicity(uml_relation["source_card"]),
        source_role=uml_relation["source_role"],
        source_role_note=uml_relation["source_role_note"],
        dest_card=parse_multiplicity(uml_relation["dest_card"]),
        dest_role=uml_relation["dest_role"],
        dest_role_note=uml_relation["dest_role_note"],
    )
