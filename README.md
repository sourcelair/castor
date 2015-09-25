Castor
======

Castor listens to Docker events and invokes a POST request to all given hooks for every event.

## Inside Castor

Castor is written in Python and consists of **2 services**

- the Castor server — a simple Python program that listens to events from a single Docker server and dispatches them to the task queue
- the Castor task queue — a Celery app that dispatches a Docker event as payload to the registered hooks

### Settings

Castor can be customized with a simple file. The settings of Castor are stored in a file called `settings.json` in the `castor` directory.

#### Example settings
```json
{
    "hooks": [
        "http://host:80/hooks/docker/events",
        "https://another-host:443/docker/event"
    ],
    "docker": {
        "base_url": "unix://var/run/docker.sock",
        "version": "1.19"
    }
}
```

## Deploying Castor

Deploying Castor is extremely easy. Castor can be deployed with two helper scripts, while we are working on deploying Castor with Docker as well.

### Deploying with the helper scripts

The only thing needed to deploy castor is start its services with a single command each.

#### Castor server
```
./script/server
```

#### Castor task queue
```
./scripts/celery-start.sh
```


### Deploying with Docker
Deploying Castor with Docker is Work In Progress. Since it needs to listen to Docker events, we have to make sure that a Docker container will have access to a Docker server, without security compromises.

## License
Castor is licensed under the MIT License. More info at [LICENSE](LICENSE) file.
