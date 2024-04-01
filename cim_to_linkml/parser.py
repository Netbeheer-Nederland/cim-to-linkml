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


def parse_uml_class_attr(
    attr: dict, classes: dict[uml_model.ObjectID, dict]
) -> uml_model.Attribute:
    try:
        type_class = [c for c in classes.values() if c["class_name"] == attr["attr_type"]][0]
    except IndexError as e:
        type_class = None

    return uml_model.Attribute(
        id=attr["attr_id"],
        name=attr["attr_name"],
        lower_bound=int(attr["attr_lower_bound"] if attr["attr_lower_bound"] is not None else "0"),
        upper_bound=int(attr["attr_upper_bound"] if attr["attr_upper_bound"] is not None else "1"),
        type=type_class,
        default=attr["attr_default"],
        notes=attr["attr_notes"],
        stereotype=attr["attr_stereotype"],
    )


def parse_uml_class(class_: dict, classes: dict[uml_model.ObjectID, dict]) -> uml_model.Class:
    return uml_model.Class(
        id=class_["class_id"],
        name=class_["class_name"],
        author=class_["class_author"],
        package=class_["class_package_id"],
        attributes={
            attr_id: parse_uml_class_attr(attr, classes)
            for attr_id, attr in class_["attributes"].items()
        },
        created_date=class_["class_created_date"],
        modified_date=class_["class_modified_date"],
        note=class_["class_note"],
        stereotype=class_["class_stereotype"],
    )
