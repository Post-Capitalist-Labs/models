from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import networkx as nx

class CoopAgent(Agent):
    def __init__(self, unique_id, model, production_cost, REA_percent, market_price=20):
        super().__init__(unique_id, model)
        self.production_cost = production_cost
        self.REA_percent = REA_percent
        self.market_price = market_price
        self.equitable_price = None
        self.interactions = []  # Track interactions

    def step(self):
        if self.market_price is None:
            self.market_price = 20

        surplus = self.market_price - self.production_cost
        alpha = self.calculate_alpha()

        if self.REA_percent < 100:
            equity_adjustment = surplus * alpha
        elif self.REA_percent > 100:
            equity_adjustment = -surplus * alpha
        else:
            equity_adjustment = 0

        self.equitable_price = self.market_price + equity_adjustment

        # Update interactions for this step
        next_agent_id = (self.unique_id + 1) % self.model.num_agents
        self.interactions.append(next_agent_id)

    def calculate_alpha(self):
        return self.model.alpha_value

class CoopModel(Model):
    def __init__(self, N, production_cost, REA_percent, market_price, alpha_value):
        self.num_agents = int(N)
        self.production_cost = production_cost
        self.REA_percent = REA_percent
        self.market_price = market_price
        self.alpha_value = alpha_value
        self.schedule = RandomActivation(self)
        self.G = nx.Graph()

        for i in range(self.num_agents):
            a = CoopAgent(i, self, self.production_cost, self.REA_percent, self.market_price)
            self.schedule.add(a)

        self.datacollector = DataCollector(
            agent_reporters={"EquitablePrice": "equitable_price"}
        )

    def step(self):
        self.G.clear()
        for agent in self.schedule.agents:
            self.G.add_node(agent.unique_id, agent=agent, size=10, color="#000000" if agent.REA_percent <= 100 else "#FF0000")

            # Update edges based on interactions
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
