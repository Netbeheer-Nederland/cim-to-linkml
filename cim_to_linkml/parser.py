import cim_to_linkml.uml_model as uml_model


def parse_uml_package(
    package_id: uml_model.ObjectID, packages: dict[uml_model.ObjectID, dict]
) -> uml_model.Package:
    package = packages[package_id]

    # Model has parent ID 0 which does not exist, so we are skipping it as a special case.
    parent = None
    if package["parent_id"] not in [0, None]:
        parent = parse_uml_package(package["parent_id"], packages)

    return uml_model.Package(
        id=package_id,
        name=package["name"],
        author=package["author"],
        parent=parent,
        created_date=package["created_date"],
        modified_date=package["modified_date"],
        notes=package["note"],
    )
