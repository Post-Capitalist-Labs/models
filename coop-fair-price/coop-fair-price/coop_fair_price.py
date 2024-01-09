from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import networkx as nx

# Define the CoopAgent class
class CoopAgent(Agent):
    def __init__(self, unique_id, model, production_cost, REA_percent):
        super().__init__(unique_id, model)
        self.production_cost = production_cost
        self.REA_percent = REA_percent
        self.market_price = None
        self.equitable_price = None

    def step(self):
        # Agent step to calculate the equitable price
        surplus = self.market_price - self.production_cost
        alpha = self.calculate_alpha()  # Method to determine alpha based on REA%

        if self.REA_percent < 100:
            equity_adjustment = surplus * alpha
        elif self.REA_percent > 100:
            equity_adjustment = -surplus * alpha
        else:
            equity_adjustment = 0

        self.equitable_price = self.market_price + equity_adjustment
        # For simplicity, let's say each agent interacts with the next agent
        next_agent_id = (self.unique_id + 1) % self.model.num_agents
        self.model.interactions.append((self.unique_id, next_agent_id))

    def calculate_alpha(self):
        # Placeholder for alpha calculation logic based on REA%. For options and tradeoffs see https://github.com/Post-Capitalist-Labs/models/blob/main/coop-fair-price/calculate_alpha.md
        return 0.1  # As an example, a flat 10% rate

# Define the CoopModel class
class CoopModel(Model):
    def __init__(self, N):
        self.num_agents = N
        self.schedule = RandomActivation(self)
        self.interactions = []  # Store interactions here
        # Initialize agents with example data
        for i in range(self.num_agents):
            a = CoopAgent(i, self, production_cost=10, REA_percent=100)
            self.schedule.add(a)

        # Set up data collector
        self.datacollector = DataCollector(
            agent_reporters={"EquitablePrice": "equitable_price"}
        )

    def step(self):
        self.interactions.clear()  # Clear previous step's interactions
        # Collect data
        self.datacollector.collect(self)
        # Tell all the agents in the model to run their step function
        self.schedule.step()

# Instantiate and run the model
model = CoopModel(N=10)
for i in range(10):
    model.step()

# Gather the data
data = model.datacollector.get_agent_vars_dataframe()
print(data)
