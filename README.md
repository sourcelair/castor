# Castor

Stream Docker Engine events as webhooks to an HTTP(S) endpoint.

## Getting started

To get started with Castor, simply pull and run the latest versioned image from the GitHub Container Registry

```
ghcr.io/sourcelair/castor:2.0.0
```

## Configuration

Castor is be configured via Docker Secrets preferably or environment variables:

- `DOCKER_HOST` (**required**): The URL to monitor for Docker Engine events (e.g. `http://docker:2375`)
- `CASTOR_WEBHOOK_URL` (**required**): The URL to stream Docker Engine events (example: `http://httpbin/anything`)
- `CASTOR_ENVIRONMENT`: The environment where Castor currently runs (example: `production`)
- `CASTOR_RELEASE`: The current version running (default: the version in `pyproject.toml`)
- `SENTRY_DSN`: The DSN of a Sentry project to report errors.

## Development

To work on Castor, you will first need to:

- Install Docker Desktop
- Clone this repository

Then, you can use Docker Compose to launch Castor and stream events from your local Docker Engine to local `httpbin`:

```console
docker compose up
```

This repository has also been set up to work with [development containers](https://containers.dev/).

## License
Castor is [MIT licensed](LICENSE).
