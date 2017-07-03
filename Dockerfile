FROM python:3.6

ARG PIP_REQUIREMENTS_FILE=requirements.txt

COPY . /opt/castor
WORKDIR /opt/castor

RUN pip install -r $PIP_REQUIREMENTS_FILE

CMD ["python", "-u", "castor/manage.py", "runserver", "0.0.0.0:8000"]
