import contextlib


@contextlib.contextmanager
def temporary_set_attr(obj, name, value):
    backup_value = None
    if hasattr(obj, name):
        backup_value = getattr(obj, name)
    try:
        setattr(obj, name, value)
        yield obj
    finally:
        if backup_value is not None:
            setattr(obj, name, backup_value)
