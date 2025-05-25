from cim_to_linkml.cim18.linkml.subset.model import Subset as LinkMLSubset
from cim_to_linkml.cim18.uml.package.model import Package as UMLPackage
from cim_to_linkml.cim18.uml.project.model import Project as UMLProject


def generate_subset(uml_package: UMLPackage) -> LinkMLSubset:
    linkml_subset = LinkMLSubset(description=uml_package.notes)
    linkml_subset._name = uml_package.name

    return linkml_subset
