#!/usr/bin/env sh

# Ensure that instances always contain the latest yt-dlp
pip install git+https://github.com/yt-dlp/yt-dlp.git

exec "$@"
