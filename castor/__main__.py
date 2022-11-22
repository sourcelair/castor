from . import settings, utils

import asyncio
import aiodocker
import httpx
import logging
import sentry_sdk
import uuid


logging.basicConfig(
    format="[%(asctime)s] %(levelname)s %(module)s.%(funcName)s: %(message)s",
    level=logging.INFO,
)


async def forward_event(client: httpx.AsyncClient, target: str, event: dict):
    serialized_event = utils.serialize_event(event)
    response = await client.post(target, json=serialized_event)
    return response


async def consume_event(client: httpx.AsyncClient, event: dict):
    event_uuid = uuid.uuid4()
    logging.info(f"{event_uuid} - consuming")

    with sentry_sdk.start_transaction(op="topic.receive", name="docker_event"):
        try:
            response = await forward_event(client, settings.CASTOR_WEBHOOK_URL, event)
            logging.info(f"{event_uuid} - consumed ({response.status_code})")
        except Exception as e:
            logging.exception(f"{event_uuid} - failed ({e})")


async def loop():
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.CASTOR_ENVIRONMENT,
        release=settings.CASTOR_RELEASE,
        traces_sample_rate=0.01,
    )
    logging.info("Initialize Docker client")
    docker = aiodocker.Docker(url=settings.DOCKER_HOST)
    subscriber = docker.events.subscribe()

    async with httpx.AsyncClient() as client:
        logging.info("Start consuming Docker events")

        while event := await subscriber.get():
            await consume_event(client, event)


def main():
    try:
        logging.info("Starting loop")
        asyncio.run(loop())
    except KeyboardInterrupt:
        logging.info("Exiting. Received keyboard interupt (Ctrl + C).")


if __name__ == "__main__":
    main()
