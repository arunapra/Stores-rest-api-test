from models.user import UserModel
from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest
import json


class ItemTest(BaseTest):
    def setUp(self):
        super(ItemTest, self).setUp()
        with self.app() as client:
            with self.app_context():
                UserModel("Test", "1234").save_to_db()
                auth_response = client.post('/auth',
                                            data=json.dumps({'username': 'Test', 'password': '1234'}),
                                            headers={'Content-Type': 'application/json'})
                auth_token = json.loads(auth_response.data)['access_token']
                self.access_token = f'JWT {auth_token}'

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/item/test')
                self.assertEqual(response.status_code, 401)
                self.assertDictEqual({'Message': 'Could not authorize. Did you include a valid authorization header?'},
                                     json.loads(response.data))

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/item/test', headers={'Authorization': self.access_token})
                self.assertEqual(response.status_code, 404)

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('Test Store').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()
                response = client.get('/item/test', headers={'Authorization': self.access_token})
                expected = {'name': 'test',
                            'price': 19.99}
                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(expected, json.loads(response.data))

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('Test Store').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()
                response = client.delete('/item/test')
                expected = {'message': 'Item deleted'}
                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(expected, json.loads(response.data))
                self.assertIsNone(ItemModel.find_by_name('test'))

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('Test Store').save_to_db()

                response = client.post('/item/test', data={'price': 17.99, 'store_id': 1})

                self.assertEqual(response.status_code, 201)
                self.assertDictEqual({'name': 'test', 'price': 17.99}, json.loads(response.data))
                self.assertIsNotNone(ItemModel.find_by_name('test'))

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('Test Store').save_to_db()
                ItemModel('test', 17.99, 1).save_to_db()

                response = client.post('/item/test', data={'price': 17.99, 'store_id': 1})

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({'message': 'An item with name \'test\' already exists.'},
                                     json.loads(response.data))

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('Test Store').save_to_db()

                response = client.put('/item/test', data={'price': 17.99, 'store_id': 1})

                self.assertEqual(response.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test').price, 17.99)
                self.assertDictEqual({'name': 'test', 'price': 17.99}, json.loads(response.data))

    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('Test Store').save_to_db()
                ItemModel('test', 17.99, 1).save_to_db()
                self.assertEqual(ItemModel.find_by_name('test').price, 17.99)

                response = client.put('/item/test', data={'price': 20.99, 'store_id': 1})

                self.assertEqual(response.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test').price, 20.99)
                self.assertDictEqual({'name': 'test', 'price': 20.99}, json.loads(response.data))

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('Test Store').save_to_db()
                ItemModel('test 1', 17.99, 1).save_to_db()
                ItemModel('test 2', 21.99, 1).save_to_db()

                response = client.get('/items')

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'items': [{'name': 'test 1', 'price': 17.99},
                                                {'name': 'test 2', 'price': 21.99}]},
                                     json.loads(response.data))





