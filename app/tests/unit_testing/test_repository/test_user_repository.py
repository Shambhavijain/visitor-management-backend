import unittest
from unittest.mock import MagicMock
from botocore.exceptions import ClientError

from src.repository.user_repository import DDBUserRepository
from src.models.user import User, UsersCount
from src.constants.role_enum import UserRole
from src.errors.error import RepositoryError, NotFoundError





def make_owner_user(user_id="u1"):
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
        Username="gatekeeper",
        Email="gate@test.com",
        Password="hashed",
        Role=UserRole.GATEKEEPER,
        Address="addr",
        FlatNo="NA",
        Tower="A",
    )





class TestUserRepository(unittest.TestCase):

    def setUp(self):
        self.mock_ddb = MagicMock()
        self.mock_table = MagicMock()

        self.mock_ddb.Table.return_value = self.mock_table

        self.repo = DDBUserRepository(self.mock_ddb, "test-table")


    def test_create_user_success(self):
        user = make_owner_user()

        self.repo.create(user)

        self.mock_table.meta.client.transact_write_items.assert_called_once()

    def test_create_user_client_error(self):
        self.mock_table.meta.client.transact_write_items.side_effect = ClientError(
            {"Error": {"Code": "InternalError"}}, "TransactWriteItems"
        )

        with self.assertRaises(RepositoryError):
            self.repo.create(make_owner_user())


    def test_create_gatekeeper_success(self):
        user = make_gatekeeper_user()

        self.repo.create_gatekeeper(user)

        self.mock_table.meta.client.transact_write_items.assert_called_once()


    def test_get_user_by_id_success(self):
        self.mock_table.get_item.return_value = {
            "Item": {
                "PK": "USERS",
                "SK": "Users#u1",
                "UserId": "u1",
                "Username": "owner",
                "Email": "owner@test.com",
                "Role": "OWNER",
                "Address": "addr",
                "Flat_no": "101",
                "Tower": "A",
            }
        }

        user = self.repo.get_user_by_id("u1")

        self.assertEqual(user.ID, "u1")
        self.assertEqual(user.Email, "owner@test.com")

    def test_get_user_by_id_not_found(self):
        self.mock_table.get_item.return_value = {}

        with self.assertRaises(NotFoundError):
            self.repo.get_user_by_id("missing")


    def test_get_by_email_success(self):
        self.mock_table.get_item.side_effect = [
            {"Item": {"UserId": "u1"}}, 
            {
                "Item": {
                    "PK": "USERS",
                    "SK": "Users#u1",
                    "UserId": "u1",
                    "Username": "owner",
                    "Email": "owner@test.com",
                    "Role": "OWNER",
                    "Address": "addr",
                    "Flat_no": "101",
                    "Tower": "A",
                }
            },
        ]

        user = self.repo.get_by_email("OWNER@TEST.COM")

        self.assertEqual(user.ID, "u1")

    def test_get_by_email_not_found(self):
        self.mock_table.get_item.return_value = {}

        with self.assertRaises(NotFoundError):
            self.repo.get_by_email("missing@test.com")


    def test_delete_owner_user(self):
        owner = make_owner_user()

        self.repo.get_user_by_id = MagicMock(return_value=owner)

        self.repo.delete(owner.ID)

        args = self.mock_table.meta.client.transact_write_items.call_args[1]
        self.assertEqual(len(args["TransactItems"]), 3)

    def test_delete_gatekeeper_user(self):
        gatekeeper = make_gatekeeper_user()

        self.repo.get_user_by_id = MagicMock(return_value=gatekeeper)

        self.repo.delete(gatekeeper.ID)

        args = self.mock_table.meta.client.transact_write_items.call_args[1]
        self.assertEqual(len(args["TransactItems"]), 2)


    def test_get_all_users(self):
        self.mock_table.query.return_value = {
            "Items": [
                {
                    "PK": "USERS",
                    "SK": "Users#u1",
                    "UserId": "u1",
                    "Username": "owner",
                    "Email": "owner@test.com",
                    "Role": "OWNER",
                    "Address": "addr",
                    "Flat_no": "101",
                    "Tower": "A",
                }
            ]
        }

        users = self.repo.get_all_users()

        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].ID, "u1")


    def test_get_owner_by_tower_and_flat_success(self):
        self.mock_table.get_item.return_value = {"Item": {"UserId": "u1"}}

        self.repo.get_user_by_id = MagicMock(return_value=make_owner_user())

        user = self.repo.get_owner_by_tower_and_flat("A", "101")

        self.assertEqual(user.ID, "u1")

    def test_get_owner_by_tower_and_flat_not_found(self):
        self.mock_table.get_item.return_value = {}

        with self.assertRaises(NotFoundError):
            self.repo.get_owner_by_tower_and_flat("A", "999")


    def test_get_users_count(self):
        self.mock_table.query.side_effect = [
            {
                "Items": [
                    {"Role": "owner"},
                    {"Role": "gatekeeper"},
                    ],
                "LastEvaluatedKey": {"PK": "USERS"},
            },
            {
                "Items": [
                    {"Role": "owner"},
                ]
            },
            ]

        result = self.repo.get_users_count()

        self.assertEqual(result.Owner, 2)
        self.assertEqual(result.Gatekeeper, 1)
