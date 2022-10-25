import hashlib
import logging
import re
from datetime import timedelta

import yt_dlp
from pydantic.dataclasses import dataclass

from clipchimp import logic


CLIP_URL_PATTERN = re.compile(r"/clip/([^/?]*)/?")

logger = logging.getLogger("gunicorn.error")


@dataclass
class DownloadParameters:
    url: str = ""
    start: timedelta = timedelta()
    end: timedelta = timedelta()
    download_from: str = ""
    post_process: bool = True

    def __post_init_post_parse__(self) -> None:
        """
        Ensure that parameters are valid and normalise the URL before extracting timestamps.
        """
        if not self.post_process:
            # Allow us to instantiate without processing
            return
        url = self.url
        try:
            metadata = logic.get_ytdl_metadata(url)
        except yt_dlp.utils.DownloadError:
            return
        self.download_from = metadata["url"]

        # If a timestamped video link was given, use that start time
        if not self.start:
            self.start = timedelta(seconds=metadata.get("start_time", 0))
        # Default the end timestamp to the end of the video
        if not self.end:
            self.end = timedelta(seconds=metadata.get("duration", 0))
        if not (match := CLIP_URL_PATTERN.search(url)):
            return

    @property
    def id(self) -> str:
        """An identifier for this particular video segment."""
        return hashlib.md5(f"{self.url}{self.start}{self.end}".encode()).hexdigest()

    def json(self) -> dict:
        end, *_ = str(self.end).partition(".")
        start, *_ = str(self.start).partition(".")
        return dict(url=self.url, start=start, end=end)
