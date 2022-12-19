# repograph

## Running

Running repograph consists of two components: the backend server and a user interface. 
Two user interfaces are provided: a Command-Line Interface (CLI) or a browser web app.

The backend must be run before using the CLI or accessing the web app.

### Running the backend

From the project root, run:

```shell
docker-compose build
docker-compose up
```

### Running the 


### Accessing the browser web app

The browser web app can be accessed at localhostL

## Development

### Pre-commit Hooks

Pre-commit hooks can be used to speed up development by running linting, tests, etc. when you commit. 

To install
```bash
pip3 install -r requirements-test.txt
pre-commit install
```