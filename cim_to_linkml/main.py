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
@click.argument("cim_db", type=click.Path(exists=True, path_type=Path), nargs=1, metavar="QEA_FILE")
@click.option(
    "--package",
    "-p",
    type=str,
    show_default=True,
    multiple=True,
    help="Fully qualified package name. [example: TC57CIM.IEC61970.Base.Core]",
)
@click.option(
    "--single-schema",
    "-s",
    is_flag=True,
    default=False,
    show_default=True,
    help="If false, a schema is generated per package. Otherwise everything will be outputted to a single schema.",
)
@click.option(
    "--output-dir",
    "-o",
    default=Path("schemas"),
    show_default=True,
    type=click.Path(path_type=Path),
    help="Directory where schemas will be outputted.",
)
def cli(
    cim_db,
    package,
    output_dir,
):
    """
    Generates LinkML schemas from the supplied Sparx EA QEA database file.


    You can specify which packages in the UML model to generate schemas from
    using the `--package` parameter, where you provide the fully qualified
    package name (e.g. TC57CIM.IEC61970.Base.Core) of each package to select it.

    If no packages are specified, the entire CIM will be selected.

    By default, a LinkML schema will be generated for each specified package.
    However, by setting the `--single-schema` flag everything is outputted to
    a single LinkML schema.



    """

    with sqlite3.connect(cim_db) as conn:
        uml_project = parse_uml_project(*read_uml_project(conn))

    generator = LinkMLGenerator(uml_project)
    if package:
        for qname in package:
            try:
                package = uml_project.packages.by_qualified_name[qname]
            except KeyError:
                print(f"Ignoring unknown package: `{qname}'.")
                continue

            schema = generator.gen_schema_for_package(package.id)
            write_schema(schema, base_output_dir=output_dir)
    else:
        for pkg_id in generator.uml_project.packages.by_id:
            # schema = generator.gen_schema_for_cim()
            schema = generator.gen_schema_for_package(pkg_id)
            write_schema(schema, base_output_dir=output_dir)


if __name__ == "__main__":
    # cProfile.run("main()", sort="tottime")
    cli.main()
