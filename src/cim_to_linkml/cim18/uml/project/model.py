from collections import UserDict
from dataclasses import dataclass

from cim_to_linkml.cim18.uml.class_.model import Class
from cim_to_linkml.cim18.uml.model import ObjectID
from cim_to_linkml.cim18.uml.package.model import Package
from cim_to_linkml.cim18.uml.relation.model import Relation, ConnectorID


class Packages(UserDict[ObjectID, Package]):
    def by_name(self, name: str) -> Package | None:
        for package_id, package in self.items():
            if package.name == name:
                return package

        return None


class Classes(UserDict[ObjectID, Class]):
    def by_name(self, name: str) -> Class | None:
        for class_id, class_ in self.items():
            if class_.name == name:
                return class_

        return None


class Relations(UserDict[ConnectorID, Relation]):
    def by_source_class(self, class_id_: ObjectID) -> Relation | None:
        # for relation in self.values():
        #     if relation.source_class == class_id_:
        #         return relation
        # return None
        ...

    def by_dest_class(self, class_id_: ObjectID) -> Relation | None:
        # for relation in self.values():
        #     if relation.dest_class == class_id_:
        #         return relation
        # return None
        ...



@dataclass
class Project:
    packages: Packages
    classes: Classes
    relations: Relations
