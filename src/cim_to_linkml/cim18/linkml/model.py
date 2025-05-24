from pydantic import BaseModel, PrivateAttr, Field
from typing import Any

type IRI = str
type CURIE = str

type SlotName = str
type ClassName = str
type EnumName = str
type TypeName = str
type SubsetName = str


CIM_PREFIX = "cim"
CIM_BASE_URI = "https://cim.ucaiug.io/ns#"
CIM_MODEL_LICENSE = "https://www.apache.org/licenses/LICENSE-2.0.txt"


class Element(BaseModel):
    _name: str = PrivateAttr()
    description: str | None = Field(None)
    annotations: dict[str, Any] | None = Field(None)
    subsets: list[SubsetName] | None = Field(None)