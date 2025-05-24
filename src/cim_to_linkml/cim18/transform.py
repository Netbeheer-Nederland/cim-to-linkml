from datetime import datetime

from cim_to_linkml.cim18.linkml.cardinality.generate import is_slot_required, is_slot_multivalued
from cim_to_linkml.cim18.linkml.class_.model import Class as LinkMLClass
from cim_to_linkml.cim18.linkml.model import CIM_MODEL_LICENSE, CIM_PREFIX, CIM_BASE_URI
from cim_to_linkml.cim18.linkml.schema.model import SCHEMA_ID, SCHEMA_NAME, LINKML_METAMODEL_VERSION, \
    GITHUB_BASE_URL
from cim_to_linkml.cim18.linkml.schema.model import Schema as LinkMLSchema
from cim_to_linkml.cim18.linkml.slot.model import Slot as LinkMLSlot
from cim_to_linkml.cim18.linkml.type_.generate import map_primitive_datatype, generate_curie
from cim_to_linkml.cim18.main import TOP_LEVEL_PACKAGE_ID
from cim_to_linkml.cim18.uml.class_.model import Attribute as UMLAttribute, ClassStereotype as UMLClassStereotype
from cim_to_linkml.cim18.uml.class_.model import Class as UMLClass
from cim_to_linkml.cim18.uml.model import ObjectID as UMLObjectID
from cim_to_linkml.cim18.uml.project.model import Project as UMLProject
from cim_to_linkml.generator import GITHUB_REPO_URL


class CIMUMLToLinkML:
    def __init__(self, uml_project: UMLProject, root_package_id: UMLObjectID = TOP_LEVEL_PACKAGE_ID):
        self.uml_project = uml_project
        self.uml_root_package = uml_project.packages[root_package_id]

    def generate_schema(self) -> LinkMLSchema:
        classes, slots, enums, types = {}, {}, {}, {}

        for uml_class in self.uml_project.classes.values():
            match uml_class.stereotype:
                case ClassStereotype.PRIMITIVE:
                    continue
                case ClassStereotype.ENUMERATION:
                    enums[uml_class.name] = self.generate_enumeration(uml_class)
                case ClassStereotype.CIM_DATATYPE:
                    types[uml_class.name] = self.generate_type(uml_class)
                case ClassStereotype.COMPOUND:
                    continue  # TODO: Implement.
                case None | _:
                    classes[uml_class.name] = self.generate_class(uml_class)

        # inline()  # TODO: Implement.

        schema = LinkMLSchema(
            id=SCHEMA_ID,
            name=SCHEMA_NAME,
            title=self.uml_root_package.name,
            description=self.uml_root_package.notes,
            contributors=["github:bartkl"],
            created_by=GITHUB_REPO_URL,
            generation_date=datetime.now(),
            license=CIM_MODEL_LICENSE,
            metamodel_version=LINKML_METAMODEL_VERSION,
            imports=["linkml:types"],
            prefixes={
                "linkml": "https://w3id.org/linkml/",
                "github": GITHUB_BASE_URL,
                CIM_PREFIX: CIM_BASE_URI,
            },
            default_curi_maps=["semweb_context"],
            default_prefix=CIM_PREFIX,
            default_range="string",
            classes=classes,
            slots=slots,
            enums=enums,
            types=types,
        )

        return schema

    def generate_attribute(self, uml_attribute: UMLAttribute, uml_parent_class: UMLClass) -> LinkMLSlot:
        type_class = [c for c in self.uml_project.classes.values() if c.name == uml_attribute.type][0]
        if type_class.stereotype == UMLClassStereotype.PRIMITIVE:
            range_ = map_primitive_datatype(uml_attr.type)
        else:
            range_ = type_class.name

        return LinkMLSlot(
            name=uml_attribute.name,
            range=map_primitive_datatype(type_class.name) if uml_attribute.type .stereotype == ClassStereotype.PRIMITIVE .type else None,
            description=uml_attribute.notes,
            required=is_slot_required(uml_attribute.multiplicity.lower_bound),
            multivalued=is_slot_multivalued(uml_attribute.multiplicity.lower_bound),
            slot_uri=generate_curie(f"{uml_parent_class.name}.{uml_attribute.name}"),
        )

    def generate_class(self, uml_class: UMLClass) -> LinkMLClass:
        return LinkMLClass(
            name=uml_class.name,
            description=uml_class.note,
            annotations={"ea_guid": uml_class.id},
            attributes={attr.name: self.generate_attribute(attr, uml_class) for attr in uml_class.attributes.values()},
        )
