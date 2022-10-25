import logging
import subprocess
from datetime import timedelta
from os import getenv

from celery import Celery

from clipchimp import logic
from clipchimp.models import DownloadParameters


CLIP_METADATA_PATTERN = r'\{"postId":"%s","startTimeMs":"(.*)","endTimeMs":"(.*)"\}'
REDIS_HOST, REDIS_PORT = getenv("REDIS_HOST"), getenv("REDIS_PORT")

app = Celery(
    "tasks",
    backend=f"redis://{REDIS_HOST}:{REDIS_PORT}",
    broker=f"redis://{REDIS_HOST}:{REDIS_PORT}",
)


@app.task
def download_segment(url: str, start: timedelta, end: timedelta) -> None:
    params = DownloadParameters(url=url, start=start, end=end, post_process=False)  # type: ignore
    command = [
        "yt-dlp",
        "--download-sections",
        f"*{start}-{end}",
        url,
        "-o",
        f"/downloads/{params.id}",
    ]
    logging.info(" ".join(command))
    subprocess.run(command)
