#!/usr/bin/env bash
export DJANGO_SETTINGS_MODULE="tellog.settings.local"

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
${DIR}/server/manage.py runserver 0.0.0.0:8080
