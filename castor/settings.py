import sec
from . import version


_POETRY_VERSION = version.get_poetry_version()

DOCKER_HOST = sec.load("docker_host", "unix:///var/run/docker.sock")
SENTRY_DSN = sec.load("sentry_dsn")
CASTOR_ENVIRONMENT = sec.load("castor_environment")
CASTOR_RELEASE = sec.load("castor_release", _POETRY_VERSION)
CASTOR_WEBHOOK_URL = sec.load("castor_webhook_url")
