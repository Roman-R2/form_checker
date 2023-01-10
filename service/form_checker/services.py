import os
import re
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum

from email_validate import validate
from pymongo import MongoClient
from pymongo.errors import CollectionInvalid


class FormType(Enum):
    EMAIL = 'email'
    PHONE_NUMBER = 'phone'
    DATE = 'date'
    TEXT = 'text'


class DataDTO:
    def __init__(self, data, data_type: FormType):
        self.data = data
        self.data_type = data_type

    def __str__(self):
        return f"DataDTO {self.data} ::: {self.data_type}"


# Chain of Responsibility
class Handler(ABC):
    @abstractmethod
    def handle(self, data: DataDTO):
        pass


# YYYY-MM-DD или DD.MM.YYYY
class DateTypeHandler(Handler):
    """ Check data for date type. """

    # refactoring is required
    def handle(self, data: DataDTO):
        try:
            datetime.strptime(data.data, "%d.%m.%Y")
            return DataDTO(data=data.data, data_type=FormType.DATE)
        except ValueError:
            pass

        try:
            datetime.strptime(data.data, "%Y-%m-%d")
            return DataDTO(data=data.data, data_type=FormType.DATE)
        except ValueError:
            pass

        return data


class PhoneTypeHandler(Handler):
    """
    Check for phone number
    """

    def handle(self, data: DataDTO):
        this_data = data.data.replace(' ', '')
        match = re.fullmatch("^((\+7|7|8)+([0-9]){10})$", this_data)
        return DataDTO(data=data.data, data_type=FormType.PHONE_NUMBER) if match else data


class EmailTypeHandler(Handler):
    """
    Check for email
    """

    def handle(self, data: DataDTO):
        return DataDTO(data=data.data, data_type=FormType.EMAIL) if validate(email_address=data.data) else data


class TextTypeHandler(Handler):
    """
    Check for text
    """

    def handle(self, data: DataDTO):
        # return by default
        return data


class TypeValidationChain:
    def __init__(self):
        self.handlers = []

    def add_handler(self, handler: Handler):
        self.handlers.append(handler)

    def handle(self, data):
        for handler in self.handlers:
            data = handler.handle(data)

        return data


class ProcessTypeValidationChain:

    def __init__(self, data):
        self.data = DataDTO(data, FormType.TEXT)
        self.validation_chain = TypeValidationChain()
        self._setup_chain()

    def _setup_chain(self):
        self.validation_chain.add_handler(DateTypeHandler())
        self.validation_chain.add_handler(PhoneTypeHandler())
        self.validation_chain.add_handler(EmailTypeHandler())
        self.validation_chain.add_handler(TextTypeHandler())

    def get_data_dto(self) -> DataDTO:
        return self.validation_chain.handle(self.data)


class ServiceMongoClient:
    def __init__(self):
        self.mongo_client = MongoClient(os.getenv('MONGO_DB_URI'))
        self.db = self.mongo_client[os.getenv('MONGO_DB_NAME')]

    def get_collection_form_checker(self):
        form_collection_name = os.getenv('FORM_COLLECTION_NAME')
        try:
            collection = self.db.create_collection(name=form_collection_name)
        except CollectionInvalid:
            collection = self.db.get_collection(name=form_collection_name)
        return collection

    def close_mongo_client(self):
        self.mongo_client.close()


class FindSuitableFormInDB:
    """ Find suitable form in DB. """

    def __init__(self, form_canvas):
        self.form_canvas = form_canvas
        self.mongo_client = ServiceMongoClient()
        self.form_checker_collection = self.mongo_client.get_collection_form_checker()

    # Refactoring required
    def conclusion(self):
        # Select the appropriate form fields
        temp_query_results = {}
        temp_query_id = None
        for key, value in self.form_canvas.items():
            temp_form_result = self.form_checker_collection.find_one({key: value})
            if temp_query_id is None and temp_form_result is not None:
                temp_query_id = temp_form_result['_id']
            if temp_form_result is not None and temp_query_id == temp_form_result['_id']:
                temp_query_results.update({
                    key: value,
                })

        finish_query_result = self.form_checker_collection.find_one(temp_query_results)
        # Close mongo_client connection
        self.mongo_client.close_mongo_client()
        if finish_query_result is None:
            return None

        # If count of fields not equal that means not suitable form
        if len(finish_query_result) - 2 != len(temp_query_results):
            finish_query_result = None
        return finish_query_result
