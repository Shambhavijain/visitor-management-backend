import boto3
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from httpx import Request
from src.errors.error import (
    NotFoundError,
    AppError,
    RepositoryError,
    ServiceError,
    AuthenticationError,
    AuthorizationError,
    UserNotFoundError,
)

import src.errors.error_handlers as err_handlers

from src.repository.user_repository import DDBUserRepository
from src.repository.visitor_repository import DDBVisitorRepository
from src.routes.auth_route import auth_router
from src.routes import users_route, gatekeeper_route, visitors_route


load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    region = os.getenv("AWS_REGION", "us-east-1")
    table_name = os.getenv("DDB_TABLE_NAME", "VMP_nosql")

    ddb = boto3.resource("dynamodb", region_name=region)
    table_name = table_name
    app.state.user_repo = DDBUserRepository(ddb_resource=ddb, table_name=table_name)

    app.state.visitor_repo = DDBVisitorRepository(
        ddb_resource=ddb, table_name=table_name
    )
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("CORS_ORIGIN", "http://localhost:4200")],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
    expose_headers=["*"],
)


def generic_exc_handler(request: Request, exc: Exception):
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)
    )


app.add_exception_handler(HTTPException, err_handlers.handle_http_exception)
app.add_exception_handler(NotFoundError, err_handlers.handle_notfound_error)
app.add_exception_handler(ServiceError, err_handlers.handle_service_error)
app.add_exception_handler(AppError, err_handlers.handle_app_error)
app.add_exception_handler(RepositoryError, err_handlers.handle_repository_error)
app.add_exception_handler(AuthenticationError, err_handlers.handle_authentication_error)
app.add_exception_handler(AuthorizationError, err_handlers.handle_authorization_error)
app.add_exception_handler(UserNotFoundError, err_handlers.handle_usernotfound_error)
app.add_exception_handler(Exception, err_handlers.generic_exc_handler)


app.include_router(auth_router)
app.include_router(users_route.user_router)
app.include_router(gatekeeper_route.gatekeeper_router)
app.include_router(visitors_route.visitor_router)
