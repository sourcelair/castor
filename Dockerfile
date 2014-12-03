# Work in progress
FROM python:2.7-onbuild
MAINTAINER Paris Kasidiaris <pariskasidiaris@gmail.com>

ADD . /var/lib/castor
RUN cp /var/lib/castor/examples/settings.json /var/lib/castor/castor/settings.json
RUN mkdir /var/lib/castor/castor/.data
RUN chown -R www-data:www-data /var/lib/castor
RUN chmod a+rw /var/lib/castor/castor/.data

VOLUME ["//var/lib/castor/castor/.data"]

WORKDIR /var/lib/castor

USER www-data
