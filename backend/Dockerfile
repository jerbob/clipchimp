FROM docker.io/library/python:3.10-slim

ENV PYTHONUNBUFFERED=1 \
  PIP_NO_CACHE_DIR=off \
  PYTHONPYCACHEPREFIX=/tmp \
  PATH=/root/.local/bin:${PATH}

RUN set -ex \
  && apt-get update \
  && apt-get install -y curl ffmpeg git \
  && rm -rf /var/lib/apt/lists/* \
  && curl -sSL 'https://install.python-poetry.org' | python \
  && poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml /app/
WORKDIR /app/src

RUN poetry install --no-root --no-interaction --no-dev

COPY . /app/src/

ENTRYPOINT [ "/app/src/entrypoint.sh" ]

CMD "gunicorn" \
  "--reload" \
  "--chdir=/app/src/" \
  "--bind=0.0.0.0:8000" \
  "--worker-class=clipchimp.config.CustomWorker" \
  "--workers=12" \
  "clipchimp:app"
