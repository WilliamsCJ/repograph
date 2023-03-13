# pragma: no cover
"""
Evaluate the performance of RepoGraph
"""
# base imports
import csv
import logging
import os
import shutil
import subprocess
import time
import string

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

repositories = [
    "tiangolo/fastapi",
    "RDFLib/pyLODE",
    "PyCQA/flake8",
    "OmkarPathak/pygorithm",
    "py2neo-org/py2neo",
]

data = pd.read_csv("./evaluation/software_type_benchmark.csv", sep=",")

repositories = repositories + list(data["repository"])

configure_logging(logging.CRITICAL)


@inject
def collect(
    build: BuildService = Provide[ApplicationContainer.build.container.service],
    graph: GraphService = Provide[ApplicationContainer.graph.container.service],
):
    with open("./evaluation/results.csv", "w+", newline="") as csvfile:
        writer = csv.writer(
            csvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        writer.writerow(["Repository", "Success", "Time (s)", "Nodes", "Relationships"])
        for repo in tqdm(repositories):
            name = repo.split("/")[1].lower()
            name = name.translate(str.maketrans("", "", string.punctuation))
            d = f"./{name}"

            try:
                subprocess.run(
                    ["git", "clone", f"https://github.com/{repo.lower()}", d]
                )

                start = time.time()
                build.build(
                    [d],
                    f"{name}",
                    "",
                    prune=True,
                )
                execution_time = time.time() - start
                summary = graph.get_summary(f"{name}")
                writer.writerow(
                    [
                        repo,
                        "True",
                        execution_time,
                        summary.nodes_total,
                        summary.relationships_total,
                    ]
                )
            except Exception as e:
                print("ERROR: ", e)
                writer.writerow(
                    [
                        repo,
                        "False",
                        0,
                        0,
                        0,
                    ]
                )
            finally:
                shutil.rmtree(d)


def plot():
    df = pd.read_csv("./evaluation/results.csv")
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
