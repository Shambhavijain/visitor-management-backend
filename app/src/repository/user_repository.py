from abc import ABC, abstractmethod
from typing import List

import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

from src.models.user import User, UsersCount
from src.errors import error
from src.constants.role_enum import UserRole


class UserRepository(ABC):

    @abstractmethod
    def get_by_email(self, email: str) -> User: ...
    @abstractmethod
    def get_user_by_id(self, user_id: str) -> User: ...
    @abstractmethod
    def create(self, user: User) -> None: ...
    @abstractmethod
    def create_gatekeeper(self, user: User) -> None: ...
    @abstractmethod
    def delete(self, user_id: str) -> None: ...
    @abstractmethod
    def get_all_users(self) -> List[User]: ...
    @abstractmethod
    def get_owner_by_tower_and_flat(self, tower: str, flat_no: str) -> User: ...
    @abstractmethod
    def get_users_count(self) -> UsersCount: ...


class DDBUserRepository(UserRepository):

    def __init__(
        self, ddb_resource: boto3.resources.base.ServiceResource, table_name: str
    ):
        self.table = ddb_resource.Table(table_name)

    def get_by_email(self, email: str) -> User:
        email = email.lower()

        resp = self.table.get_item(
            Key={
                "PK": "USERS",
                "SK": f"EMAIL#{email}",
            }
        )

        item = resp.get("Item")
        if not item:
            raise error.NotFoundError("invalid email or password")

        return self.get_user_by_id(item["UserId"])

    def get_user_by_id(self, user_id: str) -> User:
        resp = self.table.get_item(
            Key={
                "PK": "USERS",
                "SK": f"Users#{user_id}",
            },
            ConsistentRead=True,
        )

        item = resp.get("Item")
        if not item:
            raise error.NotFoundError("entity not found")

        return User.from_ddb(item)

    def create(self, user: User) -> None:
        try:
            self.table.meta.client.transact_write_items(
                TransactItems=[
                    {
                        "Put": {
                            "TableName": self.table.name,
                            "Item": {
                                "PK": "USERS",
                                "SK": f"Users#{user.ID}",
                                "UserId": user.ID,
                                "Username": user.Username,
                                "Password": user.Password,
                                "Role": (
                                    user.Role.value
                                    if hasattr(user.Role, "value")
                                    else user.Role
                                ),
                                "Email": user.Email,
                                "Address": user.Address,
                                "Flat_no": user.FlatNo,
                                "Tower": user.Tower,
                            },
                        }
                    },
                    {
                        "Put": {
                            "TableName": self.table.name,
                            "Item": {
                                "PK": "USERS",
                                "SK": f"EMAIL#{user.Email.lower()}",
                                "UserId": user.ID,
                            },
                            "ConditionExpression": "attribute_not_exists(SK)",
                        }
                    },
                    {
                        "Put": {
                            "TableName": self.table.name,
                            "Item": {
                                "PK": "USERS",
                                "SK": f"Tower#{user.Tower}#Flat_no#{user.FlatNo}",
                                "UserId": user.ID,
                                "Flat_no": user.FlatNo,
                                "Tower": user.Tower,
                            },
                        }
                    },
                ]
            )
        except ClientError as e:
            print("DynamoDB ERROR:", e.response)
            raise error.RepositoryError("failed to create user") from e

    def create_gatekeeper(self, user: User) -> None:
        self.table.meta.client.transact_write_items(
            TransactItems=[
                {
                    "Put": {
                        "TableName": self.table.name,
                        "Item": {
                            "PK": "USERS",
                            "SK": f"Users#{user.ID}",
                            "UserId": user.ID,
                            "Username": user.Username,
                            "Password": user.Password,
                            "Role": (
                                user.Role.value
                                if hasattr(user.Role, "value")
                                else user.Role
                            ),
                            "Email": user.Email,
                            "Address": user.Address,
                            "Flat_no": user.FlatNo,
                            "Tower": user.Tower,
                        },
                    }
                },
                {
                    "Put": {
                        "TableName": self.table.name,
                        "Item": {
                            "PK": "USERS",
                            "SK": f"EMAIL#{user.Email.lower()}",
                            "UserId": user.ID,
                        },
                    }
                },
            ]
        )

    def delete(self, user_id: str) -> None:
        user = self.get_user_by_id(user_id)
        transact_items = [
            {
                "Delete": {
                    "TableName": self.table.name,
                    "Key": {"PK": "USERS", "SK": f"Users#{user_id}"},
                }
            },
            {
                "Delete": {
                    "TableName": self.table.name,
                    "Key": {
                        "PK": "USERS",
                        "SK": f"EMAIL#{user.Email.lower()}",
                    },
                }
            },
        ]

        if user.Role == UserRole.OWNER or user.Role == "owner":
            transact_items.append(
                {
                    "Delete": {
                        "TableName": self.table.name,
                        "Key": {
                            "PK": "USERS",
                            "SK": f"Tower#{user.Tower}#Flat_no#{user.FlatNo}",
                        },
                    }
                }
            )

        self.table.meta.client.transact_write_items(TransactItems=transact_items)

    def get_all_users(self) -> List[User]:
        resp = self.table.query(
            KeyConditionExpression=Key("PK").eq("USERS")
            & Key("SK").begins_with("Users#")
        )
        return [User.from_ddb(i) for i in resp.get("Items", [])]

    def get_owner_by_tower_and_flat(self, tower: str, flat_no: str) -> User:
        resp = self.table.get_item(
            Key={
                "PK": "USERS",
                "SK": f"Tower#{tower}#Flat_no#{flat_no}",
            }
        )
        item = resp.get("Item")
        if not item:
            raise error.NotFoundError("owner not found")

        return self.get_user_by_id(item["UserId"])

    def get_users_count(self) -> UsersCount:

        owner_count = 0
        gatekeeper_count = 0
        last_evaluated_key = None

        while True:
            query_kwargs = {
                "KeyConditionExpression": (
                    Key("PK").eq("USERS") & Key("SK").begins_with("Users#")
                ),
                "ProjectionExpression": "#r",
                "ExpressionAttributeNames": {
                    "#r": "Role",
                },
            }

            if last_evaluated_key:
                query_kwargs["ExclusiveStartKey"] = last_evaluated_key

            resp = self.table.query(**query_kwargs)
            print("ITEMS:", resp.get("Items"))

            for item in resp.get("Items", []):
                role = item.get("Role")
                if role == UserRole.OWNER.value:
                    owner_count += 1
                elif role == UserRole.GATEKEEPER.value:
                    gatekeeper_count += 1

            last_evaluated_key = resp.get("LastEvaluatedKey")
            if not last_evaluated_key:
                break

        return UsersCount(
            Owner=owner_count,
            Gatekeeper=gatekeeper_count,
        )
