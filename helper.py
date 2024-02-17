async def async_getitem(obj, key):
    """dict type의 obj에서 key를 key로 가지는 value값을 반환합니다.
    asyncio.run()안에서 주로 사용됩니다.

    Args:
        obj (dict)
        key (string)

    Returns:
        _type_: obj[key]
    """
    results = obj
    return results[key]
