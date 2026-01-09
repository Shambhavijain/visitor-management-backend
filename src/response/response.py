from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


class Response:

    @classmethod
    def success_response(cls, data, message, status_code):
        return JSONResponse(
            status_code=status_code,
            content={
                "status": "success",
                "message": message,
                "data": jsonable_encoder(data, by_alias=True),
            },
        )

    @classmethod
    def error_response(cls, message, status_code):
        return JSONResponse(
            status_code=status_code,
            content={
                "status": "error",
                "message": message,
            },
        )
