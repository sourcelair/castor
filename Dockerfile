# Work in progress
FROM python:2.7-onbuild
MAINTAINER Paris Kasidiaris <pariskasidiaris@gmail.com>

# Copy default settings
RUN cp /usr/src/app/examples/settings.json /usr/src/app/castor/settings.json

# Create data directory
RUN mkdir /usr/src/app/castor/.data

#Set proper ownership and rights to root directory
RUN chown -R www-data:www-data /usr/src/app/
RUN chmod a+rw /usr/src/app/castor/.data

VOLUME ["/usr/src/app/castor/.data"]

WORKDIR /usr/src/app

USER www-data
