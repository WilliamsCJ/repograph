import csv
import logging
import os
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


def plot():
    df = pd.read_csv("./evaluation/results.csv")

    fig1 = plt.figure()
    ax1 = plt.axes()
    seaborn.scatterplot(x="Nodes", y="Time (s)", data=df, ax=ax1).set(
        title="Nodes Created vs Processing Time"
    )
    fig1.savefig("./evaluation/processing_time_vs_nodes.png")

    plt.clf()

    fig2 = plt.figure()
    ax2 = plt.axes()
    seaborn.scatterplot(
        x="Relationships", y="Time (s)", data=df, ax=ax2
    ).set(title="Relationships Created vs Processing Time")
    fig2.savefig("./evaluation/processing_time_vs_relationships.png")

    plt.clf()

    fig1 = plt.figure()
    ax1 = plt.axes()
    seaborn.scatterplot(x="Nodes", y="Time (s)", data=df[df['Nodes'] < 30000], ax=ax1).set(
        title="Nodes Created vs Processing Time (Nodes < 30,000)"
    )
    fig1.savefig("./evaluation/processing_time_vs_nodes_filtered.png")

    plt.clf()

    fig2 = plt.figure()
    ax2 = plt.axes()
    seaborn.scatterplot(
        x="Relationships", y="Time (s)", data=df[df['Relationships'] < 30000], ax=ax2
    ).set(title="Relationships Created vs Processing Time (Relationships < 30,000)")
    fig2.savefig("./evaluation/processing_time_vs_relationships_filtered.png")


plot()