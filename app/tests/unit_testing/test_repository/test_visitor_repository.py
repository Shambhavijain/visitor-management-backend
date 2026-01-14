import unittest
from unittest.mock import MagicMock
from botocore.exceptions import ClientError

from src.repository.visitor_repository import DDBVisitorRepository
from src.models.visitor import Visitor
from src.constants.visitor_enum import VisitorStatus
from src.errors.error import RepositoryError


def make_visitor(visitor_id="v1", owner_id="o1"):
    return Visitor(
        ID=visitor_id,
        Name="guest",
        Email="guest@test.com",
        Tower="A",
        FlatNo="101",
        AddedByRole="owner",
        Status=VisitorStatus.PENDING,
        OwnerEmail="owner@test.com",
        OwnerID=owner_id,
        CreatedAt=123456,
    )


class TestVisitorRepository(unittest.TestCase):

    def setUp(self):
        self.mock_ddb = MagicMock()
        self.mock_table = MagicMock()
        self.mock_ddb.Table.return_value = self.mock_table

        self.repo = DDBVisitorRepository(self.mock_ddb, "test-table")


    def test_create_visitor_success(self):
        visitor = make_visitor()

        self.repo.create(visitor)

        self.mock_table.put_item.assert_called_once()

    def test_create_visitor_client_error(self):
        self.mock_table.put_item.side_effect = ClientError(
            {"Error": {"Code": "InternalError"}}, "PutItem"
        )

        with self.assertRaises(RepositoryError):
            self.repo.create(make_visitor())


    def test_get_all_visitors_success(self):
        self.mock_table.query.side_effect = [
            {
                "Items": [
                    {
                        "PK": "VISITORS",
                        "SK": "VISITOR#o1#v1",
                        "ID": "v1",
                        "Name": "guest",
                        "Email": "guest@test.com",
                        "Tower": "A",
                        "FlatNo": "101",
                        "AddedByRole": "owner",
                        "Status": "pending",
                        "OwnerEmail": "owner@test.com",
                        "OwnerID": "o1",
                        "CreatedAt": 123,
                    }
                ]
            }
        ]

        visitors = self.repo.get_all_visitors()

        self.assertEqual(len(visitors), 1)
        self.assertEqual(visitors[0].ID, "v1")

    def test_get_all_visitors_client_error(self):
        self.mock_table.query.side_effect = ClientError(
            {"Error": {"Code": "InternalError"}}, "Query"
        )

        with self.assertRaises(RepositoryError):
            self.repo.get_all_visitors()


    def test_get_visitors_by_owner_success(self):
        self.mock_table.query.return_value = {
            "Items": [
                {
                    "PK": "VISITORS",
                    "SK": "VISITOR#o1#v1",
                    "ID": "v1",
                    "Name": "guest",
                    "Email": "guest@test.com",
                    "Tower": "A",
                    "FlatNo": "101",
                    "AddedByRole": "owner",
                    "Status": "pending",
                    "OwnerEmail": "owner@test.com",
                    "OwnerID": "o1",
                    "CreatedAt": 123,
                }
            ]
        }

        visitors = self.repo.get_visitors_by_owner("o1")

        self.assertEqual(len(visitors), 1)
        self.assertEqual(visitors[0].OwnerID, "o1")

    def test_get_visitors_by_owner_client_error(self):
        self.mock_table.query.side_effect = ClientError(
            {"Error": {"Code": "InternalError"}}, "Query"
        )

        with self.assertRaises(RepositoryError):
            self.repo.get_visitors_by_owner("o1")


    def test_count_visitors(self):
        self.mock_table.query.side_effect = [
            {"Count": 2, "LastEvaluatedKey": {"PK": "VISITORS"}},
            {"Count": 1},
        ]

        count = self.repo.count_visitors()

        self.assertEqual(count, 3)

    def test_count_visitors_by_owner(self):
        self.mock_table.query.side_effect = [
            {"Count": 1, "LastEvaluatedKey": {"PK": "VISITORS"}},
            {"Count": 2},
        ]

        count = self.repo.count_visitors_by_owner("o1")

        self.assertEqual(count, 3)


    def test_update_visitor_status_success(self):
        self.repo.update_visitor_status("v1", "o1", VisitorStatus.APPROVED)

        self.mock_table.update_item.assert_called_once()

    def test_update_visitor_status_client_error(self):
        self.mock_table.update_item.side_effect = ClientError(
            {"Error": {"Code": "InternalError"}}, "UpdateItem"
        )

        with self.assertRaises(RepositoryError):
            self.repo.update_visitor_status("v1", "o1", VisitorStatus.APPROVED)
