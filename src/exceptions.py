from fastapi import HTTPException


def nc_one_exception(status: int, msg: str, *args) -> HTTPException:
    STATUS_CODES = {
        "404": "NOT FOUND",
        "403": "FORBIDDEN",
        "409": "CONFLICT",
        "401": "UNAUTHORIZED",
        "400": "BAD REQUEST",
    }
    return HTTPException(
        status_code=status,
        detail={"status_code": f"{status} {STATUS_CODES[str(status)]}", "msg": msg},
    )


def not_found(item: str, id=None, msg=""):
    if msg == "":
        msg = f"{item} id: {id} does not exist"
    return nc_one_exception(404, msg)


def event_not_found(id=int):
    return nc_one_exception(404, f"event id: {id} does not exist")


def forbidden(msg: str = "Insufficient rights"):
    return nc_one_exception(403, msg)


def conflict(msg: str):
    return nc_one_exception(409, msg)


def bad_request(msg: str):
    return nc_one_exception(400, msg)
