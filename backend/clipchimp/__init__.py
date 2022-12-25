from celery.result import AsyncResult
from fastapi import FastAPI

from clipchimp import tasks
from clipchimp.config import DELTA_PATTERN, DOWNLOADS, ZERO_SECONDS, DownloadsMount
from clipchimp.models import DownloadParameters


app = FastAPI()
app.mount("/downloads", DownloadsMount(), name="downloads")


@app.get("/api/validate")
async def validate(
    url: str,
    start: str = ZERO_SECONDS,
    end: str = ZERO_SECONDS,
) -> dict:
    """Validate the provided parameters and return a normalised URL."""
    # Ensure that the provided start and end are valid
    if not DELTA_PATTERN.match(start):
        start = ZERO_SECONDS
    if not DELTA_PATTERN.match(end):
        end = ZERO_SECONDS
    return DownloadParameters(url=url, start=start, end=end).json()  # type: ignore


@app.get("/api/download")
async def download(
    url: str,
    start: str = ZERO_SECONDS,
    end: str = ZERO_SECONDS,
) -> dict:
    """Queue up a download for the provided video segment and return an ID."""
    params = DownloadParameters(url=url, start=start, end=end)  # type: ignore
    result = tasks.download_segment.apply_async(
        (params.url, str(params.start), str(params.end)), task_id=params.id
    )
    return {"status": result.state, "id": params.id}


@app.get("/api/status")
async def status(task: str) -> dict:
    """Given a task ID, check on progress of the download."""
    result = AsyncResult(task, app=tasks.app)
    response = {
        "status": result.state,
        "progress": 0,
    }
    metadata = result.info or {}
    if "progress" in metadata:
        response["progress"] = metadata["progress"]

    if result.state == "SUCCESS":
        for file in DOWNLOADS.glob(f"{task}.*"):
            if file.suffix == ".part":
                continue
            # File must be fully downloaded
            response["download"] = str(file)
    return response
