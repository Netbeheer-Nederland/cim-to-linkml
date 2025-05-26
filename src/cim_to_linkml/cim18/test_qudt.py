from dataclasses import dataclass
from enum import Enum
from typing import Any, Annotated, get_args, get_origin, get_type_hints

from pydantic import BaseModel


@dataclass(frozen=True)
class Unit:
    ucum_code: str

class QuantityKind(str, Enum):
    CURRENT_FLOW = "CurrentFlow"

class UCUMUnit(str, Enum):
    MILLIAMPERE = "mA"

class StaticVarCompensator(BaseModel):
    inductive_rating : Annotated[float, QuantityKind.CURRENT_FLOW, Unit("kA")]
    capacitive_rating: Annotated[float, QuantityKind.CURRENT_FLOW, Unit("mA")]


# --- Helper function to get metadata from Annotated type ---
def get_field_metadata(model_instance: Any, field_name: str):
    type_hints = get_type_hints(type(model_instance), include_extras=True)
    annotated_type = type_hints.get(field_name)
    if annotated_type and get_origin(annotated_type) is Annotated:
        _, *annotations = get_args(annotated_type)
        return annotations
    return []


def get_quantity_kind(model_instance: Any, field_name: str):
    annotations = get_field_metadata(model_instance, field_name)
    return next((a for a in annotations if isinstance(a, QuantityKind)), None)


def get_unit(model_instance: Any, field_name: str):
    annotations = get_field_metadata(model_instance, field_name)
    return next((a for a in annotations if isinstance(a, UCUMUnit)), None)


if __name__ == "__main__":
    my_static_var_compensator = StaticVarCompensator(inductive_rating=100.0, capacitive_rating=250.0)

    # Get metadata
    kind = get_quantity_kind(my_static_var_compensator, "inductive_rating")
    unit = get_unit(my_static_var_compensator, "capacitive_rating")

    print("Inductive Rating:", my_static_var_compensator.inductive_rating)
    print("Quantity Kind:", kind)
    print("Unit:", unit)
