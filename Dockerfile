# Work in progress
FROM python:2.7-onbuild
MAINTAINER Paris Kasidiaris <pariskasidiaris@gmail.com>

# Copy default settings
RUN cp /usr/src/app/examples/settings.json /usr/src/app/castor/settings.json

WORKDIR /usr/src/app
