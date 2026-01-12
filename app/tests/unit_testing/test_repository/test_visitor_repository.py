from tests.unit_testing.test_repository.base import DynamoDBTestCase
from botocore.exceptions import ClientError
from unittest.mock import patch

from src.constants.visitor_enum import VisitorStatus
from src.models.user import User
from src.models.visitor import Visitor
from src.constants.role_enum import UserRole
from src.constants.visitor_enum import VisitorStatus
from src.errors.error import RepositoryError


def make_owner_user(user_id="o1"):
    return User(
        ID=user_id,
        Username="owner",
        Email="owner@test.com",
        Password="hashed",
        Role=UserRole.OWNER,
        Address="addr",
        FlatNo="101",
        Tower="A",
    )


def make_gatekeeper_user(user_id="g1"):
    return User(
        ID=user_id,
        Username="gate",
        Email="gate@test.com",
        Password="hashed",
        Role=UserRole.GATEKEEPER,
        Address="addr",
        FlatNo=None,
        Tower=None,
    )


def make_visitor(visitor_id="v1", owner_id="o1"):
    return Visitor(
        ID=visitor_id,
        Name="guest",
        Email="v@test.com",
        Tower="A",
        FlatNo="101",
        AddedByRole="owner",
        Status=VisitorStatus.PENDING,
        OwnerEmail="o@test.com",
        OwnerID=owner_id,
        CreatedAt=123,
    )


class TestVisitorRepository(DynamoDBTestCase):

    def test_create_and_get_all_visitors(self):
        visitor = Visitor(
            ID="v1",
            Name="guest",
            Email="v@test.com",
            Tower="A",
            FlatNo="101",
            AddedByRole="owner",
            Status=VisitorStatus.APPROVED,
            OwnerEmail="o@test.com",
            OwnerID="o1",
            CreatedAt=123,
        )

        self.visitor_repo.create(visitor)

        visitors = self.visitor_repo.get_all_visitors()
        self.assertEqual(len(visitors), 1)

    def test_get_visitors_by_owner(self):
        visitor = Visitor(
            ID="v1",
            Name="guest",
            Email="v@test.com",
            Tower="A",
            FlatNo="101",
            AddedByRole="owner",
            Status=VisitorStatus.PENDING,
            OwnerEmail="o@test.com",
            OwnerID="o1",
            CreatedAt=123,
        )

        self.visitor_repo.create(visitor)

        visitors = self.visitor_repo.get_visitors_by_owner("o1")
        self.assertEqual(len(visitors), 1)

    def test_count_visitors(self):
        for i in range(3):
            self.visitor_repo.create(
                Visitor(
                    ID=str(i),
                    Name="guest",
                    Email="v@test.com",
                    Tower="A",
                    FlatNo="101",
                    AddedByRole="owner",
                    Status=VisitorStatus.APPROVED,
                    OwnerEmail="o@test.com",
                    OwnerID="o1",
                    CreatedAt=123,
                )
            )

        self.assertEqual(self.visitor_repo.count_visitors(), 3)
        self.assertEqual(self.visitor_repo.count_visitors_by_owner("o1"), 3)

    def test_update_visitor_status(self):
        visitor = Visitor(
            ID="v1",
            Name="guest",
            Email="v@test.com",
            Tower="A",
            FlatNo="101",
            AddedByRole="owner",
            Status=VisitorStatus.PENDING,
            OwnerEmail="o@test.com",
            OwnerID="o1",
            CreatedAt=123,
        )

        self.visitor_repo.create(visitor)

        self.visitor_repo.update_visitor_status("v1", "o1", VisitorStatus.APPROVED)

        updated = self.visitor_repo.get_visitors_by_owner("o1")[0]
        self.assertEqual(updated.Status, VisitorStatus.APPROVED)

    def test_create_visitor_client_error(self):
        visitor = make_visitor()
        with patch.object(
            self.visitor_repo.table,
            "put_item",
            side_effect=ClientError({"Error": {"Code": "InternalError"}}, "PutItem"),
        ):
            with self.assertRaises(RepositoryError):
                self.visitor_repo.create(visitor)

    def test_get_all_visitors_multiple(self):
        self.visitor_repo.create(make_visitor("v1"))
        self.visitor_repo.create(make_visitor("v2"))
        visitors = self.visitor_repo.get_all_visitors()
        self.assertEqual(len(visitors), 2)

    def test_get_visitors_by_owner_client_error(self):
        with patch.object(
            self.visitor_repo.table,
            "query",
            side_effect=ClientError({"Error": {"Code": "InternalError"}}, "Query"),
        ):
            with self.assertRaises(RepositoryError):
                self.visitor_repo.get_visitors_by_owner("o1")

    def test_update_visitor_status_client_error(self):
        with patch.object(
            self.visitor_repo.table,
            "update_item",
            side_effect=ClientError({"Error": {"Code": "InternalError"}}, "UpdateItem"),
        ):
            with self.assertRaises(RepositoryError):
                self.visitor_repo.update_visitor_status(
                    "v1", "o1", VisitorStatus.APPROVED
                )
