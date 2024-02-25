from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import networkx as nx
import random

class CoopAgent(Agent):
    def __init__(self, unique_id, model, production_cost, REA_percent, market_price=20):
        super().__init__(unique_id, model)
        self.production_cost = production_cost + random.uniform(-1, 1)
        # Adjusted to directly assign randomized REA_percent
        self.REA_percent = REA_percent + random.uniform(-5, 5)
        self.market_price = market_price + random.uniform(-2, 2)
        self.equitable_price = None
        self.is_economically_advantaged = False
        self.interactions = []
        # Determine initial color based on REA%
        self.color = self.determine_color()

    def step(self):
        self.calculate_equitable_price()
        self.update_economic_status()
        self.consume_resources()
        self.exploit_opportunities()
        self.redistribute_surplus()

        # Determine interactions
        next_agent_id = (self.unique_id + 1) % self.model.num_agents
        self.interactions = [next_agent_id]
        # Update color based on REA% after interactions
        self.color = self.determine_color()

    def calculate_equitable_price(self):
        surplus = self.market_price - self.production_cost
        alpha = self.model.alpha_value
        equity_adjustment = surplus * alpha
        self.equitable_price = self.market_price + equity_adjustment

    def update_economic_status(self):
        threshold = 15
        self.is_economically_advantaged = self.equitable_price > threshold

    def consume_resources(self):
        # Consume resources from the environment
        self.model.environment.consume_resource(self)

    def exploit_opportunities(self):
        # Check and exploit new opportunities in the environment
        self.model.environment.exploit_opportunity(self)

    def redistribute_surplus(self):
        # Redistribute surplus if economically advantaged
        if self.is_economically_advantaged:
            self.model.environment.redistribute_surplus(self)

    def determine_color(self):
        # Determine the difference between the equitable price and the market price
        price_difference = self.equitable_price - self.market_price

        # Define thresholds for determining when an agent is considered to have achieved
        # an equitable distribution. These thresholds can be adjusted.
        upper_threshold = 1 # Considered wealthy if the price difference is above this value
        lower_threshold = -1 # Considered under-resourced if the price difference is below this value

        # Determine color based on price difference
        if price_difference > upper_threshold:
            return "#FFOOOO" # Red for wealthy
        elif price_difference < lower_threshold:
            return "#FFFFOO" # Yellow for under-resourced
        else:
            return "OOFFOO" # Green for equitable distribution

class Environment:
    def __init__(self):
        self.resources = {"Resource1": 100, "Resource2": 100}
        self.opportunities = []

    def consume_resource(self, agent):
        # Logic for consuming resources
        pass

    def exploit_opportunity(self, agent):
        # Logic for agents to exploit opportunities
        pass

    def redistribute_surplus(self, agent):
        # Logic for redistributing surplus from advantaged agents
        pass

    def regenerate_resources(self):
        # Logic for resource regeneration
        pass

    def generate_opportunities(self):
        # Logic for generating new opportunities
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

            # Use agent's color attribute for node color
            color = agent.color
            size = 15 if agent.is_economically_advantaged else 10
            self.G.add_node(agent.unique_id, color=color, size=size)

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

        # Log: Print a summary after each step
        advantaged_count = sum(1 for a in self.schedule.agents if a.is_economically_advantaged)
        print(f"End of step {self.schedule.steps}: {advantaged_count} agents are economically advantaged out of {self.num_agents}")
