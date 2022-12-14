import re
from os import getenv
from pathlib import Path

from uvicorn.workers import UvicornWorker


ZERO_SECONDS = "0:00:00"
ALLOWED_ORIGIN = getenv("ALLOWED_ORIGIN")
DELTA_PATTERN = re.compile(r"(\d+:)?(\d+:)?\d+")
DOWNLOADS = Path(getenv("DOWNLOADS_DIRECTORY") or "/downloads/").absolute()
DEFAULT_ALLOWED_ORIGIN = (
    "https://package-version-ff3e16f0-7a8d-11ed-8737-951d64f4280f.sporocarp.dev"
)


class CustomWorker(UvicornWorker):
    """A custom worker to add any relevant extra headers."""

    CONFIG_KWARGS = {
        "headers": [
            ("access-control-allow-origin", ALLOWED_ORIGIN or DEFAULT_ALLOWED_ORIGIN),
        ],
    }
