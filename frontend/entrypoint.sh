#!/usr/bin/env sh

echo "export default { secretKey: '$TRUFFLE_API_KEY' }" > truffle.secret.mjs

exec "$@"
