FROM node:8 as builder

COPY ./castor/web/static/web /usr/src/app
WORKDIR /usr/src/app
RUN npm install


FROM python:3.6

ARG PIP_REQUIREMENTS_FILE=requirements.txt

COPY . /opt/castor
WORKDIR /opt/castor

RUN pip install -r $PIP_REQUIREMENTS_FILE

COPY --from=builder /usr/src/app /opt/castor/castor/web/static/web

CMD ["python", "-u", "castor/manage.py", "runserver", "0.0.0.0:8000"]
