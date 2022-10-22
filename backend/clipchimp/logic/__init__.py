import contextlib
import functools
import json
import logging
import os
import re

import httpx
import redis
import yt_dlp
from redis_lru import RedisLRU


client = redis.StrictRedis(
    host=os.getenv("REDIS_HOST", ""),
    port=int(os.getenv("REDIS_PORT", 0)),
)
cache = RedisLRU(client)
session = httpx.Client()

CACHE_LIMIT: int = 100
YTDL_OPTIONS = {
    "format": "bestvideo[ext=mp4]/best[ext=mp4]/best",
    "noplaylist": True,
    "quiet": True,
    "prefer_ffmpeg": True,
}
CLIP_METADATA_PATTERN = r'\{"postId":"%s","startTimeMs":"(.*?)","endTimeMs":"(.*?)"\}'

logger = logging.getLogger("gunicorn.error")


@cache
def is_supported(url: str) -> bool:
    """Check whether the provided URL can be downloaded from."""
    for extractor in yt_dlp.extractor.gen_extractors():
        if extractor.suitable(url) and extractor.IE_NAME != "generic":
            return True
    return False


@cache
def get_ytdl_metadata(url: str) -> dict:
    """Get all metadata from youtube-dl about the provided URL."""
    with yt_dlp.YoutubeDL(YTDL_OPTIONS) as ytdl:
        return ytdl.extract_info(url, download=False) or {}


def get_clip_config(clip_url: str, clip_id: str) -> dict:
    """Get clip config metadata from the given clip page."""
    clip_metadata = {}

    response = session.get(clip_url, cookies={})
    if consent_request := response.next_request:
        del consent_request.headers["cookie"]
        response = session.send(consent_request, follow_redirects=True)

    page = response.content.decode()
    if match := re.search(CLIP_METADATA_PATTERN % clip_id, page):
        with contextlib.suppress(json.JSONDecodeError):
            clip_metadata = json.loads(match.group(0))
    return clip_metadata
