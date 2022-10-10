from repograph.neo4j import Neo4JDatabase


class Repograph(Neo4JDatabase):
    database: str

    def __init__(self, uri, user, password, database) -> None:
        super().__init__(uri, user, password, database)
