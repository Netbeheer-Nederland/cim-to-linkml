import sqlite3
import textwrap


def read_uml_classes(conn: sqlite3.Connection) -> sqlite3.Cursor:
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    query = textwrap.dedent(
        """
        SELECT
            Class.Object_ID AS class_id,
            Class.Name AS class_name,
            Class.Author AS class_author,
            Class.Package_ID AS class_package_id,
            Class.CreatedDate AS class_created_date,
            Class.ModifiedDate AS class_modified_date,
            Class.Stereotype AS class_stereotype,
            Class.Note AS class_note,
            Attribute.ID AS attr_id,
            Attribute.Name AS attr_name,
            Attribute.LowerBound AS attr_lower_bound,
            Attribute.UpperBound AS attr_upper_bound,
            Attribute.Type AS attr_type,
            Attribute.Notes AS attr_notes,
            Attribute.Stereotype AS attr_stereotype,
            Attribute."Default" AS attr_default
        FROM t_object AS Class

        LEFT JOIN t_attribute AS Attribute
        ON Class.Object_ID = Attribute.Object_ID

        WHERE Class.Object_Type = "Class"

        ORDER BY Class.Object_ID, Attribute.Name
        """
    )
    rows = cur.execute(query)

    return rows
