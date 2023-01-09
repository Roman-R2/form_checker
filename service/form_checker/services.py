import re
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from email_validate import validate


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
