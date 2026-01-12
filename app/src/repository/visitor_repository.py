import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from abc import ABC, abstractmethod
from typing import List

from src.models.visitor import Visitor, VisitorStatus
from src.errors import error


class VisitorRepository(ABC):

    @abstractmethod
    def create(self, visitor: Visitor) -> None:
        ...

    @abstractmethod
    def get_all_visitors(self) -> List[Visitor]:
        ...

    @abstractmethod
    def get_visitors_by_owner(self, owner_id: str) -> List[Visitor]:
        ...

    @abstractmethod
    def count_visitors(self) -> int:
        ...

    @abstractmethod
    def update_visitor_status(
        self,
        visitor_id: str,
        owner_id: str,
        status: VisitorStatus
    ) -> None:
        ...

    @abstractmethod
    def count_visitors_by_owner(
        self,
        owner_id: str
    ) -> int :
         ...   




class DDBVisitorRepository(VisitorRepository):

    def __init__(
        self,
        ddb_resource: boto3.resources.base.ServiceResource,
        table_name: str
    ):
        self.table = ddb_resource.Table(table_name)

    
    def create(self, visitor: Visitor) -> None:
        try:
            self.table.put_item(
                Item={
                    "PK": "VISITORS",
                    "SK": f"VISITOR#{visitor.OwnerID}#{visitor.ID}",
                    "ID": visitor.ID,
                    "Name": visitor.Name,
                    "Email": visitor.Email,
                    "Tower": visitor.Tower,
                    "FlatNo": visitor.FlatNo,
                    "AddedByRole": visitor.AddedByRole.value,
                    "Status": visitor.Status.value,
                    "OwnerEmail": visitor.OwnerEmail,
                    "OwnerID": visitor.OwnerID,
                    "CreatedAt": visitor.CreatedAt,
                    }
                )
        except ClientError as e:
            raise error.RepositoryError("failed to create visitor") from e

    def get_all_visitors(self) -> List[Visitor]:
        try:
            visitors: List[Visitor] = []
            last_evaluated_key = None
            
            while True:
                query_kwargs = {
                    "KeyConditionExpression": (
                        Key("PK").eq("VISITORS") &
                        Key("SK").begins_with("VISITOR#")
                        )
                }
                
                if last_evaluated_key:
                    query_kwargs["ExclusiveStartKey"] = last_evaluated_key

                resp = self.table.query(**query_kwargs)

                items = resp.get("Items", [])
                visitors.extend(Visitor.from_ddb(item) for item in items)

                last_evaluated_key = resp.get("LastEvaluatedKey")
                if not last_evaluated_key:
                    break

            return visitors

        except ClientError as e:
            raise error.RepositoryError("failed to fetch visitors") from e

  
    def get_visitors_by_owner(self, owner_id: str) -> List[Visitor]:
        try:
            resp = self.table.query(
                KeyConditionExpression=(
                    Key("PK").eq("VISITORS") &
                    Key("SK").begins_with(f"VISITOR#{owner_id}")
                )
            )
            return [Visitor.from_ddb(item) for item in resp.get("Items", [])]
        except ClientError as e:
            raise error.RepositoryError("failed to fetch owner visitors") from e

  
    def count_visitors(self) -> int:
        count = 0
        last_key = None

        while True:
            kwargs = {
                "KeyConditionExpression": (
                    Key("PK").eq("VISITORS") &
                    Key("SK").begins_with("VISITOR#")
                    ),
                "Select": "COUNT",
            }

            if last_key:
                kwargs["ExclusiveStartKey"] = last_key
            
            resp = self.table.query(**kwargs)
            count += resp.get("Count", 0)
            last_key = resp.get("LastEvaluatedKey")
            if not last_key:
                break
        return count


    
    def update_visitor_status(
        self,
        visitor_id: str,
        owner_id: str,
        status: VisitorStatus
    ) -> None:
        try:
            self.table.update_item(
                Key={
                    "PK": "VISITORS",
                    "SK": f"VISITOR#{owner_id}#{visitor_id}",
                },
                UpdateExpression="SET #s = :status",
                ExpressionAttributeNames={
                    "#s": "Status",
                },
                ExpressionAttributeValues={
                    ":status": status.value,
                },
            )
        except ClientError as e:
            raise error.RepositoryError("failed to update visitor status") from e
    def count_visitors_by_owner(self, owner_id: str) -> int:
        count = 0
        last_key = None
        while True:
            kwargs = {
                "KeyConditionExpression": (
                    Key("PK").eq("VISITORS") &
                    Key("SK").begins_with(f"VISITOR#{owner_id}")
                    ),
                "Select": "COUNT",
            }

            if last_key:
                kwargs["ExclusiveStartKey"] = last_key

            resp = self.table.query(**kwargs)
            count += resp.get("Count", 0)
            last_key = resp.get("LastEvaluatedKey")

            if not last_key:
                break

        return count
