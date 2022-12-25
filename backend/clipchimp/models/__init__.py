import hashlib
import logging
import re
from datetime import timedelta
from typing import Dict, Optional

import yt_dlp
from pydantic import validate_arguments, validate_model, BaseModel, Field

from clipchimp import logic


CLIP_URL_PATTERN = re.compile(r"/clip/([^/?]*)/?")

logger = logging.getLogger("gunicorn.error")


class DownloadParameters(BaseModel):
    """Model representing form fields for a video download."""

    url: str = ""
    start: timedelta = timedelta()
    end: timedelta = timedelta()
    download_from: str = ""
    post_process: bool = True
    errors: dict = Field(default_factory=dict)

    def __init__(self, **data) -> None:
        """Catch validation errors and store them."""
        errors: Dict[str, str] = {}
        if exception := validate_model(DownloadParameters, data)[2]:
            for error in exception.errors():
                field = str(error["loc"][0])
                errors[field] = error["msg"].capitalize()
            data.clear()
        super().__init__(**data, errors=errors)

        if not self.post_process:
            # Allow us to instantiate without processing
            return

        try:
            metadata = logic.get_ytdl_metadata(self.url)
        except yt_dlp.utils.DownloadError:
            self.errors["url"] = "Invalid video url"
            return

        self.download_from = metadata["url"]
        # If a timestamped video link was given, use that start time
        if not self.start:
            self.start = timedelta(seconds=metadata.get("start_time", 0))
        # Default the end timestamp to the end of the video
        if not self.end:
            self.end = timedelta(seconds=metadata.get("duration", 0))

    @property
    def id(self) -> str:
        """An identifier for this particular video segment."""
        return hashlib.md5(f"{self.url}{self.start}{self.end}".encode()).hexdigest()

    def json(self) -> dict:
        """Construct a JSON object for API responses."""
        response = {}
        for field in ("url", "start", "end"):
            message = self.errors.get(field, "")
            response[field] = dict(
                error=bool(message),
                message=message,
                value=str(getattr(self, field)),
            )
        return response

    @validate_arguments
    def get_progress(self, newest_time: Optional[timedelta]) -> Optional[float]:
        if newest_time is None:
            return

        progress = newest_time / self.end
        return progress if progress <= 1 else 1.0
