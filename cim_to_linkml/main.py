import cProfile
import logging
import os
import sqlite3
from itertools import chain
from pathlib import Path

import click

from cim_to_linkml.generator import generate_schema
from cim_to_linkml.parser import parse_uml_project
from cim_to_linkml.read import read_uml_project
from cim_to_linkml.writer import init_yaml_serializer, write_schema

LOG_FORMAT = "[%(asctime)s] [%(levelname)s] %(message)s"

logger = logging.getLogger(__name__)
logging.basicConfig(format=LOG_FORMAT)


init_yaml_serializer()


@click.command()
@click.argument("cim_db", type=click.Path(exists=True, path_type=Path), nargs=1, metavar="QEA_FILE")
@click.option(
    "--package",
    "-p",
    type=str,
    show_default=True,
    default="TC57CIM",
    help="Fully qualified package name.",
)
@click.option(
    "--single-schema",
    is_flag=True,
    default=False,
    show_default=True,
    help="If true, a single schema is created, a schema per package otherwise.",
)
@click.option(
    "--ignore-subpackages",
    is_flag=True,
    default=False,
    show_default=True,
    help="If passed, all subpackages of the provided package are ignored, i.e. only the package itself is selected.",
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
    single_schema,
    ignore_subpackages,
    output_dir,
):
    """
    Generates LinkML schemas from the supplied Sparx EA QEA database file.


    You can specify which packages in the UML model to generate schemas from
    using the `--package` parameter, where you provide the fully qualified
    package name (e.g. `TC57CIM.IEC61970.Base.Core') of the package to select it.

    If the specified package is a leaf package, a single schema file will be
    generated.

    If the provided package is a non-leaf package, by default its subpackages are
    included and a schema file per package is created. A single schema file can also
    be created by passing `--single-schema'.
    Finally, it's possible to ignore all subpackages and create a single schema file
    just for the specified package alone. To achieve this, pass `--ignore-subpackages'.

    """

    with sqlite3.connect(cim_db) as conn:
        uml_project = parse_uml_project(*read_uml_project(conn))

    try:
        uml_package = uml_project.packages.by_qualified_name[package]
    except KeyError:
        click.echo(f"Ignoring unknown package: `{package}'.", err=True)
        raise SystemExit(1)

    if uml_project.packages.is_leaf_package(package):
        single_schema = True
        ignore_subpackages = True

    if ignore_subpackages:
        uml_packages = [uml_package]
        single_schema = True
    else:
        uml_packages = [p for qname, p in uml_project.packages.by_qualified_name.items() if qname.startswith(package)]

    os.makedirs(output_dir, exist_ok=True)

    if single_schema:
        uml_classes = list(
            chain.from_iterable(
                uml_class for p in uml_packages if (uml_class := uml_project.classes.by_package.get(p.id))
            )
        )
        schema = generate_schema(uml_package, uml_classes, uml_project)

        schema_path = os.path.join(output_dir, package) + ".yml"
        write_schema(schema, schema_path)
    else:
        for uml_package in uml_packages:
            uml_classes = uml_project.classes.by_package.get(uml_package.id, [])
            schema = generate_schema(uml_package, uml_classes, uml_project)

            qname = uml_project.packages.get_qualified_name(uml_package.id)
            package_path = qname.split(".")
            dir_path = os.path.join(output_dir, os.path.sep.join(package_path[:-1]))
            file_name = package_path[-1] + ".yml"
            out_file = os.path.join(dir_path, file_name)

            os.makedirs(dir_path, exist_ok=True)
            write_schema(schema, out_file)


if __name__ == "__main__":
    # cProfile.run("main()", sort="tottime")
    cli.main()
