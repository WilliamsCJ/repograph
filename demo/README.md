# Demonstration

To begin, clone the demo repositories by running the following from this directory:

```shell
./clone.sh
```

## Single Repository Example

To create a graph with a single repository, run:

```shell
cd ../backend
python -m repograph.cli --config default_config.yaml --name pyLODE --input ../demo/pyLODE --prune
```

You can then execute the Cypher Queries

## Multi-Repository Example

_NOTE: This step relies on having previously run the above example_

**WARNING: This may take some time!**

To create a graph with multiple repositories, run:

```shell
python -m repograph.cli --config default_config.yaml  --prune --input ../demo/fastapi --input ../demo/pygorithm --input ../demo/starlette --input ../demo/flake8 --input ../demo/pyLODE --prune
```

## Cypher Queries

The following Cypher queries can be executed by copy and pasting them into the
Neo4j Browser. The Browser can be accessed at `http://localhost:7474/browser`

### Select the requirements of a given repo

**_NOTE: Not currently working due to issues with inspect4py_**

`MATCH (r)-[r:Requires]->(p) RETURN p, r`

### Select the readmes of a given repo

```
MATCH (n:README) RETURN n.path as `README File`, n.content as `Contents`
```

### Select the metadata of a given repo

```
MATCH (r:Repository) RETURN properties(r) as `Repository Metadata`
```

### Select the license of a given repo

```
MATCH (n:License) RETURN n.license_type as `License`, n.confidence as `Confidence`, n.text as `Content`
```

### Select the docstring (long and short) of a given repo

```
MATCH (n:Docstring)-[r:Documents]-(f:Function) WHERE n.short_description IS NOT NULL RETURN f.name as `Function Name`, n.short_description as `Docstring Summary`, n.long_description as `Doctring Body`
```

### Select the summarizations of functions of a given repo

`MATCH (n:Docstring)-[r:Documents]-(f) WHERE n.summarization IS NOT NULL RETURN n, f, r LIMIT 5`

### Select the filenames of a given demo

```
MATCH (m:Module) RETURN m.name + '.' + m.extension as `Filename`
```

### Select the function and class names of a given demo

```
MATCH (n) WHERE n:Class OR n:Function RETURN n.name as `Name`, labels(n) as `Type`
```

### Select the source code of a given demo

```
MATCH (f:Function) WHERE f.source_code IS NOT NULL RETURN f.name, f.source_code
```

### Select the call graph of a given demo
