# import cProfile
import logging
import sqlite3
from pathlib import Path

import click

from cim_to_linkml.cim18.parser import parse_uml_project
from cim_to_linkml.cim18.reader import read_uml_packages, read_uml_classes, read_uml_relations
from cim_to_linkml.cim18.writer import init_yaml_serializer

LOG_FORMAT = "[%(asctime)s] [%(levelname)s] %(message)s"  # noqa
TOP_LEVEL_PACKAGE_NAME = "CIM"

logger = logging.getLogger(__name__)
logging.basicConfig(format=LOG_FORMAT)

init_yaml_serializer()


def _generate_linkml_schema(cim_db, output_dir):
    """Generates LinkML schemas from the supplied Sparx EA QEA database file."""

    with sqlite3.connect(cim_db) as conn:
        # print(list(read_uml_packages(conn)))
        uml_project = parse_uml_project(read_uml_packages(conn), read_uml_classes(conn), read_uml_relations(conn))
    print(uml_project)

    # try:
    #     uml_package = uml_project.packages.by_qualified_name[TOP_LEVEL_PACKAGE_NAME]
    # except KeyError:
    #     click.echo(f"Ignoring unknown package: `{TOP_LEVEL_PACKAGE_NAME}'.", err=True)
    #     raise SystemExit(1)
    #
    # uml_packages = [
    #     p for qname, p in uml_project.packages.by_qualified_name.items() if qname.startswith(TOP_LEVEL_PACKAGE_NAME)
    # ]
    # os.makedirs(output_dir, exist_ok=True)
    #
    # uml_classes = list(
    #     chain.from_iterable(uml_class for p in uml_packages if (uml_class := uml_project.classes.by_package.get(p.id)))
    # )
    # schema = generate_schema(uml_package, uml_classes, uml_project)
    #
    # schema_path = os.path.join(output_dir, TOP_LEVEL_PACKAGE_NAME) + ".yml"
    # write_schema(schema, schema_path)
    #
    # return uml_project


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
