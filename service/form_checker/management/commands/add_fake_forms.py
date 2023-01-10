"""
Command add some fake forms into MongoDB
"""
from random import choice, randint

from django.core.management import BaseCommand
from faker import Faker

from form_checker.services import FormType, ServiceMongoClient


class Command(BaseCommand):
    MAX_FIELD_COUNT = 5
    fake = Faker()

    def add_arguments(self, app):
        app.add_argument(
            'number_of_fake_forms',
            type=int,
            help='Number of fake forms for testing',
        )

    def get_fake_form(self) -> dict:
        fake_form = {
            'name': self.fake.city()
        }
        for field in range(randint(1, self.MAX_FIELD_COUNT)):
            fake_form.update({
                self.fake.first_name(): choice(list(FormType)).value
            })
        return fake_form

    def handle(self, *args, **options):

        service_obj = ServiceMongoClient()
        collection = service_obj.get_collection_form_checker()

        # Generate forms
        for item in range(options['number_of_fake_forms']):
            collection.insert_one(self.get_fake_form())

        service_obj.close_mongo_client()

        print(f"Added {options['number_of_fake_forms']} fake forms in {collection.full_name}")
