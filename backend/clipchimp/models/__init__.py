import asyncio
import hashlib
import json
import logging
import re
from concurrent import futures
from dataclasses import InitVar, field
from datetime import timedelta

import nest_asyncio
from requests_html import AsyncHTMLSession
from pydantic.dataclasses import dataclass

from clipchimp import logic


CLIP_URL_PATTERN = re.compile(r"/clip/(.*)/?")

nest_asyncio.apply()

session = AsyncHTMLSession()
logger = logging.getLogger("gunicorn.error")

event_loop = asyncio.get_event_loop()


@dataclass
class DownloadParameters:
    clip_url: InitVar[str]

    start: timedelta = timedelta()
    end: timedelta = timedelta()
    url: str = ""

    errors: list = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

    def __post_init_post_parse__(self, clip_url: str) -> None:
        """Ensure that parameters are valid before extracting start and end."""
        self.url = clip_url
        if not logic.is_supported(clip_url):
            self.errors.append("This URL is not supported.")
            return

        metadata = self.metadata = logic.get_ytdl_metadata(clip_url)
        # If a timestamped video link was given, use that start time
        self.start = timedelta(seconds=metadata.get("start_time", 0))
        if metadata.get("extractor") == "youtube":
            self.url = f"https://youtu.be/{metadata['id']}"
        if not self.end:
            self.end = timedelta(seconds=metadata.get("duration", 0))
        if not (match := CLIP_URL_PATTERN.search(clip_url)):
            return

        # Extra processing for youtube clips
        coroutine = logic.get_clip_config(
            session=session, clip_url=clip_url, clip_id=match.group(1)
        )
        clip_metadata = event_loop.run_until_complete(coroutine)
        self.start = timedelta(milliseconds=clip_metadata.get("startTimeMs", 0))
        self.end = timedelta(milliseconds=clip_metadata.get("endTimeMs", 0))

    @property
    def id(self) -> str:
        """An identifier for this particular video segment."""
        return hashlib.md5(f"{self.url}{self.start}{self.end}".encode()).hexdigest()

    def json(self) -> dict:
        return dict(url=self.url, start=str(self.start), end=str(self.end))
