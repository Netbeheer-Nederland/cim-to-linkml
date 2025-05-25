import sqlite3
import textwrap


def read_uml_packages(conn: sqlite3.Connection) -> sqlite3.Cursor:
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    query = textwrap.dedent(
        """
        SELECT
            Package.Package_ID AS id,
            Package.Name AS name,
            Package.Parent_ID AS parent_id,
            Package.CreatedDate AS created_date,
            Package.ModifiedDate AS modified_date,
            Package.Notes AS note,
            Object.author as author,
            Package.ea_guid AS ea_guid,
            Version."Default" AS version
        FROM t_package AS Package

        LEFT JOIN t_object AS Object
        ON Package.Package_ID = Object.Object_ID
        AND Object.Object_Type = "Package"

        LEFT JOIN t_object AS VersionClass
        ON Package.Package_ID = VersionClass.Package_ID
        AND VersionClass.Name LIKE '%Version'

        LEFT JOIN t_attribute AS Version
        ON VersionClass.Object_ID = Version.Object_ID
        AND Version.Name = 'version'

        ORDER BY id
        """
    )
    rows = cur.execute(query)

    return rows