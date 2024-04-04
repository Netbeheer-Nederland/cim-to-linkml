from functools import lru_cache
from urllib.parse import quote
from typing import Optional

import cim_to_linkml.uml_model as uml_model
import cim_to_linkml.linkml_model as linkml_model


class LinkMLGenerator:
    def __init__(self, uml_project: uml_model.Project) -> None:
        self.uml_project = uml_project

    @staticmethod
    def map_primitive_data_type(val):
        try:
            return {
                "Float": "float",
                "Integer": "integer",
                "DateTime": "date",
                "String": "string",
                "Boolean": "boolean",
                "Decimal": "double",  # Is this right?
                "MonthDay": "date",  # Is this right?
                "Date": "date",
                "Time": "time",
                "Duration": "integer",
            }[val]
        except KeyError:
            raise TypeError(f"Data type `{val}` is not a CIM Primitive.")

    @staticmethod
    def gen_safe_name(name: str) -> str:  # TODO: Implement and move.
        # Cleanup colons and weird characters.
        return name

    @staticmethod
    def convert_camel_to_snake(name: str) -> str:  # TODO: Implement and move.
        return name

    @staticmethod
    def gen_curie(name: str, prefix: str) -> str:  # TODO: Implement and move.
        # Also escape characters.
        return f"{prefix}:{quote(name)}"

    def _gen_class_with_deps(self, uml_class: uml_model.Class) -> None:
        match uml_class.stereotype:
            case uml_model.ClassStereotype.PRIMITIVE:
                return
            case uml_model.ClassStereotype.ENUMERATION:
                enum = self.gen_enum(uml_class)
                self.enums[uml_class.id] = enum
            case uml_model.ClassStereotype.CIMDATATYPE | None | _:
                class_ = self.gen_class(uml_class)
                self.classes[uml_class.id] = class_

        uml_dep_classes = set()

        uml_super_class = self.get_super_class(uml_class)
        if uml_super_class:
            uml_dep_classes.add(uml_super_class)

        uml_dep_classes |= self.get_attr_type_classes(uml_class) | self.get_rel_type_classes(
            uml_class
        )

        for uml_dep_class in uml_dep_classes:
            if uml_dep_class.id in self.classes:
                continue
            self._gen_class_with_deps(uml_dep_class)

    def gen_schema(self, uml_package_id: uml_model.ObjectID) -> linkml_model.Schema:
        uml_package = self.uml_project.packages.by_id[uml_package_id]

        # Set or reset state.
        self.classes: dict[uml_model.ObjectID, linkml_model.Class] = {}
        self.enums: dict[uml_model.ObjectID, linkml_model.Enum] = {}

        # for uml_class in self.uml_project.classes.by_id.values():
        for uml_class in self.uml_project.classes.by_pkg_id.get(uml_package_id, []):
            self._gen_class_with_deps(uml_class)

        schema = linkml_model.Schema(
            id=self.gen_curie(uml_package.name, "cim"),
            name=self.gen_safe_name(self.convert_camel_to_snake(uml_package.name)),
            title=uml_package.name,
            enums={enum.name: enum for enum in self.enums.values()},
            description=uml_package.notes,
            classes={class_.name: class_ for class_ in self.classes.values()},
            imports=["linkml:types"],
            prefixes={
                "linkml": "https://w3id.org/linkml/",
                linkml_model.CIM_PREFIX: linkml_model.CIM_BASE_URI,
            },
            default_curi_maps=["semweb_context"],
            default_prefix=linkml_model.CIM_PREFIX,
            default_range="string",
        )

        return schema

    @lru_cache(maxsize=2048)
    def gen_enum(self, uml_enum: uml_model.Class) -> linkml_model.Enum:
        assert uml_enum.stereotype == uml_model.ClassStereotype.ENUMERATION
        enum_name = self.gen_safe_name(uml_enum.name)

        return linkml_model.Enum(
            name=self.gen_safe_name(enum_name),
            enum_uri=self.gen_curie(uml_enum.name, linkml_model.CIM_PREFIX),
            description=uml_enum.note,
            permissible_values=frozenset(
                {
                    (
                        uml_enum_val.name,
                        linkml_model.PermissibleValue(
                            text=enum_val,
                            meaning=self.gen_curie(
                                f"{enum_name}.{enum_val}", linkml_model.CIM_PREFIX
                            ),
                        ),
                    )
                    for uml_enum_val in uml_enum.attributes
                    if (
                        enum_val := self.convert_camel_to_snake(
                            self.gen_safe_name(uml_enum_val.name)
                        )
                    )
                }
            ),
        )

    @lru_cache(maxsize=2048)
    def get_super_class(self, uml_class: uml_model.Class) -> Optional[uml_model.Class]:
        rels = self.uml_project.relations.by_source_id.get(uml_class.id, [])
        for uml_relation in rels:
            try:
                source_class = self.uml_project.classes.by_id[uml_relation.source_class]
            except KeyError as e:
                continue  # Bad data, but no superclass for sure.
            if (
                uml_relation.type == uml_model.RelationType.GENERALIZATION
                and source_class.id == uml_class.id
            ):
                super_class = self.uml_project.classes.by_id[uml_relation.dest_class]
                return super_class
        return None

    @lru_cache(maxsize=2048)
    def get_attr_type_classes(self, uml_class: uml_model.Class) -> frozenset[uml_model.Class]:
        type_classes = {
            class_
            for attr in uml_class.attributes
            if attr.type is not None
            if (class_ := self.uml_project.classes.by_name[attr.type])
        }

        return frozenset(type_classes)

    @lru_cache(maxsize=2048)
    def get_rel_type_classes(self, uml_class: uml_model.Class) -> frozenset[uml_model.Class]:
        from_classes = set()
        to_classes = set()

        for rel in self.uml_project.relations.by_id.values():
            if rel.type == uml_model.RelationType.GENERALIZATION:
                continue
            match uml_class.id:
                case rel.source_class:
                    dest_class = self.uml_project.classes.by_id[rel.dest_class]
                    to_classes.add(dest_class)
                case rel.dest_class:
                    source_class = self.uml_project.classes.by_id[rel.source_class]
                    from_classes.add(source_class)

        return frozenset(from_classes | to_classes)

    def gen_slot_from_attr(
        self, uml_attr: uml_model.Attribute, uml_class: uml_model.Class
    ) -> linkml_model.Slot:
        # range_ = None
        # if uml_attr.type is not None:
        type_class = self.uml_project.classes.by_name[uml_attr.type]
        if type_class.stereotype == uml_model.ClassStereotype.PRIMITIVE:
            range_ = self.map_primitive_data_type(uml_attr.type)
        else:
            range_ = self.convert_camel_to_snake(self.gen_safe_name(type_class.name))

        return linkml_model.Slot(
            name=self.convert_camel_to_snake(self.gen_safe_name(uml_attr.name)),
            range=range_,
            description=uml_attr.notes,
            required=self._slot_required(uml_attr.lower_bound),
            multivalued=self._slot_multivalued(uml_attr.lower_bound),
            slot_uri=self.gen_curie(f"{uml_class.name}.{uml_attr.name}", linkml_model.CIM_PREFIX),
        )

    @staticmethod
    def _slot_required(lower_bound: uml_model.CardinalityValue) -> bool:
        return lower_bound == "*" or lower_bound > 0

    @staticmethod
    def _slot_multivalued(upper_bound: uml_model.CardinalityValue) -> bool:
        return upper_bound == "*" or upper_bound > 1

    def gen_slot_from_relation(
        self, uml_relation: uml_model.Relation, direction
    ) -> linkml_model.Slot:
        source_class = self.uml_project.classes.by_id[uml_relation.source_class]
        dest_class = self.uml_project.classes.by_id[uml_relation.dest_class]

        match direction:
            case "source->dest":
                return linkml_model.Slot(
                    name=self.convert_camel_to_snake(
                        self.gen_safe_name(uml_relation.dest_role or dest_class.name)
                    ),
                    range=self.gen_safe_name(dest_class.name),
                    description=uml_relation.dest_role_note,
                    required=self._slot_required(uml_relation.dest_card.lower_bound),
                    multivalued=self._slot_multivalued(uml_relation.dest_card.upper_bound),
                    slot_uri=self.gen_curie(
                        f"{source_class.name}.{uml_relation.dest_role or dest_class.name}",
                        linkml_model.CIM_PREFIX,
                    ),
                )
            case "dest->source":
                return linkml_model.Slot(
                    name=self.convert_camel_to_snake(
                        self.gen_safe_name(uml_relation.source_role or source_class.name)
                    ),
                    range=self.gen_safe_name(source_class.name),
                    description=uml_relation.source_role_note,
                    required=self._slot_required(uml_relation.source_card.lower_bound),
                    multivalued=self._slot_multivalued(uml_relation.source_card.upper_bound),
                    slot_uri=self.gen_curie(
                        f"{dest_class.name}.{uml_relation.source_role or source_class.name}",
                        linkml_model.CIM_PREFIX,
                    ),
                )
            case _:
                raise TypeError(
                    f"Provided direction value was invalid. (relation ID: {uml_relation.id})"
                )

    @lru_cache(maxsize=2048)
    def gen_class(self, uml_class: uml_model.Class) -> linkml_model.Class:
        super_class = self.get_super_class(uml_class)

        attr_slots = {
            (slot.name, slot)
            for uml_attr in uml_class.attributes
            if (slot := self.gen_slot_from_attr(uml_attr, uml_class))
        }

        from_relation_slots = {
            (slot.name, slot)
            for rel in self.uml_project.relations.by_source_id.get(uml_class.id, [])
            if rel and rel.type != uml_model.RelationType.GENERALIZATION
            if (slot := self.gen_slot_from_relation(rel, "source->dest"))
        }

        to_relation_slots = {
            (slot.name, slot)
            for rel in self.uml_project.relations.by_dest_id.get(uml_class.id, [])
            if rel and rel.type != uml_model.RelationType.GENERALIZATION
            if (slot := self.gen_slot_from_relation(rel, "dest->source"))
        }

        class_ = linkml_model.Class(
            name=self.gen_safe_name(uml_class.name),
            class_uri=self.gen_curie(uml_class.name, linkml_model.CIM_PREFIX),
            is_a=super_class.name if super_class else None,
            description=uml_class.note,
            attributes=frozenset(attr_slots | from_relation_slots | to_relation_slots),
        )

        return class_
