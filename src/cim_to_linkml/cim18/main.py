# import cProfile
import logging
import os
import sqlite3
from itertools import chain
from pathlib import Path

import click

from cim_to_linkml.generator import generate_schema
from cim_to_linkml.parser import parse_uml_project
from cim_to_linkml.reader import read_uml_project
from cim_to_linkml.writer import init_yaml_serializer, write_schema

LOG_FORMAT = "[%(asctime)s] [%(levelname)s] %(message)s"  # noqa
TOP_LEVEL_PACKAGE_NAME = "TC57CIM"

logger = logging.getLogger(__name__)
logging.basicConfig(format=LOG_FORMAT)

init_yaml_serializer()


def _generate_linkml_schema(cim_db, output_dir):
    """Generates LinkML schemas from the supplied Sparx EA QEA database file.
    """

    with sqlite3.connect(cim_db) as conn:
        uml_project = parse_uml_project(*read_uml_project(conn))

    try:
        uml_package = uml_project.packages.by_qualified_name[TOP_LEVEL_PACKAGE_NAME]
    except KeyError:
        click.echo(f"Ignoring unknown package: `{TOP_LEVEL_PACKAGE_NAME}'.", err=True)
        raise SystemExit(1)

    uml_packages = [p for qname, p in uml_project.packages.by_qualified_name.items() if qname.startswith(TOP_LEVEL_PACKAGE_NAME)]
    os.makedirs(output_dir, exist_ok=True)

    uml_classes = list(
        chain.from_iterable(uml_class for p in uml_packages if (uml_class := uml_project.classes.by_package.get(p.id)))
    )
    schema = generate_schema(uml_package, uml_classes, uml_project)

    schema_path = os.path.join(output_dir, TOP_LEVEL_PACKAGE_NAME) + ".yml"
    write_schema(schema, schema_path)

    return uml_project

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
    """Generates LinkML schemas from the supplied Sparx EA QEA database file.
    """

    return _generate_linkml_schema(cim_db, output_dir)

if __name__ == "__main__":
    # cProfile.run("main()", sort="tottime")  # noqa
    # cli.main()
    cim_db = Path("/home/bart/Programming/Netbeheer-Nederland/cim-to-linkml/data/CIM_Grid18v10_Support14v00_Market04v14.qea")
    cim_db = Path("/home/bart/Programming/Netbeheer-Nederland/cim-to-linkml/data/iec61970cim17v40_iec61968cim13v13b_iec62325cim03v17b_CIM100.1.1.1.qea")
    cim18_dict = _generate_linkml_schema(cim_db, "./schemas")
    print(cim18_dict)
