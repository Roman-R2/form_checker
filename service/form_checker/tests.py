import os

from django.test import TestCase, Client
from pymongo import MongoClient
from pymongo.errors import CollectionInvalid

from form_checker.services import FormType
from service import status


class FormCheckerTest(TestCase):
    def setUp(self):
        form_collection_name = os.getenv('FORM_COLLECTION_NAME')

        self.mongo_client = MongoClient(os.getenv('MONGO_DB_URI'))
        db = self.mongo_client[os.getenv('MONGO_DB_NAME')]
        try:
            collection = db.create_collection(name=os.getenv('FORM_COLLECTION_NAME'))
        except CollectionInvalid:
            collection = db.get_collection(name=form_collection_name)

        # Generate test forms
        form_1 = {
            "name": "Name form 1",
            "field_name_1": FormType.EMAIL.value,
            "field_name_2": FormType.PHONE_NUMBER.value
        }
        collection.insert_one(form_1)

        form_2 = {
            "name": "Name form 2",
            "user_login": FormType.TEXT.value,
            "user_phone": FormType.PHONE_NUMBER.value,
            "user_email": FormType.EMAIL.value,
        }
        collection.insert_one(form_2)

    def test_get_form_post(self):
        response = self.client.post('/get_form/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_form_get(self):
        response = self.client.get('/get_form/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_form_delete(self):
        response = self.client.delete('/get_form/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_form_head(self):
        response = self.client.head('/get_form/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_form_no_in_db(self):
        """ Test for get form, which not in DB. """
        post_data = {
            'f_name1': 'my@mail.ru',
            'f_name2': 'Some text',
            'f_name3': '2023-01-09',
            'f_name4': '+71234567890',
        }
        assert_response_data = {
            "f_name1": "email",
            "f_name2": "text",
            "f_name3": "date",
            "f_name4": "phone"
        }
        response = self.client.post(
            path='/get_form/',
            data=post_data
        )
        self.assertEqual(response.json(), assert_response_data)

    def tearDown(self) -> None:
        self.mongo_client.close()
