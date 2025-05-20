from dataclasses import dataclass

from cim_to_linkml.cim18.uml.class_.model import Class
from cim_to_linkml.cim18.uml.model import ObjectID
from cim_to_linkml.cim18.uml.package.model import Package
from cim_to_linkml.cim18.uml.relation.model import Relation


@dataclass
class Project:
    packages: dict[ObjectID, Package]
    classes: dict[ObjectID, Class]
    relations: dict[ObjectID, Relation]
