FROM node:8 as builder

COPY ./castor/web/static/web /usr/src/app
WORKDIR /usr/src/app
RUN npm install


FROM python:3.6

COPY . /usr/src/app
WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/usr/local

RUN pip install pipenv==9.0.1
RUN pipenv install

COPY --from=builder /usr/src/app /usr/src/app/castor/web/static/web

CMD ["python", "-u", "castor/manage.py", "runserver", "0.0.0.0:8000"]
