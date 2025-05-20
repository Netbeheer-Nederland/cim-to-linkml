from functools import cached_property
from itertools import groupby
from operator import attrgetter


class RelationsQuery:
    def __init__(self, relations):
        self._data = relations

    @cached_property
    def by_id(self):
        return {r.id: r for r in sorted(self._data, key=attrgetter("id"))}

    @cached_property
    def by_source_class(self):
        key = attrgetter("source_class")

        relations_by_source_class = {}
        for source_class, relations in groupby(sorted(self._data, key=key), key=key):
            relations = list(sorted(relations, key=attrgetter("id")))
            relations_by_source_class[source_class] = relations

        return relations_by_source_class

    @cached_property
    def by_dest_class(self):
        key = attrgetter("dest_class")

        relations_by_dest_class = {}
        for dest_class, relations in groupby(sorted(self._data, key=key), key=key):
            relations = list(sorted(relations, key=attrgetter("id")))
            relations_by_dest_class[dest_class] = relations

        return relations_by_dest_class
