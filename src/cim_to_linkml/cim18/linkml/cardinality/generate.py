from cim_to_linkml.cim18.uml.multiplicity.model import MultiplicityBound


def is_slot_required(lower_bound: MultiplicityBound) -> bool:
    return lower_bound == "*" or lower_bound > 0


def is_slot_multivalued(upper_bound: MultiplicityBound) -> bool:
    return upper_bound == "*" or upper_bound > 1
