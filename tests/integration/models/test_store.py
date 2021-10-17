from models.item import ItemModel
from tests.base_test import BaseTest
from models.store import StoreModel


class StoreTest(BaseTest):
    def test_create_store_items_empty(self):
        store = StoreModel("Test Store")

        self.assertListEqual(store.items.all(), [],
                             " The store items length was not 0, even though no items were added.")

    def test_crud(self):
        with self.app_context():
            store = StoreModel("Test Store")

            self.assertIsNone(StoreModel.find_by_name(store.name))
            store.save_to_db()
            self.assertIsNotNone(StoreModel.find_by_name(store.name))
            store.delete_from_db()
            self.assertIsNone(StoreModel.find_by_name(store.name))

    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel("Test Store")
            item = ItemModel("Test Item", 19.99, 1)

            store.save_to_db()
            item.save_to_db()

            self.assertEqual(store.items.count(), 1)
            self.assertEqual(store.items.first().name, "Test Item")

    def test_store_json(self):
        with self.app_context():
            store = StoreModel("Test Store")
            expected = {
                'id': None,
                'name': 'Test Store',
                'items': []
            }
            self.assertDictEqual(store.json(), expected)

    def test_store_json_with_item(self):
        with self.app_context():
            store = StoreModel("Test Store")
            item = ItemModel("Test Item", 19.99, 1)

            store.save_to_db()
            item.save_to_db()

            expected = {
                'name': 'Test Store',
                'items': [{'name': 'Test Item', 'price': 19.99}]
            }
            self.assertDictEqual(store.json(), expected)
