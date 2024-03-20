from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import random

class CommonsAgent(Agent):
    """An agent with diverse opinions on resource management and a reputation system."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.opinion = self.random.choice([True, False])  # Initial simple opinion on lower resource usage limit
        self.reputation = random.uniform(0.5, 1.5)  # Random starting reputation score
        self.strategy = self.random.choice(['conservation', 'exploitation', 'moderation'])
        self.votes = {}

    def debate(self):
        # Agents interact and might change their opinion based on others' reputation and strategies
        for other_agent in self.model.schedule.agents:
            if other_agent.unique_id != self.unique_id:
                if other_agent.reputation > self.reputation and random.random() > 0.5:
                    self.strategy = other_agent.strategy  # Simple influence mechanism

    def propose(self):
        # Propose a management strategy based on current opinion and strategy
        return self.strategy

    def vote(self):
        # Collect votes for different strategies
        self.votes[self.strategy] = self.votes.get(self.strategy, 0) + 1

class DirectDemocracyModel(Model):
    """A model with agents voting on resource management strategies with environmental dynamics."""
    def __init__(self, N, resource_limit):
        self.num_agents = N
        self.schedule = RandomActivation(self)
        self.resource_limit = resource_limit
        self.environmental_health = 100  # Starting state of the environment
        
        # Create agents
        for i in range(self.num_agents):
            a = CommonsAgent(i, self)
            self.schedule.add(a)
        
        # DataCollector
        self.datacollector = DataCollector(
            model_reporters={
                "Resource Limit": lambda m: m.resource_limit,
                "Environmental Health": lambda m: m.environmental_health
            },
            agent_reporters={
                "Reputation": "reputation"
            }
        )

    def step(self):
        # Debate phase
        for agent in self.schedule.agents:
            agent.debate()
        
        # Proposal and voting phase
        votes = {}
        for agent in self.schedule.agents:
            proposal = agent.propose()
            votes[proposal] = votes.get(proposal, 0) + 1
        
        # Determine winning strategy and update resource limit and environmental health
        winning_strategy, votes_received = max(votes.items(), key=lambda x: x[1])
        if winning_strategy == "conservation":
            self.resource_limit = max(self.resource_limit - 10, 0)
            self.environmental_health += 5
        elif winning_strategy == "exploitation":
            self.resource_limit = min(self.resource_limit + 10, 200)
            self.environmental_health -= 5
        else:  # moderation strategy
            self.environmental_health = max(0, min(self.environmental_health, 100))  # No change to resource limit
        
        self.environmental_health = max(0, min(self.environmental_health, 100))  # Keep environmental health within bounds
        self.datacollector.collect(self)
        self.schedule.step()

# Example of model instantiation and running
model = DirectDemocracyModel(10, 100)
for i in range(20):
    model.step()
