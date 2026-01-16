from fastapi import HTTPException

def error_message(e) -> HTTPException:
    if isinstance(e, HTTPException):
        raise e
    else:
        raise HTTPException(500, str(e))