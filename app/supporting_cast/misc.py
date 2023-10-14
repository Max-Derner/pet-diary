from datetime import datetime, timezone


def utc_timestamp_now() -> float:
    return datetime.now(tz=timezone.utc).timestamp()
