from datetime import timedelta
from temporalio import workflow

# Import activity, passing it through the sandbox without reloading the module
with workflow.unsafe.imports_passed_through():
    from .activities import api_call_activity


@workflow.defn
class ApiCallWorkflow:
    @workflow.run
    async def run(self, api_call_count: int = 1000) -> list[dict | BaseException]:
        return await workflow.execute_activity(
            api_call_activity,
            api_call_count,
            start_to_close_timeout=timedelta(seconds=3),
        )
