# DevOps Apprenticeship: Project Exercise

## Getting started

The project uses a poetry to isolate package dependencies. To get poetry running install poetry for python and then run:

```bash
poetry install
```

## MongoDB

To set up MongoDB add your username, password, mongo url and default database to the relevent environment variables.

Once the setup script has completed and all packages have been installed, start the Flask app by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Testing

### Unit Tests

Unit tests can be run with the following command

```bash
poetry run pytest tests
```

### Integration Tests

Integration Tests can be run with the following command

```bash
poetry run pytest integration_tests
```

### End-2-End Tests

Make sure you have geckodriver installed and in the path.
Tests can then be run with the following command

```bash
poetry run pytest e2e_tests
```

## Vagrant

To run the app file in vagrant run:
```bash
vagrant up
```

then navigate to http://localhost:5000

## Docker
To run production version of docker

```bash
docker build --target production --tag todo-app:prod .
docker run -d --env-file {Location of env file} -p 8003:8003 todo-app:prod
```

To run development version in docker on linux using port 80.

```bash
run_dev.sh
```

on windows:

```bash
run_dev.bat
```
