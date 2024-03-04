from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import NetworkModule
from mesa.visualization.UserParam import Slider 
from coop_fair_price import CoopModel 

def network_portrayal(G):
    portrayal = {
        'nodes': [
            {
                'id': node_id,
                'size': G.nodes[node_id].get('size', 10),
                'color': G.nodes[node_id].get('color', "#000000")  # Default color is black
            }
            for node_id in G.nodes
        ],
        'edges': [
            {
                'source': source,
                'target': target,
                'color': "#0000FF",  # Blue color for edges for consistency
                'width': 2  # Thicker width for visibility
            }
            for source, target in G.edges
        ]
    }
    return portrayal

# Network visualization size can be adjusted as needed
network = NetworkModule(network_portrayal, 1000, 1000)

server = ModularServer(CoopModel,
                       [network],
                       "Co-op Fair Price Model",
                       {"N": Slider("Number of Co-ops", 10, 2, 200, 1),
                        "production_cost": Slider("Production Cost", 15, 5, 25, 1),
                        "REA_percent": Slider("REA Percent", 100, 50, 150, 1),
                        "market_price": Slider("Market Price", 20, 10, 30, 1),
                        "alpha_value": Slider("Alpha Value", 0.1, 0.01, 0.2, 0.01)})

# If you have a specific port in mind, you can set it here. Otherwise, it defaults to 8521
server.port = 8521
server.launch()
