def to_float(s: str):
    if s is None:
        return s
    s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return -1


def to_int(s: str):
    if s is None:
        return None
    try:
        return int(s)
    except ValueError:
        return -1
