import os
import re
import time
from datetime import timedelta
from subprocess import Popen, PIPE

from celery import Celery, Task

from clipchimp.models import DownloadParameters


PROGRESS_PATTERN = re.compile(r"time=(\d\d:\d\d:\d\d.\d\d)")
CLIP_METADATA_PATTERN = r'\{"postId":"%s","startTimeMs":"(.*)","endTimeMs":"(.*)"\}'
REDIS_HOST, REDIS_PORT = os.getenv("REDIS_HOST"), os.getenv("REDIS_PORT")

app = Celery(
    "tasks",
    backend=f"redis://{REDIS_HOST}:{REDIS_PORT}",
    broker=f"redis://{REDIS_HOST}:{REDIS_PORT}",
)


@app.task(bind=True)
def download_segment(self: Task, url: str, start: timedelta, end: timedelta) -> None:
    download = DownloadParameters(url=url, start=start, end=end, post_process=False)
    process = Popen(
        [
            "yt-dlp",
            "--download-sections",
            f"*{start}-{end}",
            url,
            "-o",
            f"/downloads/{download.id}",
        ],
        stderr=PIPE,
        text=True,
    )
    for line in process.stderr:
        if match := PROGRESS_PATTERN.search(line):
            progress = download.get_progress(match.group(1))
            self.update_state(state="STARTED", meta={"progress": progress})
