from datetime import datetime, timezone

#intentional flak8 issue
def utc_timestamp_now() -> float:
    return datetime.now(tz=timezone.utc).timestamp()
