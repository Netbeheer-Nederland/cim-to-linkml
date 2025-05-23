import sqlite3

from cim_to_linkml.cim18.uml.package.model import INFORMAL_PACKAGES, DOCUMENTATION_PACKAGES, Package, PackageStatus
from cim_to_linkml.cim18.uml.type_.parse import parse_iso_datetime_val


def parse_uml_package_status(package: sqlite3.Row, packages: list[sqlite3.Row]) -> PackageStatus:
    package_id = package["id"]

    if package_id in INFORMAL_PACKAGES:
        return PackageStatus.INFORMAL
    elif package_id in DOCUMENTATION_PACKAGES:
        return PackageStatus.DOCUMENTATION

    try:
        parent_package = [p for p in packages if p["id"] == package["parent_id"]][0]
    except IndexError:
        return PackageStatus.NORMATIVE

    return parse_uml_package_status(parent_package, packages)


def parse_uml_package(package: sqlite3.Row, packages: list[sqlite3.Row]) -> Package:
    return Package(
        id=package["id"],
        name=package["name"],
        status=parse_uml_package_status(package, packages),
        parent=package["parent_id"],
        created_date=parse_iso_datetime_val(package["created_date"]),
        modified_date=parse_iso_datetime_val(package["modified_date"]),
        author=package["author"],
        notes=package["note"],
    )
