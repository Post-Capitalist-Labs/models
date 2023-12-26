from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import random

class WorkersCouncilAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.production_plan = random.randint(50, 100)

    def step(self):
        adjustment = self.model.worker_adjustment
        self.production_plan += random.randint(-adjustment, adjustment)

class ConsumersCouncilAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.consumption_plan = random.randint(60, 120)

    def step(self):
        adjustment = self.model.consumer_adjustment
        self.consumption_plan += random.randint(-adjustment, adjustment)

class CouncilBasedEconomyModel(Model):
    def __init__(self, num_workers_councils, num_consumers_councils, worker_adjustment, consumer_adjustment, width, height):
        super().__init__()
        self.worker_adjustment = worker_adjustment
        self.consumer_adjustment = consumer_adjustment
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.datacollector = DataCollector(
            model_reporters={
                "Total Production": lambda m: sum(agent.production_plan for agent in m.schedule.agents if isinstance(agent, WorkersCouncilAgent)),
                "Total Consumption": lambda m: sum(agent.consumption_plan for agent in m.schedule.agents if isinstance(agent, ConsumersCouncilAgent))
            }
        )

        for i in range(num_workers_councils):
            agent = WorkersCouncilAgent(i, self)
            self.schedule.add(agent)
            self.place_agent_randomly(agent)

        for i in range(num_consumers_councils):
            agent = ConsumersCouncilAgent(i + num_workers_councils, self)
            self.schedule.add(agent)
            self.place_agent_randomly(agent)

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

    def place_agent_randomly(self, agent):
        x = random.randrange(self.grid.width)
        y = random.randrange(self.grid.height)
        while not self.grid.is_cell_empty((x, y)):
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
        self.grid.place_agent(agent, (x, y))
