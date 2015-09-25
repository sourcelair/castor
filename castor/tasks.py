from redis import Redis
from rq.decorators import job
import settings


redis_conn = Redis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
)


@job('castor', connection=redis_conn)
def dispatch_event(event):
    print event
