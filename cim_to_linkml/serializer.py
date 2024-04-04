def represent_none(self, _):
    return self.represent_scalar("tag:yaml.org,2002:null", "")


def frozenset_representer(dumper, data):
    assert type(data) == frozenset
    if len(data) == 0:
        return dumper.represent_none(data)

    for el in data:  # Only check first element.
        if type(el) == tuple and len(el) == 2:
            return dumper.represent_dict(dict(data))
        else:
            return dumper.represent_set(data)


def linkml_namedtuple_representer(dumper, data):
    return dumper.represent_dict(data._asdict())


# def linkml_schema_representer(dumper, data):
#     return dumper.represent_dict(
#         OrderedDict(
#             {
#                 "id": data.id,
#                 "name": data.name,
#                 "title": data.title,
#                 "description": data.description,
#                 "imports": data.imports,
#                 "prefixes": data.prefixes,
#                 "default_curi_maps": data.default_curi_maps,
#                 "default_prefix": data.default_prefix,
#                 "default_range": data.default_range,
#                 "classes": data.classes,
#                 "enums": data.enums,
#             }
#         )
#     )
