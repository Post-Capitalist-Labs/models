from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import networkx as nx
import random

class CoopAgent(Agent):
    def __init__(self, unique_id, model, production_cost, REA_percent, market_price=20):
        super().__init__(unique_id, model)
        self.production_cost = production_cost + random.uniform(-1, 1)
        self.REA_percent = REA_percent + random.uniform(-5, 5)
        self.market_price = market_price + random.uniform(-2, 2)
        self.equitable_price = None
        self.is_economically_advantaged = False
        self.interactions = []
        # Initialize with a default color to avoid AttributeError before the first step
        self.color = "#000000"

    def step(self):
        self.calculate_equitable_price()
        # Update color based on the new equitable price
        self.color = self.determine_color()
        self.update_economic_status()
        self.consume_resources()
        self.exploit_opportunities()
        self.redistribute_surplus()

        # Determine interactions
        next_agent_id = (self.unique_id + 1) % self.model.num_agents
        self.interactions = [next_agent_id]

    def calculate_equitable_price(self):
        surplus = self.market_price - self.production_cost
        alpha = self.model.alpha_value
        equity_adjustment = surplus * alpha
        self.equitable_price = self.market_price + equity_adjustment

    def update_economic_status(self):
        threshold = 15
        self.is_economically_advantaged = self.equitable_price > threshold

    def consume_resources(self):
        # Placeholder for consuming resources from the environment
        pass

    def exploit_opportunities(self):
        # Placeholder for exploiting new opportunities in the environment
        pass

    def redistribute_surplus(self):
        # Placeholder for redistributing surplus if economically advantaged
        pass

    def determine_color(self):
        # Make sure equitable_price is calculated before determining color
        if self.equitable_price is None:
            return "#000000"  # Default color if equitable_price hasn't been set

        price_difference = self.equitable_price - self.market_price
        upper_threshold = 1
        lower_threshold = -1

        if price_difference > upper_threshold:
            return "#FF0000"  # Red for wealthy
        elif price_difference < lower_threshold:
            return "#FFFF00"  # Yellow for under-resourced
        else:
            return "#00FF00"  # Green for equitable distribution

class Environment:
    def __init__(self):
        self.resources = {"Resource1": 100, "Resource2": 100}
        self.opportunities = []

    def consume_resource(self, agent):
        pass

    def exploit_opportunity(self, agent):
        pass

    def redistribute_surplus(self, agent):
        pass

    def regenerate_resources(self):
        pass

    def generate_opportunities(self):
        pass

class CoopModel(Model):
    def __init__(self, N, production_cost, REA_percent, market_price, alpha_value):
        self.num_agents = int(N)
        self.production_cost = production_cost
        self.REA_percent = REA_percent
        self.market_price = market_price
        self.alpha_value = alpha_value
        self.schedule = RandomActivation(self)
        self.environment = Environment()
        self.G = nx.Graph()

        for i in range(self.num_agents):
            a = CoopAgent(i, self, self.production_cost, self.REA_percent, self.market_price)
            self.schedule.add(a)

        self.datacollector = DataCollector(
            agent_reporters={"EquitablePrice": "equitable_price"}
        )

    def step(self):
        self.environment.regenerate_resources()
        self.environment.generate_opportunities()

        self.G.clear()
        for agent in self.schedule.agents:
            agent.step()
            # Use agent's updated color attribute for node color
            color = agent.color
            size = 15 if agent.is_economically_advantaged else 10
            self.G.add_node(agent.unique_id, color=color, size=size)

            for partner_id in agent.interactions:
                self.G.add_edge(agent.unique_id, partner_id)

        self.schedule.step()
        self.datacollector.collect(self)
