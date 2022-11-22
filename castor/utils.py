from datetime import datetime
import typing


def serialize_item(key: str, value: typing.Any) -> typing.Any:
    if key == "time" and isinstance(value, datetime):
        return int(value.timestamp())
    return value


def serialize_event(event: dict) -> dict:
    return {key: serialize_item(key, value) for key, value in event.items()}
