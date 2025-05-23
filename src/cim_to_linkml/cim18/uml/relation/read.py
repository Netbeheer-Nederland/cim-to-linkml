import sqlite3
import textwrap


def read_uml_relations(conn: sqlite3.Connection) -> sqlite3.Cursor:
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    query = textwrap.dedent(
        """
        SELECT
            Relation.Connector_ID AS relation_id,
            Relation.Connector_Type AS relation_type,
            Relation.Start_Object_ID AS relation_start_object_id,
            Relation.End_Object_ID AS relation_end_object_id,
            Relation.Direction AS relation_direction,
            Relation.SourceRole AS relation_source_role,
            Relation.SourceRoleNote AS relation_source_role_note,
            Relation.SourceCard AS relation_source_card,
            Relation.DestRole AS relation_dest_role,
            Relation.DestRoleNote AS relation_dest_role_note,
            Relation.DestCard AS relation_dest_card
        FROM t_connector AS Relation
        
        LEFT JOIN t_object AS SourceClass
        ON Relation.Start_Object_ID = SourceClass.Object_ID
        
        LEFT JOIN t_object AS DestClass
        ON Relation.End_Object_ID = DestClass.Object_ID

        WHERE relation_type IN ("Aggregation", "Association", "Generalization")
        AND SourceClass.Stereotype IN ("CIMDatatype", "Primitive", "enumeration", "Compound")
        AND DestClass.Stereotype IN ("CIMDatatype", "Primitive", "enumeration", "Compound")

        ORDER BY relation_id
        """
    )
    rows = cur.execute(query)

    return rows