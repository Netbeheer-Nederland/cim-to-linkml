from cim_to_linkml.cim18.linkml.subset.model import Subset as LinkMLSubset
from cim_to_linkml.cim18.uml.package.model import Package as UMLPackage
from cim_to_linkml.cim18.uml.project.model import Project as UMLProject


def generate_subset(uml_package: UMLPackage, uml_project: UMLProject) -> LinkMLSubset:
    uml_parent_package = uml_project.packages[uml_package.parent]
    linkml_subset = LinkMLSubset(
        description=uml_package.notes,
        annotations={
            "ea_guid": uml_package.ea_guid,
            "parent_ea_guid": uml_parent_package.ea_guid,
            "version": uml_package.version,
        },
        conforms_to=uml_package.standard,
    )
    linkml_subset._name = uml_package.name

    return linkml_subset
