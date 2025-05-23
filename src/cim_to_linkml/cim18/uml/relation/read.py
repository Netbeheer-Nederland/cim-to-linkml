import sqlite3
import textwrap


def read_uml_relations(conn: sqlite3.Connection) -> sqlite3.Cursor:
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    query = textwrap.dedent(
        """
        SELECT
            Connector_ID AS id,
            Connector_Type AS type,
            Start_Object_ID AS start_object_id,
            End_Object_ID AS end_object_id,
            Direction AS direction,
            SourceRole AS source_role,
            SourceRoleNote AS source_role_note,
            SourceCard AS source_card,
            DestRole AS dest_role,
            DestRoleNote AS dest_role_note,
            DestCard AS dest_card
        FROM t_connector

        WHERE type IN ("Aggregation", "Association", "Generalization")

        ORDER BY id
        """
    )
    rows = cur.execute(query)

    return rows