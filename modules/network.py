import matplotlib.pyplot as plt
import networkx as nx
from networkx.readwrite import json_graph
from modules import globals
import json


class Network:
    def __init__(self):
        self.G = None
        self.graph_data = {
            "node_labels": {},
            "edge_labels": {}
        }

    def write_data_json(self, filename="data/network2.json"):
        try:
            with open(filename, 'w') as f:
                data = json_graph.node_link_data(self.G)
                f.write(json.dumps(data, indent=2))
        except:
            globals.print_exception("write data json")

    def load_data_json(self, filename="data/network.json"):
        try:
            with open(filename, 'r') as f:
                data = f.read()
                data = json.loads(data)
                self.get_graph_data(data)

                self.G = json_graph.node_link_graph(data)
        except:
            globals.print_exception("load data json")

    def get_graph_data(self, data):
        self.graph_data["node_labels"] = {}
        self.graph_data["edge_labels"] = {}

        for node in data["nodes"]:
            try:
                self.graph_data["node_labels"][node["id"]] = node["label"]
            except:
                self.graph_data["node_labels"][node["id"]] = node["id"]

        for (i, edge) in enumerate(data["links"]):
            try:
                self.graph_data["edge_labels"][edge["id"]] = edge["label"]
            except:
                self.graph_data["edge_labels"][edge["id"]] = i

    def get_data(self):
        return list(self.G.adjacency())

    def disp(self):
        # nx.circular_layout
        # nx.spring_layout
        # https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.drawing.nx_pylab.draw_networkx.html
        # nx.draw(self.G, pos=nx.circular_layout(self.G), labels=self.graph_data["labeldict"], with_labels=True)
        G = self.G
        pos = nx.circular_layout(self.G)
        nx.draw(G, pos)
        # node_labels = nx.get_node_attributes(G, 'label')
        nx.draw_networkx_labels(G, pos, labels=self.graph_data["node_labels"])
        # edge_labels = nx.get_edge_attributes(G, 'label')
        # nx.draw_networkx_edge_labels(G, pos, edge_labels)
        nx.draw_networkx_edge_labels(G, pos, labels=self.graph_data["edge_labels"])
        plt.show()

