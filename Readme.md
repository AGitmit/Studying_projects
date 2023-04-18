# Usher Module

The Usher module is responsible for submitting new methods and operations to event types under the *Planner* module, posting events, and executing them. This is done concurrently using threading and **ShiftManager_IO** or in parallel using multiprocessing and **ShiftManager_Compute**.

## Usage
To use the Usher module, import it using `from py-usher.usher import Usher`. Create an instance of Usher, and pass in the following parameters:

`system` - A string literal that specifies the system to be used. Can be "io" or "compute". Default value is "io".  

`num_of_workers` - An integer that specifies the number of workers to use. Default value is 2.  

`daemon` - A boolean value that specifies whether the worker threads/processes should run as daemons. Default value is False.  

`in_q_size` - An integer that specifies the size of the input queue. Default value is 10.  

`out_q_size` - An integer that specifies the size of the output queue. Default value is 15.  

## Methods

The following methods are available in the Usher module:

`plan_event(event_type: str, func: Callable) -> NoReturn`: This method submits a new operation to the specified event type.  

`del_operation(event_type: str, func_name: str) -> Optional`: This method deletes an operation from the specified event type.  

`del_event(event_type: str) -> dict`: This method deletes an event type.  

`view_event(event_type: str) -> List`: This method returns a list of the event type's details.  

`start_event(event_type: str, *args, **kwargs) -> NoReturn`: This method starts an event, executing its operations.