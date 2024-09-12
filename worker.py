import asyncio
import os

from temporalio.client import Client
from temporalio.worker import Worker

from src.activities import api_call_activity
from src.workflows import ApiCallWorkflow

TEMOPORAL_SERVICE_URL: str = os.environ.get("TEMOPORAL_SERVICE", "127.0.0.1:7233")


async def main():
    client = await Client.connect(TEMOPORAL_SERVICE_URL, namespace="default")
    # Run the worker
    worker = Worker(
        client,
        task_queue="api-call-activity",
        workflows=[ApiCallWorkflow],
        activities=[api_call_activity],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
