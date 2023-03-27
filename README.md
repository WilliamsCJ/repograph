# RepoGraph

[![Workflow](https://github.com/WilliamsCJ/repograph/actions/workflows/python.yaml/badge.svg)](https://github.com/WilliamsCJ/repograph/actions)
[![codecov](https://codecov.io/gh/WilliamsCJ/repograph/branch/main/graph/badge.svg?token=1WYUIBCMQF)](https://codecov.io/gh/WilliamsCJ/repograph)

[![Share to Community](https://huggingface.co/datasets/huggingface/badges/raw/main/powered-by-huggingface-light.svg)](https://huggingface.co/cjwilliams/codet5-base-python-sum)

Knowledge Graphs and Semantic Search for Python Repositories using Neo4j.

## Structure

Running repograph consists of three components: the Neo4j database, the backend server and a user interface.
Two user interfaces are provided: a Command-Line Interface (CLI) or a browser web app.

## Requirements

This project requires Python 3.10 (preferably 3.10.8). This is due to issues related to the
`inspect4py` library and `pigar`.

## Running the Application

The backend must be run before using the CLI or accessing the web app.

### Main Method

From the project root, run:

```shell
docker-compose build
docker-compose up
```

_Note: It can take up to a minute for the frontend and backend containers to start as they have to
wait for the Neo4J container._

### Alternative Method

If you can't use Docker Compose (e.g. lab machines), run the following commands (in order) from the project root:

```shell
podman build -t localhost/repograph-backend:latest -f backend/Dockerfile backend

podman build -t localhost/repograph-frontend:latest -f frontend/Dockerfile frontend

podman network create repograph-network

mkdir .sqlite .cache .nltk

podman run -d --network=repograph-network -p 7474:7474 -p 7687:7687 --name neo4j --network-alias repograph-database -e NEO4J_AUTH='neo4j/s3cr3t' -e NEO4J_dbms_security_auth__minimum__password__length=1 -e NEO4J_ACCEPT_LICENSE_AGREEMENT=yes neo4j:5.4.0-enterprise

podman run -d --network=repograph-network -p 3000:3000 --name repograph-backend --network-alias repograph-backend -v `pwd`/.sqlite:/code/sqlite -v `pwd`/.cache:/root/.cache -v `pwd`/.nltk:/nltk_data repograph-backend:latest

podman run -d --network=repograph-network -p 8080:8080 --name repograph-frontend --network-alias repograph-frontend repograph-frontend:latest
```

Please allow a minute or two (depending on your internet connection) for the backend to download the required models. Whilst this is happening, the frontend/web app may show a `500 Error`. Refreshing the page once enough time has been allowed will rectify this.

## Accessing the Application

The browser web app can be accessed at `http://localhost:8080`

### Accessing the Neo4J database

The backend runs a Neo4J database in a container. The database itself can be accessed at
`neo4j://localhost:7687`. The Neo4J admin console can be accessed at `http://localhost:7474`.

The required credentials are:

- Username: `neo4j`
- Password: `s3cr3t`

### Using the CLI

The CLI is intended for debugging, and should not be used as the primary interface.

From the project root, run:

```shell
cd backend
python3 -m repograph.cli --config <PATH_TO_CONFIG> --name <GRAPH_NAME> --description <GRAPH_DESCRIPTION> --input <PATH_TO_REPOSITORY>
```

Multiple repositories can be passed into the CLI at the same time, as such:

```shell
cd backend
python3 -m repograph.cli --config <PATH_TO_CONFIG> --name <GRAPH_NAME> --description <GRAPH_DESCRIPTION> --input <PATH_TO_REPOSITORY> --input <PATH_TO_ANOTHER_REPOSITORY>
```

Several other command line options, such as `--prune`, are also available. To see these options,
and descriptions of their functionality, run:

```shell
python3 -m repograph.cli --help
```

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
