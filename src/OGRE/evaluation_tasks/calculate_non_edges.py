"""
For link prediction mission, one needs a csv file of non edges of each graph. This file creates them.
For your own dataset, you need its name and path to where it can be found (see downward). If your dataset needs a
different way of loading, add it, in the end you need a networkx graph.
"""
from __future__ import annotations
import copy
import networkx as nx
from .eval_utils import load_graph
import os
import itertools as IT
import csv
import random


def calculate_non_edges(graph: nx.Graph | str, name: str, save_path: str = ".", percentage: float = 0.5) -> None:
    """
    Calculate the non edges of a graph and save them in a csv file.
    :param name: name of the dataset
    :param graph: networkx graph or path to the graph without the graph name
    :param save_path: path to save the csv file
    :param percentage: percentage of non edges to be generated. Default is 0.5.
    non-edge might be too big for all nodes, choose the biggest portion your device
    can handle with.
    :return:
    """
    if isinstance(graph, str):
        G: nx.Graph = load_graph(graph, name, False)
    else:
        G: nx.Graph = copy.deepcopy(graph)

    list_in_embd = list(G.nodes())
    portion = int(len(list_in_embd) * percentage)

    # choosing randomly indices of the nodes because non-edge is too big for all nodes, choose the biggest size your device
    # can handle with
    indexes = random.sample(range(1, len(list_in_embd)), portion)
    new_list = []
    for l in indexes:
        new_list.append(list_in_embd[l])
    sub_G: nx.Graph = G.subgraph(new_list)
    print(sub_G.number_of_nodes())
    # create a list of all missing edges of the nodes that were chosen randomly
    missing = [pair for pair in IT.combinations(sub_G.nodes(), 2) if not sub_G.has_edge(*pair)]
    print(len(missing))

    # extract list to a csv file, save it where you want, you will need it for link prediction task
    csvfile = open(os.path.join(save_path, f'non_edges_{name}.csv'), 'w', newline='')
    obj = csv.writer(csvfile)
    obj.writerows(missing)
    csvfile.close()
