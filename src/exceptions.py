from fastapi import HTTPException

def nc_one_exception(status: int, msg: str, field: list | None) -> HTTPException:
    STATUS_CODES = {"404": "NOT FOUND", "403": "FORBIDDEN", "409": "CONFLICT", "401": "UNAUTHORIZED"}
    return HTTPException(
        status_code= int,
        detail= {"status_code": f"{status} {STATUS_CODES[status]}", "msg": msg }
    )



def not_found(item: str, id):
    return nc_one_exception(404, f"{item} id: {id} does not exist")

def forbidden(msg: str = "Insufficient rights"):
    return nc_one_exception(403, msg)

def conflict(msg: str):
    return nc_one_exception(409,msg)