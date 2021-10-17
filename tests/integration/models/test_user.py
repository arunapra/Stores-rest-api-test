from models.user import UserModel
from tests.base_test import BaseTest


class UserTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            user = UserModel("Test", "abcd")

            self.assertIsNone(user.find_by_username("Test"))
            self.assertIsNone(user.find_by_id(1))

            user.save_to_db()

            self.assertIsNotNone(user.find_by_username("Test"))
            self.assertIsNotNone(user.find_by_id(1))

