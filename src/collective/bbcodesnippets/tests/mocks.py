def mock_get_registry_record(*args, **kw):
    def _func(*args, **kw):
        return ["dummy"]

    return _func
