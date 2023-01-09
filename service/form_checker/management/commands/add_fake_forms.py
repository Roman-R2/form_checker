"""
Command add some fake forms into MongoDB
"""
import os
from pprint import pprint
from random import randint, choice

from django.conf import settings
from django.core.management import BaseCommand
from pymongo import MongoClient
from pymongo.errors import CollectionInvalid
from faker import Faker

from form_checker.services import FormType


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

        form_collection_name = os.getenv('FORM_COLLECTION_NAME')

        with MongoClient(os.getenv('MONGO_DB_URI')) as client:
            db = client[os.getenv('MONGO_DB_NAME')]
            try:
                collection = db.create_collection(name=os.getenv('FORM_COLLECTION_NAME'))
            except CollectionInvalid:
                print(f"Collection {form_collection_name} already exists")
                collection = db.get_collection(name=form_collection_name)

            # Generate forms
            for item in range(options['number_of_fake_forms']):
                collection.insert_one(self.get_fake_form())

        print(f"Added {options['number_of_fake_forms']} fake forms in {form_collection_name} collection")
