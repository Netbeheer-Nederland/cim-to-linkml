# import cProfile
import logging
import sqlite3
from pathlib import Path

import click

from cim_to_linkml.parser import parse_uml_project
from cim_to_linkml.reader import read_uml_project, read_uml_classes
from cim_to_linkml.writer import init_yaml_serializer

LOG_FORMAT = "[%(asctime)s] [%(levelname)s] %(message)s"  # noqa

logger = logging.getLogger(__name__)
logging.basicConfig(format=LOG_FORMAT)

init_yaml_serializer()


def _generate_linkml_schema(cim_db, output_dir):
    """Generates LinkML schemas from the supplied Sparx EA QEA database file.
    """

    with sqlite3.connect(cim_db) as conn:
        uml_project = parse_uml_project(*read_uml_project(conn))

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
    cim18_qea = Path("/home/bart/Programming/Netbeheer-Nederland/cim-to-linkml/data/CIM_Grid18v10_Support14v00_Market04v14.qea")
    cim18_dict = _generate_linkml_schema(cim18_qea, "./schemas")
    print(cim18_dict)