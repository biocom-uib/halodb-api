# halodb-api

## Setting up for development

Starting from scratch, there are two options:

1. Start with an empty database

2. From existing data

### Option 1. Clean start

The following directories are mounted as volumes and must to belong to the user 1021 and group 1002. Create and `chown 1021:1002` them first if they don't exist:

- `volumes/mysql_data/`
- `volumes/tmp/`
- `volumes/uploads/`

In addition, the credentials JSON should be placed into `secrets/credentials.json`.

Therefore, to get the API running from scratch, the process is as follows:

```bash
cd halodb-api
mkdir -p volumes/{mysql_data,tmp,uploads} secrets
cp /path/to/credentials.json secrets/credentials.json
sudo chown -R 1021:1002 volumes
docker compose up --build
```

### Option 2. From existing data

Alternatively, copy existing data from a running instance. It should contain the following data:

- `volumes/mysql_data/...`
- `volumes/tmp/...`
- `volumes/uploads/...`
- `secrets/...`

A snapshot tarball can be directly extracted into this directory with:

```sh
sudo tar --same-owner -xvf halodb-snapshot.tar.gz
```

*Note:* Sudo is required in order to write these files as a different user (in
this case 1021:1002)

When using a snapshot from production for development, remember to update the values of any passwords in docker-compose.override.yml with the corresponding values from the secrets directory.

Summing up, to start an instance from an existing snapshot:

```bash
cd halodb-api
sudo tar --same-owner -xvf /path/to/halodb_snapshot.tar.gz
# remember to update docker-compose.override.yml with passwords from secrets
vim docker-compose.override.yml
docker compose up --build
```

## Differences between development and production

### Docker Compose

* Development is the default when running `docker compose ...`
* Production requires specifying overrides manually. A shortcut script `docker-compose-prod.sh` is included.
```bash
docker compose -f docker-compose.yml -f production.yml ...
# or
./docker-compose-prod.sh ...
```

Remember to append `--build` if there have been any changes to the Dockerfile
or copied files (see below).

Examples:

Run a development server and attach to see the logs
```bash
docker compose up --build -d && docker compose logs -f
```

Start a production server (detached)
```bash
./docker-compose-prod.sh up --build -d
```

### Dockerfile differences

The Dockerfile is structured as a multi-stage build, with a different stage for development (the base) and production (appropriately named production).

The main differences are:

* In production, `./api` is copied into the image, gunicorn runs with more workers/threads, and logs are written to `access.log` and `error.log` files, with default log level `INFO`.
* In development, hot-reload is enabled (the sources from `./api` are mounted instead), gunicorn runs with a single worker and 2 threads, logs are written to standard output and the default log level is `DEBUG`.

### Volumes and copied files overview

In development, the following directories are mounted:

* app: `./api:/opt/halodb-api/api:ro`
* app: `./volumes/tmp:/opt/halodb-api/tmp`
* app: `./volumes/uploads:/opt/halodb-api/uploads`
* mysql: `./sql:/docker-entrypoint-initdb.d:ro`
* mysql: `./volumes/mysql_data:/var/lib/mysql`

and MySQL credentials are defined with environment variables.

In production, `./api` is copied into the container instead, and the following are mounted

* app: `/data/shared/halodb/logs:/var/log/halodb-api`
* app: `/data/shared/halodb/tmp:/opt/halodb-api/tmp`
* app: `/data/shared/halodb/uploads:/opt/halodb-api/uploads`
* mysql: `./sql:/docker-entrypoint-initdb.d:ro`
* mysql: `/data/shared/halodb/mysql_data:/var/lib/mysql`

and MySQL credentials are defined via docker secrets.

To run a production server locally, remember to update these paths to your local directories (presumably from a snapshot).

