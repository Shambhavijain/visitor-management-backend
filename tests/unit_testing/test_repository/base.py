import unittest
import boto3
from moto import mock_aws

from src.repository.user_repository import DDBUserRepository
from src.repository.visitor_repository import DDBVisitorRepository


class DynamoDBTestCase(unittest.TestCase):

    TABLE_NAME = "test-table"

    def setUp(self):
        self.mock = mock_aws()
        self.mock.start()

        self.ddb = boto3.resource("dynamodb", region_name="us-east-1")

        self.table = self.ddb.create_table(
            TableName=self.TABLE_NAME,
            KeySchema=[
                {"AttributeName": "PK", "KeyType": "HASH"},
                {"AttributeName": "SK", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "PK", "AttributeType": "S"},
                {"AttributeName": "SK", "AttributeType": "S"},
            ],
            BillingMode="PAY_PER_REQUEST",
        )

        self.table.wait_until_exists()

        self.user_repo = DDBUserRepository(self.ddb, self.TABLE_NAME)
        self.visitor_repo = DDBVisitorRepository(self.ddb, self.TABLE_NAME)

    def tearDown(self):
        self.mock.stop()
