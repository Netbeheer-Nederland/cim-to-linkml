from dataclasses import dataclass
from datetime import datetime

from cim_to_linkml.cim18.uml.model import ObjectID

INFORMAL_PACKAGES = [29, 30, 31, 32, 50, 54, 59, 60, 62, 64, 66, 71, 75,
                     76, 88, 92, 94, 99, 100, 132, 133, 134, 135, 136,
                     137, 138, 139, 140, 142, 143, 144, 160, 188, 195, 224]

DOCUMENTATION_PACKAGES = [5, 27, 49, 70, 104, 189]

@dataclass
class Package:
    id: ObjectID
    name: str
    notes: str | None = None
    author: str | None = None
    created_date: datetime = datetime.now()
    modified_date: datetime = datetime.now()
    parent: ObjectID | None = None
    is_informal: bool = False
    is_documentation: bool = False
