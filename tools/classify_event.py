def classify_event(activity_raw: str, remark: str) -> str:
    a = (activity_raw or "").lower()
    r = (remark or "").lower()

    if "wire" in a or "log" in r:
        return "WIRELINE"

    if "trip" in a or "rih" in r or "pooh" in r:
        return "TRIP"

    if "dst" in r:
        return "DST"

    if "mud" in r or "circulation" in r:
        return "MUD_CONDITIONING"

    if "rig up" in r or "rig down" in r:
        return "RIG_UP_DOWN"

    if "wait" in a or "waiting" in r:
        return "WAITING"

    if "fail" in r:
        return "EQUIPMENT_FAILURE"

    return "OTHER"
