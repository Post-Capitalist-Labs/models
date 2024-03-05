from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from mesa_viz_tornado.UserParam import *
from direct_democracy_model import DirectDemocracyModel

def agent_portrayal(agent):
    portrayal = {"Shape": "circle", "Filled": "true", "r": 0.5, "Color": "green" if agent.opinion else "blue"}
    return portrayal

chart = ChartModule([{"Label": "Resource Limit", "Color": "Black"}],
                    data_collector_name='datacollector')

server = ModularServer(DirectDemocracyModel,
                       [chart],
                       "Direct Democracy Model",
                       {"N": UserParam('Slider', 'Number of Agents', 100, 10, 200, 1),
                        "resource_limit": UserParam('Slider', 'Initial Resource Limit', 100, 50, 150, 1)})

if __name__ == '__main__':
    server.launch()
