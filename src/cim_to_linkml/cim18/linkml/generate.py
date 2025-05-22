from urllib.parse import quote

from cim_to_linkml.cim18.linkml.model import CIM_PREFIX


def generate_curie(name: str, prefix: str = CIM_PREFIX) -> str:
    return f"{prefix}:{quote(name)}"