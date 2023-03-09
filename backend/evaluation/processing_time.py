# pragma: no cover
"""
Evaluate the performance of RepoGraph
"""
# base imports
import csv
import logging
import os
import shutil
import time

# pip imports
from dependency_injector.wiring import inject, Provide
import matplotlib.pyplot as plt
import pandas as pd
import seaborn
from tqdm.auto import tqdm
from yaml import UnsafeLoader

# Entity imports
from repograph.container import ApplicationContainer
from repograph.entities.build.service import BuildService
from repograph.entities.graph.service import GraphService

# Utils
from repograph.utils.logging import configure_logging

paths = [
    "./demo/pygorithm",
    "./demo/pyLODE",
    "./demo/flake8",
    "./demo/fastapi",
]

repositories = [
    ("pygorithm", "pygorithm"),
    ("pyLODE", "pylode"),
    ("flake8", "flake8"),
    ("fastapi", "fastapi"),
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
        for i in tqdm(range(3)):
            for path, name in tqdm(repositories):
                shutil.copytree(f"../demo/{path}", f"./evaluation/{path}")
                path = f"./evaluation/{path}"

                try:
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
                finally:
                    shutil.rmtree(path)


def plot():
    df = pd.read_csv("./evaluation/processing_time.csv")
    print(df)

    ax1 = seaborn.scatterplot(x="Nodes", y="Time (s)", data=df, hue="Repository").set(
        title="Nodes Created vs Processing Time"
    )
    fig1 = ax1.get_figure()
    fig1.savefig("./evaluation/processing_time_vs_nodes.png")
    plt.clf()
    ax2 = seaborn.scatterplot(
        x="Relationships", y="Time (s)", data=df, hue="Repository"
    ).set(title="Relationships Created vs Processing Time")
    fig2 = ax2.get_figure()
    fig2.savefig("./evaluation/processing_time_vs_relationships.png")


if __name__ == "__main__":
    container = ApplicationContainer()
    container.config.from_yaml("./evaluation_config.yaml", loader=UnsafeLoader)
    container.wire(modules=[__name__])

    open("./evaluation/test.db", "w")

    print("Evaluating processing times...")

    try:
        collect()
        plot()
    except Exception as e:
        print("ERROR: ", e)
    finally:
        os.remove("./evaluation/test.db")
