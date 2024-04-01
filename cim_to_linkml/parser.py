from pprint import pprint
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


def parse_uml_class(
    class_id: uml_model.ObjectID,
    classes: dict[uml_model.ObjectID, dict],
):
    class_ = classes[class_id]
    print(class_)
    return uml_model.Class(
        id=class_id,
        name=class_["class_name"],
        author=class_["class_author"],
        package=class_["class_package_id"],
        attributes={},
        created_date=class_["class_created_date"],
        modified_date=class_["class_modified_date"],
        note=class_["class_note"],
        stereotype=class_["class_stereotype"],
    )
