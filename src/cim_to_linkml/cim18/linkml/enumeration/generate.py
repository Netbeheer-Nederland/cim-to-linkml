from cim_to_linkml.cim18.linkml.enumeration.model import Enum as LinkMLEnumeration, PermissibleValue
from cim_to_linkml.cim18.linkml.type_.generate import generate_curie
from cim_to_linkml.cim18.uml.class_.model import Class as UMLClass
from cim_to_linkml.cim18.uml.project.model import Project as UMLProject


def generate_enumeration(uml_class: UMLClass, uml_project: UMLProject) -> LinkMLEnumeration:
    uml_package_name = uml_project.packages[uml_class.package].name
    linkml_enum = LinkMLEnumeration(
        enum_uri=generate_curie(f"{uml_class.name}"),
        description=uml_class.note,
        annotations={"ea_guid": uml_class.id},
        in_subset=[
            uml_package_name
        ],  # NOTE: Just the immediate package, not the ancestors. That can be derived by logic.
        permissible_values={
            enum_val.name: PermissibleValue(
                meaning=generate_curie(f"{uml_class.name}.{enum_val.name}"), description=enum_val.notes
            )
            for enum_val in uml_class.attributes.values()
        },
    )
    linkml_enum._name = uml_class.name

    return linkml_enum
