from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import networkx as nx
import random

class CoopAgent(Agent):
    def __init__(self, unique_id, model, production_cost, REA_percent, market_price=20):
        super().__init__(unique_id, model)
        # Introduce variability in initial conditions
        self.production_cost = production_cost + random.uniform(-1, 1)
        self.REA_percent = REA_percent + random.uniform(-5, 5)
        self.market_price = market_price + random.uniform(-2, 2)
        self.equitable_price = None
        self.is_economically_advantaged = False
        self.interactions = []

    def step(self):
        # Dynamically use the model's current parameters
        self.calculate_equitable_price()
        self.update_economic_status()

        # Update interactions for this step
        next_agent_id = (self.unique_id + 1) % self.model.num_agents
        self.interactions = [next_agent_id]

    def calculate_equitable_price(self):
        # Dynamic logic based on updated agent parameters
        surplus = self.market_price - self.production_cost
        alpha = self.model.alpha_value
        equity_adjustment = surplus * alpha * (self.REA_percent / 100)
        self.equitable_price = self.market_price + equity_adjustment

    def update_economic_status(self):
        threshold = 15
        self.is_economically_advantaged = self.equitable_price > threshold

class CoopModel(Model):
    def __init__(self, N, production_cost, REA_percent, market_price, alpha_value):
        self.num_agents = int(N)
        self.production_cost = production_cost
        self.REA_percent = REA_percent
        self.market_price = market_price
        self.alpha_value = alpha_value
        self.schedule = RandomActivation(self)
        self.G = nx.Graph()

        # Create agents with variability
        for i in range(self.num_agents):
            a = CoopAgent(i, self, self.production_cost, self.REA_percent, self.market_price)
            self.schedule.add(a)

        self.datacollector = DataCollector(
            agent_reporters={"EquitablePrice": "equitable_price"}
        )

    def step(self):
        self.G.clear()
        for agent in self.schedule.agents:
            agent.step()

            # Reflect agent's status in node attributes
            color = "#FF0000" if agent.is_economically_advantaged else "#000000"
            size = 15 if agent.is_economically_advantaged else 10
            self.G.add_node(agent.unique_id, color=color, size=size)

            # Update edges
            for partner_id in agent.interactions:
                self.G.add_edge(agent.unique_id, partner_id)

        self.schedule.step()
        self.datacollector.collect(self)

    def text_visualization(self):
        print("Step:", self.schedule.steps)
        print("Number of Agents:", self.num_agents)
        print("Production Costs:", self.production_cost)
        print("REA Percent:", self.REA_percent)
        print("Market Price:", self.market_price)
        print("Alpha Value:", self.alpha_value)
