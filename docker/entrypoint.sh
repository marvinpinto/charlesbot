#!/bin/bash

if [ -z "${CHARLESBOT_SETTINGS_FILE}" ]; then
  if [ ! -e "./development.ini" ]; then
    echo "Could not find environment variable CHARLESBOT_SETTINGS_FILE or ./development.ini"
    exit 1
  fi
fi

/src/env/bin/charlesbot
