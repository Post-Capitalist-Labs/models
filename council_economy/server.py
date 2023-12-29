from mesa_viz_tornado.ModularVisualization import *
from mesa_viz_tornado.UserParam import *
from mesa_viz_tornado.modules import CanvasGrid, ChartModule
from mesa_viz_tornado.ModularVisualization import ModularServer
from council_economy import CouncilBasedEconomyModel, WorkersCouncilAgent, ConsumersCouncilAgent

def agent_portrayal(agent):
    if agent is None:
        return

    portrayal = {"Shape": "circle", "Filled": "true", "r": 0.5, "Layer": 0}

    if isinstance(agent, WorkersCouncilAgent):
        portrayal["Color"] = "#FF0000"  # Red for WorkersCouncilAgent
    elif isinstance(agent, ConsumersCouncilAgent):
        portrayal["Color"] = "#0000FF"  # Blue for ConsumersCouncilAgent

    return portrayal

grid_width, grid_height = 20, 20
canvas_element = CanvasGrid(agent_portrayal, grid_width, grid_height, 500, 500)

chart_element = ChartModule([
    {"Label": "Worker Council Production Proposals", "Color": "Red"},
    {"Label": "Consumer Council Consumption Proposals", "Color": "Blue"}
])

model_params = {
    "num_workers_councils": Slider("Number of Worker Councils", 100, 1, 200, 1),
    "num_consumers_councils": Slider("Number of Consumer Councils", 100, 1, 200, 1),
    "worker_adjustment": Slider("Worker Propsals Adjustment", 10, 1, 20, 1),
    "consumer_adjustment": Slider("Consumer Proposal Adjustment", 10, 1, 20, 1),
    "width": grid_width,
    "height": grid_height
}

server = ModularServer(
    CouncilBasedEconomyModel,
    [canvas_element, chart_element],
    "Council Based Economy Model",
    model_params
    )
