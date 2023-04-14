from typing import *


class Planner:
    """
    The Planner unit is responsible for storing and fetching the event types and their various operations.
    """
    def __init__(self):
        """ The `output` event type is a default event type for handling logging and results of operations. """
        self.__event_types = {"output": []}

    def submit_operation(self, event_type: str, func: Callable) -> dict:
        try:
            if event_type not in self.__event_types:
                self.__event_types[event_type] = []
            self.__event_types[event_type].append(func)
            return {"message": "Operation submitted successfully.", "event_type": event_type, "func": func.__name__,
                    "status_code": 200}
        except Exception as err:
            return {"error_message": err, "event_type": event_type, "func": func.__name__, "status_code": 500}

    def event_exists(self, event_type: str) -> bool:
        if event_type in self.__event_types:
            return True
        return False

    def event_details(self, event_type: str) -> List[Callable]:
        if event_type in self.__event_types:
            return self.__event_types[event_type]
        return []
