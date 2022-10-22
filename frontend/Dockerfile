FROM docker.io/library/node:18.11.0

RUN set -ex \
  && apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/* \
  && yarn global add @trufflehq/cli

COPY . /app/src
WORKDIR /app/src/

CMD "truffle-cli" "dev"
