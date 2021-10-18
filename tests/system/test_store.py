from models.store import StoreModel
from tests.base_test import BaseTest
import json


class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                response = client.post("/store/Test Store")

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name("Test Store"))
                self.assertDictEqual({'id': 1, 'name': 'Test Store', 'items': []}, json.loads(response.data))

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                client.post("/store/Test Store")
                response = client.post("/store/Test Store")

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({'message': "A store with name 'Test Store' already exists."},
                                     json.loads(response.data))

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                client.post("/store/Test Store")
                response = client.delete("/store/Test Store")

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'message': 'Store deleted'}, json.loads(response.data))

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                client.post("/store/Test Store")
                response = client.get("/store/Test Store")
                expected = {
                    'id': 1,
                    'name': 'Test Store',
                    'items': []
                    }

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(expected, json.loads(response.data))

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                response = client.get("/store/Test Store")

                self.assertEqual(response.status_code, 404)
                self.assertDictEqual({"message": "Store not found"}, json.loads(response.data))

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                client.post("/store/Test Store")
                client.post("/item/Test Item", data={'price': 19.99, 'store_id': 1})
                response = client.get("/store/Test Store")
                expected = {
                    'id': 1,
                    'name': 'Test Store',
                    'items': [
                                {
                                    'name': 'Test Item',
                                    'price': 19.99
                                }
                            ]
                            }
                self.assertDictEqual(expected, json.loads(response.data))

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                client.post("/store/Test Store 1")
                client.post("/store/Test Store 2")
                response = client.get("/stores")
                expected = {'stores': [
                    {
                        'id': 1,
                        'name': 'Test Store 1',
                        'items': []
                     },
                    {
                        'id': 2,
                        'name': 'Test Store 2',
                        'items': []
                     }
                ]
                }
                self.assertDictEqual(expected, json.loads(response.data))

    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                client.post("/store/Test Store 1")
                client.post("/item/Test Item 1", data={'price': 19.99, 'store_id': 1})
                client.post("/store/Test Store 2")
                client.post("/item/Test Item 2", data={'price': 29.99, 'store_id': 2})
                response = client.get("/stores")
                expected = {'stores': [
                    {
                        'id': 1,
                        'name': 'Test Store 1',
                        'items': [
                         {
                             'name': 'Test Item 1',
                             'price': 19.99
                          }
                         ]
                     },
                    {
                        'id': 2,
                        'name': 'Test Store 2',
                        'items': [
                         {
                             'name': 'Test Item 2',
                             'price': 29.99
                          }
                        ]
                     }
                ]
                }
                self.assertDictEqual(expected, json.loads(response.data))
