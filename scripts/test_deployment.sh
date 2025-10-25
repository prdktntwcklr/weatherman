#!/usr/bin/env bash

URL="https://weatherman.onrender.com/"

HTTP_CODE=$(curl -sSL -w "%{http_code}" -o /tmp/response_body "$URL")

if [ "$HTTP_CODE" -eq 200 ]; then
  if ! grep -q "Temperature" /tmp/response_body; then
    echo "Site returned 200 but content check failed at $URL."
    exit 1
  fi
else
  echo "Deployment check failed: Site did not return 200 (got $HTTP_CODE)."
  exit 1
fi

echo "Deployment check passed: Site is live and accessible at $URL."
exit 0
