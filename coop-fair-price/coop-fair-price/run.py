from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import NetworkModule
from mesa_viz_tornado.UserParam import *
from coop_fair_price import CoopModel

def network_portrayal(G):
    portrayal = dict()
    portrayal['nodes'] = [
        {
            'id': node_id,
            'size': G.nodes[node_id].get('size', 10),
            'color': G.nodes[node_id].get('color', "#000000")
        }
        for node_id in G.nodes
    ]
    portrayal['edges'] = [
        {
            'source': source,
            'target': target,
            'color': "#0000FF",  # Blue color for edges
            'width': 2           # Thicker width for visibility
        }
        for source, target in G.edges
    ]
    return portrayal

network = NetworkModule(network_portrayal, 1000, 1000)
server = ModularServer(CoopModel,
                       [network],
                       "Co-op Fair Price Model",
                       {"N": Slider("Number of Co-ops", 10, 2, 200, 1),
                        "production_cost": Slider("Production Cost", 10, 5, 20, 1),
                        "REA_percent": Slider("REA Percent", 100, 50, 150, 5),
                        "market_price": Slider("Market Price", 20, 10, 30, 1),
                        "alpha_value": Slider("Alpha Value", 0.1, 0.01, 0.2, 0.01)})

server.port = 8521  # Default is 8521
server.launch()
