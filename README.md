Castor - Webhooks for Docker events
===================================

[![Build Status](https://travis-ci.org/sourcelair/castor.svg)](https://travis-ci.org/sourcelair/castor)

Castor monitors the Docker events of multiple Docker servers and
dispatches them via HTTP POST requests to the desired WebHooks.

## Example
You can tell Castor to monitor `unix:///var/run/docker.sock` (named as `localhost`) for Docker events and forward them to `https://www.example.com/hooks/docker`.

Now, when the following event gets captured by Castor:

```json
{
  "from": "image/with:tag",
  "id": "container-id",
  "status": "start",
  "time": 1423339459
}
```

it will be `POST`ed to `https://www.example.com/hooks/docker` with `application/json` content type and the following payload:

```json
{
  "docker_server": "localhost",
  "event": {
    "from": "image/with:tag",
    "id": "container-id",
    "status": "start",
    "time": 1423339459
  }
}
```

## Getting started

### Step 0: Host setup
Make sure you are running on a Ubuntu Linux machine with Docker 1.12 (or newer version) and Docker Compose installed.

(Docker for Mac should work as well)

### Step 1: Clone this repository
The first step you have to take is clone this repository and `cd` into it's root directory.

### Step 2: Create a `.env` file
Next, you will need to create a `.env` file to store configuration for your Castor installation in environment variable format (see how [`examples/.env.example`](examples/.env.example) is structured).

### Step 3: Configure database and Redis
Now you have to set the following environment variables in your `.env` file:

- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_DB`
- `REDIS_URL`

Use the same format with [`examples/.env.example`](examples/.env.example)

### Step 4: Configure authentication
Castor allows only members of a GitHub organization to access it's dashboard. For this reason you will need to [register a new OAuth application](https://github.com/settings/applications/new) in GitHub.

Then save your application's **Client ID**, **Client Secret** and **Organization name** in the following environment variables respectively in your `.env` file:

- `SOCIAL_AUTH_GITHUB_KEY`
- `SOCIAL_AUTH_GITHUB_SECRET`
- `SOCIAL_AUTH_GITHUB_ORG_NAME`

Use the same format with [`examples/.env.example`](examples/.env.example)

### Step 5: Bootstrap the environment
Run the following commands to:

1. Create the database and a new superuser
2. Install all front-end assets needed for the UI

```
docker-compose run --rm web ./bin/bootstrap
docker run --rm -v $(PWD):/mnt/castor -w /mnt/castor/castor/web/static/web node:8 npm install
```

### Step 6: Launch Castor!
Now all you have to do is launch castor by running:

```
docker-compose up
```

Now you can visit the Django admin panel, sign in with the superuser credentials that you created before and add Docker servers for monitoring and web hooks for dispatching events captured on those servers.

⚠️ **Warning:** This will run Castor in *development mode*, and it will bind `/var/run/docker.sock` into the container to bind easily to a local Docker daemon. It is suggested strongly to create your own `docker-compose.yaml` file for your production deployment of Castor.

## License
Castor is licensed under the MIT License. More info at [LICENSE](LICENSE) file.
