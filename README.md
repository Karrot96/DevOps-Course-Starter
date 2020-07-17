# DevOps Apprenticeship: Project Exercise

## Getting started

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from a bash shell terminal:

### On macOS and Linux
```bash
$ source setup.sh
```
### On Windows (Using Git Bash)
```bash
$ source setup.sh --windows
```

## Trello

To set up trello add your token and key to a json file stored as `secrets/trello_secrets.json`. The file should be in the following format:

```Json
{
    "token": "YOUR_TOKEN",
    "key": "YOUR_KEY"
}
```

In the file `config/settings.py` you should set the constant `TRELLO_BOARD_ID` to your trello board ID.

The trello lists required in the project are:
- `Not Started`
- `Completed`

Once the setup script has completed and all packages have been installed, start the Flask app by running:
```bash
$ flask run
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
