import os

from yaml import UnsafeLoader
from repograph.container import ApplicationContainer
import time
import csv
from repograph.entities.build.service import BuildService
from repograph.entities.graph.service import GraphService
from dependency_injector.wiring import inject, Provide
from tqdm.auto import tqdm
from repograph.utils.logging import configure_logging
import logging

repositories = [
    ("./evaluation/demo/pygorithm", "pygorithm"),
    ("./evaluation/demo/pyLODE", "pyLODE"),
    ("./evaluation/demo/flake8", "flake8"),
    ("./evaluation/demo/fastapi", "FastAPI"),
]

configure_logging(logging.CRITICAL)


@inject
def collect(
    build: BuildService = Provide[ApplicationContainer.build.container.service],
    graph: GraphService = Provide[ApplicationContainer.graph.container.service],
):
    with open("./evaluation/processing_time.csv", "w+", newline="") as csvfile:
        writer = csv.writer(
            csvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        writer.writerow(["Repository", "Time (s)", "Nodes", "Relationships"])
        for i in tqdm(range(5)):
            for path, name in tqdm(repositories):
                start = time.time()
                build.build(
                    [path],
                    f"{name}{i}",
                    "",
                    prune=True,
                )
                execution_time = time.time() - start
                summary = graph.get_summary(f"{name}{i}")
                writer.writerow(
                    [
                        name,
                        execution_time,
                        summary.nodes_total,
                        summary.relationships_total,
                    ]
                )


if __name__ == "__main__":
    container = ApplicationContainer()
    container.config.from_yaml("./evaluation_config.yaml", loader=UnsafeLoader)
    container.wire(modules=[__name__])

    open("./evaluation/test.db", "w")

    try:
        collect()
    except:
        pass
    finally:
        os.remove("./evaluation/test.db")
