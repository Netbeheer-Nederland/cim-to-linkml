import sqlite3
import textwrap


def read_uml_relations(conn: sqlite3.Connection) -> sqlite3.Cursor:
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    query = textwrap.dedent(
        """
        SELECT
            Relation.Connector_ID AS id,
            Relation.Connector_Type AS type,
            Relation.Start_Object_ID AS start_object_id,
            Relation.End_Object_ID AS end_object_id,
            Relation.Direction AS direction,
            Relation.SourceRole AS source_role,
            Relation.SourceRoleNote AS source_role_note,
            Relation.SourceCard AS source_card,
            Relation.DestRole AS dest_role,
            Relation.DestRoleNote AS dest_role_note,
            Relation.DestCard AS dest_card
        FROM t_connector AS Relation
        
        LEFT JOIN t_object AS SourceClass
        ON Relation.Start_Object_ID = SourceClass.Object_ID
        
        LEFT JOIN t_object AS DestClass
        ON Relation.End_Object_ID = DestClass.Object_ID

        -- See: `Rule075` and `Rule119`
        WHERE type IN ("Aggregation", "Association", "Generalization")
        AND SourceClass.Stereotype IS NULL
        AND DestClass.Stereotype IS NULL

        ORDER BY id
        """
    )
    rows = cur.execute(query)

    return rows
