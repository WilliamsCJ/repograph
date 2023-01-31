# repograph

![Workflow](https://github.com/WilliamsCJ/repograph/actions/workflows/python.yaml/badge.svg)

Knowledge Graph extraction and semantic code search for Python repositories.

## Running

Running repograph consists of two components: the backend server and a user interface.
Two user interfaces are provided: a Command-Line Interface (CLI) or a browser web app.

The backend must be run before using the CLI or accessing the web app.

Several example notebooks are provided for testing and evaluation purposes. These notebooks handle
the running of the repograph CLI to generate knowledge graphs and provide an easily and repeatable
way to run [Cypher](https://neo4j.com/developer/cypher/) queries.

### Running the backend

From the project root, run:

```shell
docker-compose build
docker-compose up
```

_Note: It can take up to a minute for the frontend and backend containers to start as they have to
wait for the Neo4J container._

#### Accessing the Neo4J database

The backend runs a Neo4J database in a container. The database itself can be accessed at
`neo4j://localhost:7687`. The Neo4J admin console can be accessed at `http://localhost:7474`.

The required credentials are:

- Username: `neo4j`
- Password: `s3cr3t`
- Database: `neo4j` (see below about Community Edition)

### Running the CLI

This requires that `inspect4py` has already been run on a repository, and its output
directory accessible at `<PATH_TO_INSPECT4PY_OUTPUT_DIR>`

From the project root, run:

```shell
cd backend
python3 -m repograph.cli --uri neo4j://localhost:7687 --username neo4j --password s3cr3t --database neo4j --input <PATH_TO_INSPECT4PY_OUTPUT_DIR>
```

Several other command line options, such as `--prune`, are also available. To see these options,
and descriptions of their functionality, run:

```shell
python3 -m repograph.cli --help
```

_Note: If using the Neo4J instance created by running the backend (see above), the only
available option for `--database` is `neo4j`. This is due to limitations in the
[Community Edition license](https://neo4j.com/licensing/)._

### Accessing the browser web app

The browser web app can be accessed at `http://localhost:8080`

## Demonstration

See `demo/README.md`.

## Development

Tips for contributing to/developing repograph.

### Pre-commit Hooks

Pre-commit hooks can be used to speed up development by running linting, tests, etc. when you commit.

To install:

```bash
pip3 install -r requirements-test.txt
pre-commit install
```
