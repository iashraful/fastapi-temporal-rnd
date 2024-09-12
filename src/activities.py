import asyncio
import time
from typing import Any
from temporalio import activity

from src.api_client import get_api_data


@activity.defn
async def api_call_activity(
    api_call_count: int, per_sec_call: int = 100
) -> list[dict[str, Any] | BaseException]:
    _tasks: list[asyncio.Task] = list()
    # Creating asyncio tasks
    for _ in range(api_call_count):
        _tasks.append(
            # TODO: Will update the static URL after successful testing.
            asyncio.create_task(get_api_data(url="http://10.21.179.47:7001/lorem"))
        )

    task_responses: list[dict | BaseException] = list()
    num_of_iterations: int = api_call_count // per_sec_call
    iteration_index = 0
    for _ in range(num_of_iterations + 1):
        # Grav the time :)
        start_time: float = time.time()
        _temp_tasks: list[Any] = _tasks[
            iteration_index : iteration_index + per_sec_call
        ]
        print(_temp_tasks)
        _result: list[dict | BaseException] = await asyncio.gather(
            # Just divide the tasks into seperate calls as per our per second call
            *_temp_tasks,
            return_exceptions=True,
        )
        print(_result)

        time_took: float = time.time() - start_time
        if time_took < 1.0:
            print(f"Sleeping for {1.0-time_took} seconds")
            await asyncio.sleep(1.0 - time_took)

        task_responses += _result
        iteration_index += per_sec_call
    if isinstance(task_responses, BaseException):
        # We can raise custom exception from here. Or handle whatever we like to do,
        print(isinstance)
    return task_responses
