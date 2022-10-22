import subprocess
from datetime import timedelta
from os import getenv

from celery import Celery

from clipchimp.models import DownloadParameters


REDIS_HOST, REDIS_PORT = getenv("REDIS_HOST"), getenv("REDIS_PORT")

app = Celery(
    "tasks",
    backend=f"redis://{REDIS_HOST}:{REDIS_PORT}",
    broker=f"redis://{REDIS_HOST}:{REDIS_PORT}",
)


@app.task
def download_segment(url: str, start: timedelta, end: timedelta) -> None:
    params = DownloadParameters(clip_url=url, start=start, end=end)  # type: ignore
    command = f"ffmpeg -ss {start} -i {params.metadata['url']} -to {end} -c copy /downloads/{params.id}.mp4"
    print(f"Running the following command:\n{command}")
    subprocess.run(command.split(" "))
