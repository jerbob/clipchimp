import re
from os import getenv
from pathlib import Path

from uvicorn.workers import UvicornWorker


ZERO_SECONDS = "0:00:00"
DEFAULT_ALLOWED_ORIGIN = "*"
ALLOWED_ORIGIN = getenv("ALLOWED_ORIGIN")
DELTA_PATTERN = re.compile(r"(\d+:)?(\d+:)?\d+")
DOWNLOADS = Path(getenv("DOWNLOADS_DIRECTORY") or "/downloads/").absolute()


class CustomWorker(UvicornWorker):
    """A custom worker to add any relevant extra headers."""

    CONFIG_KWARGS = {
        "headers": [
            ("access-control-allow-origin", ALLOWED_ORIGIN or DEFAULT_ALLOWED_ORIGIN),
        ],
    }
