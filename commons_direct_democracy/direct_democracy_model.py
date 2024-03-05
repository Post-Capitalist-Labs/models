from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector

class CommonsAgent(Agent):
    """An agent with an opinion on resource usage limit."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.opinion = self.random.choice([True, False])  # True for supporting lower usage limit

    def vote(self):
        # Simple voting mechanism based on the agent's opinion
        return self.opinion

class DirectDemocracyModel(Model):
    """A model with some number of agents that vote on a resource usage limit."""
    def __init__(self, N, resource_limit):
        self.num_agents = N
        self.schedule = RandomActivation(self)
        self.resource_limit = resource_limit
        self.votes_for_lower_limit = 0
        
        # Create agents
        for i in range(self.num_agents):
            a = CommonsAgent(i, self)
            self.schedule.add(a)
            
        # DataCollector
        self.datacollector = DataCollector(
            model_reporters={"Resource Limit": "resource_limit"},
        )

    def step(self):
        self.votes_for_lower_limit = sum([agent.vote() for agent in self.schedule.agents])
        
        # Update resource limit based on vote
        if self.votes_for_lower_limit > self.num_agents / 2:
            self.resource_limit = max(self.resource_limit - 10, 0)  # Decrease limit, with a floor of 0
        else:
            self.resource_limit = min(self.resource_limit + 10, 200)  # Increase limit, with a ceiling of 200
        
        self.datacollector.collect(self)
        self.schedule.step()
