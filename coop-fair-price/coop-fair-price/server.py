from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import NetworkModule
from coop_fair_price import CoopModel, CoopAgent

def network_portrayal(G):
    # Dict to hold the portrayal for the network
    portrayal = dict()
    portrayal['nodes'] = [{'id': node_id, 'size': 10, 'color': "#FF0000" if G.nodes[node_id]['agent'].REA_percent > 100 else "#00FF00"} for node_id in G.nodes]
    portrayal['edges'] = [{'source': source, 'target': target} for source, target in G.edges]
    return portrayal

network = NetworkModule(network_portrayal, 500, 500)
server = ModularServer(CoopModel,
                       [network],
                       "Cooperative Model",
                       {"N":10})
server.port = 8521  # Default is 8521
server.launch()
