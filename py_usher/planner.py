import re
import sqlite3
import json
import datetime
from typing import *
from .database import DBHandler


def validate_op(func: Callable) -> bool:
    """Validate that the provided function is callable."""
    return callable(func)


def sanitize_input(input_string: str) -> str:
    """Replace any non-alphanumeric character with an empty string and trim whitespaces form both ends"""
    sanitized_input = re.sub(r'\W+', '', input_string)
    sanitized_input = sanitized_input.strip()
    return sanitized_input


now = datetime.datetime.now().timestamp()


class Planner:
    """
    The Planner unit is responsible for storing and fetching the event types and their various operations.
    """
    def __init__(self):
        self.__db = DBHandler()
        try:
            self.__db.create_table()
        except sqlite3.OperationalError:
            pass

    def submit_operation(self, event_type: str, func: Callable) -> dict:
        try:
            response = self.__db.insert_new(event_type, func.__name__)
            return response
        except Exception as err:
            return {"error_message": err, "event_type": event_type, "func": func.__name__, "status_code": 500}

    def del_operation(self, event_type: str, operation_name: str) -> Optional:
        try:
            response = self.__db.del_operation(event_type, operation_name)
            return response
        except Exception as err:
            return {"error_message": err, "event_type": event_type, "func": operation_name, "status_code": 500}

    def del_event(self, event_type: str) -> dict:
        try:
            response = self.__db.del_event(event_type)
            return response
        except Exception as err:
            return {"error_message": err, "event_type": event_type, "status_code": 500}

    def __output_operations(self, response: dict) -> NoReturn:
        output_op = self.__db.fetch_event("output_operations")
        if not output_op:
            return response
        for operation in output_op:
            operation(response)

    def event_details(self, event_type: str) -> List[str]:
        event_operations = self.__db.fetch_event(event_type)
        return event_operations

    def event_ops(self, event_type: str) -> json or None:
        event = self.__db.fetch_event(event_type)
        if event:
            event_operations = event[2]
            return json.loads(event_operations)
        return None
