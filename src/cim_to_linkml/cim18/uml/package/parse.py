import sqlite3

from cim_to_linkml.cim18.uml.package.model import INFORMAL_PACKAGES, DOCUMENTATION_PACKAGES, Package
from cim_to_linkml.cim18.uml.utils import parse_iso_datetime_val


def is_informal_package(package: sqlite3.Row, packages: list[sqlite3.Row]) -> bool:
    if int(package["id"]) in INFORMAL_PACKAGES:
        return True

    try:
        parent_package = [p for p in packages if int(p["id"]) == int(package["parent_id"])][0]
    except IndexError:
        return False

    return False or is_informal_package(parent_package, packages)


def is_documentation_package(package: sqlite3.Row, packages: list[sqlite3.Row]) -> bool:
    if int(package["id"]) in DOCUMENTATION_PACKAGES:
        return True

    try:
        parent_package = [p for p in packages if int(p["id"]) == int(package["parent_id"])][0]
    except IndexError:
        return False

    return False or is_documentation_package(parent_package, packages)


def parse_uml_package(package: sqlite3.Row, packages: list[sqlite3.Row]) -> Package:
    return Package(
        id=int(package["id"]),
        name=package["name"],
        notes=package["note"],
        author=package["author"],
        created_date=parse_iso_datetime_val(package["created_date"]),
        modified_date=parse_iso_datetime_val(package["modified_date"]),
        parent=package["parent_id"],
        is_informal=is_informal_package(package, packages),
        is_documentation=is_documentation_package(package, packages),
    )
