# Demonstration

Demonstration. Several specific directories are included.Ω

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

**WARNING: This may take some time!**

To create a graph with multiple repositories, run:

```shell
python -m repograph.cli --config default_config.yaml  --prune --input ../demo/fastapi --input ../demo/pygorithm --input ../demo/starlette --input ../demo/flake8 --input ../demo/pyLODE --prune
```

## Cypher Queries

The following Cypher queries can be executed by copy and pasting them into the
Neo4j Browser. The Browser can be accessed at `http://localhost:7474/browser`

They allow for filtering by the particular repository.

### Select the requirements of a given repo

Return all requirements defined by a given repository.

```
MATCH (r:Repository)-[s:Requires]->(d) WHERE r.name = 'REPO NAME' RETURN r.name as `Repository`, d.name as `Dependency`, s.version as `Version`
MATCH (r:Repository)-[s:Requires]->(d) WHERE r.name =~ '<REPO>' RETURN r.name as `Repository`, d.name as `Dependency`, s.specifications as `Specifications`

```

Query options for repository (`<REPO>`):

- Repository name, e.g. `pyLODE`
- Wildcard, e.g. `.*`
- Multiple repositories, e.g. `pyLODE|fastapi`

### Select the readmes of a given repo

Return the text of all README files contained within a repository.

```
MATCH (n:README)-[:Contains*1..]-(r:Repository) WHERE r.name =~ '<REPO>' RETURN r.name as `Repository`, n.path as `File`, n.content as `Contents`
```

Query options for repository (`<REPO>`):

- Repository name, e.g. `pyLODE`
- Wildcard, e.g. `.*`
- Multiple repositories, e.g. `pyLODE|fastapi`

### Select the metadata of a given repo TODO:

Select the metadata of a particular repository, or all.

```
MATCH (r:Repository) WHERE r.name =~ '<REPO>' RETURN r.name as `Repository`, properties(r) as `Repository Metadata`
```

Query options for repository (`<REPO>`):

- Repository name, e.g. `pyLODE`
- Wildcard, e.g. `.*`
- Multiple repositories, e.g. `pyLODE|fastapi`

### Select the license of a given repo

Selects the possible licenses of a given repository.

```
MATCH (n:License)-[]-(r:Repository) WHERE r.name =~ '<REPO>' RETURN r.name as `Repository`, n.license_type as `License`,
n.confidence as `Confidence`, n.text as `Content`
```

Query options for repository (`<REPO>`):

- Repository name, e.g. `pyLODE`
- Wildcard, e.g. `.*`
- Multiple repositories, e.g. `pyLODE|fastapi`

### Select the docstring (long and short) of a given repo

Selects the docstrings contained with a given repository

```
MATCH (n:Docstring)-[Documents]-(f:Function)-[:HasFunction|HasMethod]-()-[:Contains*1..]-(r:Repository)
WHERE (n.short_description IS NOT NULL OR n.long_description IS NOT NULL)
AND r.name =~ '<REPO>' RETURN r.name as `Repository`, f.name as `Function Name`,
n.short_description as `Docstring Summary`, n.long_description as `Doctring Body`
```

Query options for repository (`<REPO>`):

- Repository name, e.g. `pyLODE`
- Wildcard, e.g. `.*`
- Multiple repositories, e.g. `pyLODE|fastapi`

### Select the summarizations of functions of a given repo

Selects the function summarizations that belong to a particular repository.

```
MATCH (n:Docstring)-[:Documents]-(f)-[:HasFunction|HasMethod]-()-[:Contains*1..]-(r:Repository)
WHERE n.summarization IS NOT NULL AND r.name =~ '<REPO>'
RETURN r.name as `Repository`, f.name as `Function`,
n.summarization as `Summarization`
```

Query options for repository (`<REPO>`):

- Repository name, e.g. `pyLODE`
- Wildcard, e.g. `.*`
- Multiple repositories, e.g. `pyLODE|fastapi`

### Select the filenames of a given demo

Returns all the filenames for the given repository.

```
MATCH (m:Module)-[:Contains*1..]-(r:Repository) WHERE r.name =~ '<REPO>'
RETURN m.name + '.' + m.extension as `Filename`, r.name as `Repository`
```

Query options for repository (`<REPO>`):

- Repository name, e.g. `pyLODE`
- Wildcard, e.g. `.*`
- Multiple repositories, e.g. `pyLODE|fastapi`

### Select the function and class names of a given repo

Return the function and class names contained within a given repo.

```
MATCH (n:Class|Function)-[:HasFunction|HasMethod*0..]-()-[:Contains*1..]-(r:Repository)
WHERE r.name =~ '<REPO>' RETURN r.name as `Repository`, n.name as `Name`, labels(n) as `Type`
```

Query options for repository (`<REPO>`):

- Repository name, e.g. `pyLODE`
- Wildcard, e.g. `.*`
- Multiple repositories, e.g. `pyLODE|fastapi`

### Select the source code of a given repo

Return the function source code within a given repo.

```
MATCH (f:Function)-[:HasFunction|HasMethod*0..]-()-[:Contains*1..]-(r:Repository) WHERE r.name =~ '<REPO>' AND
f.source_code IS NOT NULL RETURN r.name as `Repository`, f.name as `Function`, f.source_code as `Source Code
```

Query options for repository (`<REPO>`):

- Repository name, e.g. `pyLODE`
- Wildcard, e.g. `.*`
- Multiple repositories, e.g. `pyLODE|fastapi`

### Select the call graph of a given repo

Select the call graph for a given function, possibly within a given repository.

```
MATCH (c:Function)-[:Calls]-(f:Function)-[:HasFunction|HasMethod*0..]-()-[:Contains*1..]-(r:Repository)
WHERE r.name =~ '<REPO>' AND f.canonical_name =~ '<FUNCTION>'  RETURN c, f
```

Query options for repository (`<REPO>`):

- Repository name, e.g. `pyLODE`
- Wildcard, e.g. `.*`
- Multiple repositories, e.g. `pyLODE|fastapi`

Query options for function (`<FUNCTION>`):

- Exact canonical name, e.g. `pylode.utils.rdf_obj_html`
- Wildcard query to match only the function name, e.g. `.*rdf_obj_html`
