from functools import lru_cache
from operator import attrgetter


@lru_cache()
def by_qualified_name(self):
    return {self.get_qualified_name(p_id): p for p_id, p in self.by_id.items()}

@lru_cache(maxsize=173)
def get_qualified_name(self, package_id):
    return ".".join(self._get_package_path(package_id))

def _get_package_path(self, start_pkg_id, package_path=None):
    if package_path is None:
        package_path = []

    package = self.by_id[start_pkg_id]

    if package.parent in (0, None):
        return package_path

    return self._get_package_path(package.parent, [package.name] + package_path)


