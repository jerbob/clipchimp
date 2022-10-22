import contextlib
import functools
import json
import re

import youtube_dl
from requests_html import AsyncHTMLSession


CACHE_LIMIT: int = 100
YTDL_OPTIONS = {
    "format": "bestvideo[ext=mp4]/best[ext=mp4]/best",
    "noplaylist": True,
    "quiet": True,
    "prefer_ffmpeg": True,
}
CLIP_METADATA_PATTERN = r'\{"postId":"%s","startTimeMs":"(.*)","endTimeMs":"(.*)"\}'


@functools.lru_cache(CACHE_LIMIT)
def is_supported(url: str) -> bool:
    """Check whether the provided URL can be downloaded from."""
    for extractor in youtube_dl.extractor.gen_extractors():
        if extractor.suitable(url) and extractor.IE_NAME != "generic":
            return True
    return False


@functools.lru_cache(CACHE_LIMIT)
def get_ytdl_metadata(url: str) -> dict:
    """Get all metadata from youtube-dl about the provided URL."""
    with youtube_dl.YoutubeDL(YTDL_OPTIONS) as ytdl:
        return ytdl.extract_info(url, download=False) or {}


async def get_clip_config(
    session: AsyncHTMLSession, clip_url: str, clip_id: str
) -> dict:
    """Get clip config metadata from the given clip page."""
    response = session.get(clip_url)
    page = response.content.decode()

    if match := re.search(CLIP_METADATA_PATTERN % clip_id, page):
        with contextlib.suppress(json.JSONDecodeError):
            clip_metadata = json.loads(match.group(0))

    await response.html.arender()
    clip_metadata = await response.html.arender(
        script="""
            () => {
                document.querySelector("button").click();
                return ytInitialPlayerResponse.clipConfig
            }
        """,
        send_cookies_session=True,
    )
    return clip_metadata
