#! /usr/bin/env sh

cd castor
celery -A tasks worker -l INFO
