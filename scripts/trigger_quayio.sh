#!/bin/bash

if [ -z "${BEARER_TOKEN}" ]; then
  echo "BEARER_TOKEN environment variable not found"
  exit 1
fi

if [ -z "${QUAY_TRIGGER_ID}" ]; then
  echo "QUAY_TRIGGER_ID environment variable not found"
  exit 1
fi

# # Note that one could retrieve the $QUAY_TRIGGER_ID by using something like:
# curl \
#   -X GET \
#   -H "Content-Type: application/json" \
#   -H "Authorization: Bearer ${BEARER_TOKEN}" \
#   -s \
#   https://quay.io/api/v1/repository/marvin/charlesbot/trigger/

# Trigger a quay.io automated build of charlesbot
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${BEARER_TOKEN}" \
  --data '{"branch_name": "master"}' \
  -s \
  https://quay.io/api/v1/repository/marvin/charlesbot/trigger/${QUAY_TRIGGER_ID}/start
