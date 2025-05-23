# import cProfile
import logging
import os
import sqlite3
from pathlib import Path

import click

from cim_to_linkml.cim18.linkml.schema.generate import generate_schema
from cim_to_linkml.cim18.linkml.writer import init_yaml_serializer, write_schema
from cim_to_linkml.cim18.uml.class_.read import read_uml_classes
from cim_to_linkml.cim18.uml.package.read import read_uml_packages
from cim_to_linkml.cim18.uml.project.parse import parse_uml_project
from cim_to_linkml.cim18.uml.relation.read import read_uml_relations

LOG_FORMAT = "[%(asctime)s] [%(levelname)s] %(message)s"  # noqa

logger = logging.getLogger(__name__)
logging.basicConfig(format=LOG_FORMAT)

init_yaml_serializer()


def _generate_linkml_schema(cim_db, output_dir):
    """Generates LinkML schemas from the supplied Sparx EA QEA database file."""

    # Parse.
    with sqlite3.connect(cim_db) as conn:
        uml_project = parse_uml_project(read_uml_packages(conn), read_uml_classes(conn), read_uml_relations(conn))

    # Generate.
    linkml_schema = generate_schema(uml_project)

    # Write.
    os.makedirs(output_dir, exist_ok=True)
    schema_path = os.path.join(output_dir, "CIM") + ".yml"
    write_schema(linkml_schema, schema_path)


@click.command()
@click.argument("cim_db", type=click.Path(exists=True, path_type=Path), nargs=1, metavar="QEA_FILE")
@click.option(
    "--output-dir",
    "-o",
    default=Path("schemas"),
    show_default=True,
    type=click.Path(path_type=Path),
    help="Directory where schemas will be outputted.",
)
def generate_linkml_schema(cim_db, output_dir):
    """Generates LinkML schemas from the supplied Sparx EA QEA database file."""

    return _generate_linkml_schema(cim_db, output_dir)


if __name__ == "__main__":
    # cProfile.run("main()", sort="tottime")  # noqa
    cim18_db = (
        "/home/bart/Programming/Netbeheer-Nederland/cim-to-linkml/data/CIM_Grid18v10_Support14v00_Market04v14.qea"
    )
    generate_linkml_schema.main([cim18_db, "-o", "../../../schemas"])
