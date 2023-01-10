from django.test import TestCase

from form_checker.services import FormType, ServiceMongoClient
from service import status


class FormCheckerTest(TestCase):
    service_obj = ServiceMongoClient()
    collection = service_obj.get_collection_form_checker()

    def setUp(self):
        # Generate test forms
        form_1 = {
            "name": "Name form 1",
            "field_name_1": FormType.EMAIL.value,
            "field_name_2": FormType.PHONE_NUMBER.value
        }
        self.collection.insert_one(form_1)

        form_2 = {
            "name": "Name form 2",
            "user_login": FormType.TEXT.value,
            "user_phone": FormType.PHONE_NUMBER.value,
            "user_email": FormType.EMAIL.value,
            "last_login_date": FormType.DATE.value,
        }
        self.collection.insert_one(form_2)

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

    def test_get_form_1(self):
        post_data = {
            "field_name_1": "some@maiil.ru",
            "field_name_2": "+79993335577"
        }
        response = self.client.post(
            path='/get_form/',
            data=post_data
        )
        assert_response_data = {
            "name": "Name form 1",
        }
        self.assertEqual(response.json(), assert_response_data)

    def test_get_form_1_not_all_fields(self):
        post_data = {
            "field_name_1": "some@maiil.ru",
        }
        response = self.client.post(
            path='/get_form/',
            data=post_data
        )
        assert_response_data = {
            'field_name_1': 'email',
        }
        self.assertEqual(response.json(), assert_response_data)

    def test_get_form_1_more_fields(self):
        post_data = {
            "field_name_0": "2023-01-09",
            "field_name_1": "some@maiil.ru",
            "field_name_2": "+79993335577",
            "field_name_3": "Test text",
        }
        response = self.client.post(
            path='/get_form/',
            data=post_data
        )
        assert_response_data = {
            "name": "Name form 1",
        }
        self.assertEqual(response.json(), assert_response_data)

    def test_get_form_2(self):
        post_data = {
            "user_login": "Text login",
            "user_phone": "+79513456789",
            "user_email": "my@mail.ru",
            "last_login_date": "09.01.2023",
        }
        response = self.client.post(
            path='/get_form/',
            data=post_data
        )
        assert_response_data = {
            "name": "Name form 2",
        }
        self.assertEqual(response.json(), assert_response_data)

    def tearDown(self) -> None:
        self.service_obj.close_mongo_client()
