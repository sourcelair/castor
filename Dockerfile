FROM ghcr.io/withlogicco/poetry:1.2.2

COPY pyproject.toml poetry.lock ./
RUN poetry install

COPY ./ ./

ARG CASTOR_RELEASE=norelease
ENV CASTOR_RELEASE=${CASTOR_RELEASE}
CMD [ "python", "-m", "castor" ]
