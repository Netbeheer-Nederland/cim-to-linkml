from functools import cached_property
from itertools import groupby
from operator import attrgetter


# TODO: Remove class, but beware for performance (cached properties and such).
class ClassQuery:
    def __init__(self, classes):
        self._data = classes

    @cached_property
    def by_id(self):
        return {c.id: c for c in sorted(self._data, key=attrgetter("id"))}

    @cached_property
    def by_name(self):
        key = attrgetter("name")

        classes_by_name = {}
        for name, classes in groupby(sorted(self._data, key=key), key=key):
            classes = list(sorted(classes, key=attrgetter("id")))
            class_ = classes[0]
            if len(classes) > 1:
                print(
                    f"Multiple classes with name {name}. Choosing one (object ID: {class_[0]}) "
                    f"and skipping the others (object IDs: {', '.join(str(c.id) for c in classes[1:])})."
                )
            classes_by_name[name] = class_

        return classes_by_name

    @cached_property
    def by_package(self):
        key = attrgetter("package")

        classes_by_package = {}
        for package_id, classes in groupby(sorted(self._data, key=key), key=key):
            classes = list(sorted(classes, key=attrgetter("id")))
            classes_by_package[package_id] = classes

        return classes_by_package
