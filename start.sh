#!/usr/bin/env bash

NEXT_WAIT_TIME=0
until python manage.py migrate || [[ ${NEXT_WAIT_TIME} -eq 20 ]]; do
   sleep $(( NEXT_WAIT_TIME++ ))
done

python manage.py runserver 0.0.0.0:8000
