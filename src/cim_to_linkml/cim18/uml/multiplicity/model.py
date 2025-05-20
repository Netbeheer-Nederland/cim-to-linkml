from dataclasses import dataclass
from typing import Literal

type MultiplicityBound = int | Literal["*"]


@dataclass
class Multiplicity:
    lower_bound: MultiplicityBound = 0
    upper_bound: MultiplicityBound = 1
