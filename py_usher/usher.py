import dill
import datetime
from typing import *
from time import perf_counter
from py_shiftmanager import ShiftManager_IO, ShiftManager_Compute
from .planner import Planner

"""
The Usher module is responsible for submitting new method and operations to event types under the Planner module,
posting events and executing them, including every operation registered to them on the data sent along with it,
concurrently using threading and ShiftManager_IO or in parallel using multiprocessing and ShiftManager_Compute.
"""

now = datetime.datetime.now().timestamp()


class Usher:
    def __init__(self, system: Literal["io", "compute"] = "io",
                 num_of_workers: int = 2, daemon: bool = False, in_q_size: int = 10, out_q_size: int = 15):
        self.__planner = Planner()
        self.__operations = {"output_operations": []}

        if system == "io":
            self.__manager = ShiftManager_IO(num_of_workers, daemon, in_q_size, out_q_size)
        else:
            self.__manager = ShiftManager_Compute(num_of_workers, daemon, in_q_size, out_q_size)

    def plan_event(self, event_type: str, func: Callable) -> NoReturn:
        response = self.__planner.submit_operation(event_type, func)
        if 'error_message' not in response:
            if func.__name__ not in list(self.__operations.keys()):
                self.__operations[func.__name__] = dill.dumps(func)
        # output_op = self.__planner.event_details("output_operations")

    def del_operation(self, event_type: str, func_name: str):
        response = self.__planner.del_operation(event_type, func_name)
        return response

    def del_event(self, event_type: str):
        response = self.__planner.del_event(event_type)
        return response

    def view_event(self, event_type: str) -> List:
        return self.__planner.event_details(event_type)

    def start_event(self, event_type: str, *args, **kwargs) -> NoReturn:
        event = self.__planner.event_ops(event_type)
        # output_op = self.__planner.event_details("output_operations")
        if not event:
            message = {"message": "Event type not found.", "event_type": event_type, "status_code": 400,
                       "timestamp": now}
            return message

        start_time = perf_counter()
        operations_list = event['operations']
        with self.__manager as manager:
            for operation in operations_list:
                ops = [self.__operations[operation] for operation in operations_list if operation in self.__operations]
                [manager.new_task(dill.loads(op), *args, **kwargs) for op in ops]

        results = manager.get_results()
        end_time = perf_counter() - start_time

        message = {"message": "Successful.", "event_type": event_type, "status_code": 200,
                   "total_time": end_time, "timestamp": now, "results": results}
        return message
