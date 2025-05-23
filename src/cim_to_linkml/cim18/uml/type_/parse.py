from datetime import datetime


def parse_iso_datetime_val(val: str | None) -> datetime:
    if val is None:
        return datetime.now()

    return datetime.fromisoformat(val)