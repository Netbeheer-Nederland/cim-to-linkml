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
            Class.Package_ID AS class_package_id,
            Attribute.ID AS attr_id,
            Attribute.Name AS attr_name,
            Attribute.Type AS attr_type,
            Attribute.LowerBound AS attr_lower_bound,
            Attribute.UpperBound AS attr_upper_bound,
            Attribute."Default" AS attr_default,
            Attribute.Notes AS attr_notes,
            Attribute.Stereotype AS attr_stereotype,
            Class.CreatedDate AS class_created_date,
            Class.ModifiedDate AS class_modified_date,
            Class.Author AS class_author,
            Class.Note AS class_note,
            Class.Stereotype AS class_stereotype
        FROM t_object AS Class

        LEFT JOIN t_attribute AS Attribute
        ON Class.Object_ID = Attribute.Object_ID

        WHERE Class.Object_Type = "Class"
        AND (Class.Stereotype IN ("CIMDatatype", "Primitive", "enumeration", "Compound")
            OR Class.Stereotype IS NULL)
        AND (Attribute.Stereotype == "enum"
            OR Attribute.Stereotype IS NULL)

        ORDER BY Class.Object_ID, Attribute.Name
        """
    )
    rows = cur.execute(query)

    return rows
