from pathlib import Path
import cProfile
import sqlite3

import click

from cim_to_linkml.generator import LinkMLGenerator
from cim_to_linkml.parser import parse_uml_project
from cim_to_linkml.read import read_uml_project
from cim_to_linkml.writer import init_yaml_serializer, write_schema

init_yaml_serializer()


@click.command()
@click.argument("cim_db", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--package",
    "-p",
    type=str,
    required=True,
    show_default=True,
    multiple=True,
    help="Qualified package name. Example: TC57CIM.IEC61970.Base.Core",
)
@click.option(
    "--output-dir",
    "-o",
    default=Path("schemas"),
    type=click.Path(path_type=Path),
    help="Directory where schemas will be outputted.",
)
def cli(
    cim_db,
    package,
    output_dir,
):
    with sqlite3.connect(cim_db) as conn:
        uml_project = parse_uml_project(*read_uml_project(conn))

    generator = LinkMLGenerator(uml_project)
    for qname in package:
        try:
            package = uml_project.packages.by_qualified_name[qname]
        except KeyError:
            print(f"Ignoring unknown package: `{qname}'.")
            continue

        schema = generator.gen_schema_for_package(package.id)
        write_schema(schema, base_output_dir=output_dir)


if __name__ == "__main__":
    # cProfile.run("main()", sort="tottime")
    cli.main()
