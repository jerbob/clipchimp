import re
from os import getenv
from pathlib import Path
from fastapi import Response

from starlette.datastructures import Headers
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles, NotModifiedResponse

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


class DownloadsMount(StaticFiles):
    """A custom static files mount adding appropriate extra headers."""

    def __init__(self) -> None:
        return super().__init__(directory=DOWNLOADS)

    def file_response(
        self,
        full_path,
        stat_result,
        scope,
        status_code=200,
    ) -> Response:
        method = scope["method"]
        request_headers = Headers(scope=scope)
        file_extension = str(full_path).partition(".")[2]

        response = FileResponse(
            full_path,
            status_code=status_code,
            stat_result=stat_result,
            method=method,
            filename=f"clip.{file_extension}",
        )
        if self.is_not_modified(response.headers, request_headers):
            return NotModifiedResponse(response.headers)
        return response
