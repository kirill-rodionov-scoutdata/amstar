import orjson


def orjson_dumper(obj) -> str:
    return orjson.dumps(obj).decode()
