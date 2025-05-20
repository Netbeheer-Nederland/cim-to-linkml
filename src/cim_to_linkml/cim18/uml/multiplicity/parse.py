from cim_to_linkml.cim18.uml.multiplicity.model import Multiplicity, MultiplicityBound


def parse_multiplicity(val: str | None) -> Multiplicity:
    if val is None:
        return Multiplicity()

    lb, _, ub = val.partition("..")

    return Multiplicity(
        lower_bound=parse_multiplicity_val(lb),
        upper_bound=parse_multiplicity_val(ub),
    )


def parse_multiplicity_val(val: str | None) -> MultiplicityBound:
    match val:
        case "" | None:
            return 0
        case "n" | "*":
            return "*"
        case _:
            return int(val)

