import os
from uuid import uuid4
from fastapi import FastAPI
from temporalio.client import Client
import lorem

from src.workflows import ApiCallWorkflow

app = FastAPI()


@app.get("/")
async def health_handler():
    return {"msg": "OK!"}


@app.get("/lorem")
async def loream_text_handler():
    return {
        "id": uuid4().hex,
        "sentence": lorem.sentence(),
        "paragraph": lorem.paragraph(),
    }


@app.get("/run-workflow")
async def run_workflow_handler():
    # Create client connected to server at the given address
    client = await Client.connect(os.environ.get("TEMOPORAL_SERVICE", "localhost:7233"))

    # Execute a workflow
    result = await client.execute_workflow(
        ApiCallWorkflow.run,
        150,
        id="API-CALL-WORKFLOW",
        task_queue="api-call-activity",
    )
    return result
