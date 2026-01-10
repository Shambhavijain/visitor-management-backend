from unittest.mock import Mock, patch
from botocore.exceptions import ClientError


from src.models.user import User
from src.constants.role_enum import UserRole
from src.errors.error import NotFoundError, RepositoryError
from tests.unit_testing.test_repository.base import DynamoDBTestCase
from src.models.user import User
from src.constants.role_enum import UserRole


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
        Username="gatekeeper",
        Email="gate@test.com",
        Password="hashed",
        Role=UserRole.GATEKEEPER,
        Address="addr",
        FlatNo=None,
        Tower=None,
    )


class TestUserRepository(DynamoDBTestCase):

    def test_create_and_get_user(self):
        user = User(
            ID="u1",
            Username="john",
            Email="john@test.com",
            Password="hashed",
            Role=UserRole.OWNER,
            Address="addr",
            FlatNo="101",
            Tower="A",
        )

        self.user_repo.create(user)

        fetched = self.user_repo.get_user_by_id("u1")

        self.assertEqual(fetched.ID, "u1")
        self.assertEqual(fetched.Email, "john@test.com")

    def test_get_by_email_not_found(self):
        with self.assertRaises(NotFoundError):
            self.user_repo.get_by_email("missing@test.com")

    def test_get_owner_by_tower_and_flat(self):
        user = User(
            ID="o1",
            Username="owner",
            Email="owner@test.com",
            Password="hashed",
            Role=UserRole.OWNER,
            Address="addr",
            FlatNo="101",
            Tower="A",
        )

        self.user_repo.create(user)

        owner = self.user_repo.get_owner_by_tower_and_flat("A", "101")

        self.assertEqual(owner.ID, "o1")

    def test_get_all_users(self):
        for i in range(2):
            self.user_repo.create(
                User(
                    ID=str(i),
                    Username=f"u{i}",
                    Email=f"u{i}@test.com",
                    Password="pwd",
                    Role=UserRole.OWNER,
                    Address="addr",
                    FlatNo=str(100 + i),
                    Tower="A",
                )
            )

        users = self.user_repo.get_all_users()
        self.assertEqual(len(users), 2)

    def test_get_users_count(self):
        self.user_repo.create(
            User(
                ID="o1",
                Username="owner",
                Email="o@test.com",
                Password="pwd",
                Role=UserRole.OWNER,
                Address="addr",
                FlatNo="101",
                Tower="A",
            )
        )

        self.user_repo.create_gatekeeper(
            User(
                ID="g1",
                Username="gate",
                Email="g@test.com",
                Password="pwd",
                Role=UserRole.GATEKEEPER,
                Address="addr",
                FlatNo=None,
                Tower=None,
            )
        )

        counts = self.user_repo.get_users_count()

        self.assertEqual(counts.Owner, 1)
        self.assertEqual(counts.Gatekeeper, 1)

    def test_create_user_client_error(self):
        user = make_owner_user()
        with patch.object(
            self.user_repo.table.meta.client,
            "transact_write_items",
            side_effect=ClientError(
                {"Error": {"Code": "InternalError"}}, "TransactWriteItems"
            ),
        ):
            with self.assertRaises(RepositoryError):
                self.user_repo.create(user)

    def test_delete_owner_removes_tower_flat_index(self):
        user = make_owner_user()
        self.user_repo.create(user)
        self.user_repo.delete(user.ID)
        with self.assertRaises(NotFoundError):
            self.user_repo.get_owner_by_tower_and_flat("A", "101")

    def test_get_owner_by_tower_flat_not_found(self):
        with self.assertRaises(NotFoundError):
            self.user_repo.get_owner_by_tower_and_flat("Z", "999")

    def test_create_gatekeeper(self):
        user = make_gatekeeper_user()
        self.user_repo.create_gatekeeper(user)
        fetched = self.user_repo.get_user_by_id(user.ID)
        self.assertEqual(fetched.Role, UserRole.GATEKEEPER)
