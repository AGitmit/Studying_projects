import datetime
from typing import *
from time import perf_counter
from py_shiftmanager import ShiftManager_IO, ShiftManager_Compute
from py_shiftmanager import Logger
from .planner import Planner

"""
The Usher module is responsible for submitting new method and operations to event types under the Planner module,
posting events and executing them, including every operation registered to them on the data sent along with it,
concurrently using threading and ShiftManager_IO or in parallel using multiprocessing and ShiftManager_Compute.
"""

logger = Logger()
now = datetime.datetime.now().timestamp()


class Usher:
    def __init__(self, system: Literal["io", "compute"] = "io", num_of_workers: int = 2, daemon: bool = False, in_q_size: int = 10, out_q_size: int = 15):
        self.__planner = Planner()
        if system == "io":
            self.__manager = ShiftManager_IO(num_of_workers, daemon, in_q_size, out_q_size)
        else:
            self.__manager = ShiftManager_Compute(num_of_workers, daemon, in_q_size, out_q_size)

    def plan_event(self, event_type: str, func: Callable) -> NoReturn:
        response = self.__planner.submit_operation(event_type, func)
        output = self.__planner.event_details("output")
        logger.logger.info(response)
        if not output:
            return response
        for operation in output:
            operation(response)

    def view_event(self, event_type: str) -> List:
        return [func.__name__ for func in self.__planner.event_details(event_type)]

    def start_event(self, event_type: str, *args, **kwargs) -> NoReturn:
        event = self.__planner.event_details(event_type)
        output = self.__planner.event_details("output")
        if not event:
            logger.logger.info({"message": "Event type not found.", "event_type": event_type, "status_code": 400,
                                "timestamp": now})
            return
        start_time = perf_counter()
        with self.__manager as manager:
            for operation in event:
                manager.new_task(operation, *args, **kwargs)
        end_time = perf_counter() - start_time
        results = {"message": "Successful.", "event_type": event_type, "status_code": 200,
                   "total_time": end_time, "timestamp": now, "results": manager.get_results()}
        logger.logger.info(results)
        if not output:
            return results
        for operation in output:
            operation(results)
