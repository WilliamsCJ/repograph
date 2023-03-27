# RepoGraph

[![Workflow](https://github.com/WilliamsCJ/repograph/actions/workflows/python.yaml/badge.svg)](https://github.com/WilliamsCJ/repograph/actions)
[![codecov](https://codecov.io/gh/WilliamsCJ/repograph/branch/main/graph/badge.svg?token=1WYUIBCMQF)](https://codecov.io/gh/WilliamsCJ/repograph)

[![Share to Community](https://huggingface.co/datasets/huggingface/badges/raw/main/powered-by-huggingface-light.svg)](https://huggingface.co/cjwilliams/codet5-base-python-sum)

Knowledge Graphs and Semantic Search for Python Repositories using Neo4j.

## Requirements

This project requires Python 3.10 (preferably 3.10.8). This is due to issues related to the
`inspect4py` library and `pigar`.

## Running

Running repograph consists of two components: the backend server and a user interface.
Two user interfaces are provided: a Command-Line Interface (CLI) or a browser web app.

The backend must be run before using the CLI or accessing the web app.

Several example notebooks are provided for testing and evaluation purposes. These notebooks handle
the running of the repograph CLI to generate knowledge graphs and provide an easily and repeatable
way to run [Cypher](https://neo4j.com/developer/cypher/) queries.

### Running the application

From the project root, run:

```shell
docker-compose build
docker-compose up
```

_Note: It can take up to a minute for the frontend and backend containers to start as they have to
wait for the Neo4J container._

### Alternative Method

If you are not able to use Docker Compose (i.e. on the lab machines), the following Podman commands can be run to start the application:

```shell
podman build -t localhost/repograph-backend:latest -f backend/Dockerfile backend

podman build -t localhost/repograph-frontend:latest -f frontend/Dockerfile frontend

podman network create repograph-network

podman run -d --network=repograph-network -p 7474:7474 -p 7687:7687 --name neo4j --network-alias repograph-database -e NEO4J_AUTH='neo4j/s3cr3t' -e NEO4J_dbms_security_auth__minimum__password__length=1 -e NEO4J_ACCEPT_LICENSE_AGREEMENT=yes neo4j:5.4.0-enterprise

podman run -d --network=repograph-network -p 3000:3000 --name repograph-backend --network-alias repograph-backend -v `pwd`/.sqlite:/code/sqlite -v `pwd`/.cache:/root/.cache -v `pwd`/.nltk:/nltk_data repograph-backend:latest

podman run -d --network=repograph-network -p 8080:8080 --name repograph-frontend --network-alias repograph-frontend repograph-frontend:latest
```

### Accessing the browser web app

The browser web app can be accessed at `http://localhost:8080`

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
python3 -m repograph.cli --uri neo4j://localhost:7687 --username neo4j --password s3cr3t --database neo4j --input <PATH_TO_REPOSITORY>
```

Multiple repositories can be passed into the CLI at the same time, as such:

```shell
cd backend
python3 -m repograph.cli --uri neo4j://localhost:7687 --username neo4j --password s3cr3t --database neo4j --input <PATH_TO_REPOSITORY> --input <PATH_TO_ANOTHER_REPOSITORY>
```

Several other command line options, such as `--prune`, are also available. To see these options,
and descriptions of their functionality, run:

```shell
python3 -m repograph.cli --help
```

\_Note: If using the Neo4J instance created by running the backend (see above), the only
available option for `--database` is `neo4j`. This is due to limitations in the
[Community Edition license](https://neo4j.com/licensing/).

## Demonstration

See `demo/README.md`.

## Development

Tips for contributing to RepoGraph.

### Testing

Before testing, please clone the demo directories. See `demo/README.md`

From the project root, run:

```shell
cd backend
python -m unittest
```

#### Coverage

![Coverage Tree](https://codecov.io/gh/WilliamsCJ/repograph/branch/main/graphs/tree.svg?token=1WYUIBCMQF)
![Coverage Sunburst](https://codecov.io/gh/WilliamsCJ/repograph/branch/main/graphs/sunburst.svg?token=1WYUIBCMQF)
