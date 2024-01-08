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
        self.move()

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False)
        new_position = random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

class ConsumersCouncilAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.consumption_plan = random.randint(60, 120)

    def step(self):
        adjustment = self.model.consumer_adjustment
        self.consumption_plan += random.randint(-adjustment, adjustment)
        self.move()

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False)
        new_position = random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

class CouncilBasedEconomyModel(Model):
    def __init__(self, num_workers_councils, num_consumers_councils, worker_adjustment, consumer_adjustment, width, height):
        super().__init__()
        self.num_workers_councils = num_workers_councils
        self.num_consumers_councils = num_consumers_councils
        self.worker_adjustment = worker_adjustment
        self.consumer_adjustment = consumer_adjustment
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.datacollector = DataCollector(
            model_reporters={
                "Worker Council Production Proposals": lambda m: sum(agent.production_plan for agent in m.schedule.agents if isinstance(agent, WorkersCouncilAgent)),
                "Consumer Council Consumption Proposals": lambda m: sum(agent.consumption_plan for agent in m.schedule.agents if isinstance(agent, ConsumersCouncilAgent))
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

        # Initialize variables for tracking proposals
        self.total_matched_proposals = 0
        self.total_unmatched_proposals = 0

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

        # Update text visualization before checking all proposals matched
        self.text_visualization()

        if self.all_proposals_matched():
            self.running = False

    def text_visualization(self):
        matched, unmatched_consumers, unmatched_workers = self.proposals_status()
        self.total_matched_proposals += matched
        self.total_unmatched_proposals += (unmatched_consumers + unmatched_workers)

        print(f"Step: {self.schedule.steps}")
        print(f"Number of Workers Councils: {self.num_workers_councils}")
        print(f"Number of Consumers Councils: {self.num_consumers_councils}")
        print(f"Worker Adjustment: {self.worker_adjustment}")
        print(f"Consumer Adjustment: {self.consumer_adjustment}")
        print(f"Matched Proposals This Step: {matched}")
        print(f"Total Matched Proposals: {self.total_matched_proposals}")
        print(f"Unmatched Consumer Proposals This Step: {unmatched_consumers}")
        print(f"Unmatched Worker Proposals This Step: {unmatched_workers}")
        print(f"Total Unmatched Proposals: {self.total_unmatched_proposals}")
        print("-----------------------------------")

    def proposals_status(self):
        matched = 0
        unmatched_consumers = 0
        unmatched_workers = 0

        for cell in self.grid.coord_iter():
            agents = cell[0]
            if len(agents) > 1:
                if any(isinstance(agent, WorkersCouncilAgent) for agent in agents) and \
                   any(isinstance(agent, ConsumersCouncilAgent) for agent in agents):
                    matched += 1
                else:
                    unmatched_consumers += sum(1 for agent in agents if isinstance(agent, ConsumersCouncilAgent))
                    unmatched_workers += sum(1 for agent in agents if isinstance(agent, WorkersCouncilAgent))
            else:
                unmatched_consumers += sum(1 for agent in agents if isinstance(agent, ConsumersCouncilAgent))
                unmatched_workers += sum(1 for agent in agents if isinstance(agent, WorkersCouncilAgent))

        return matched, unmatched_consumers, unmatched_workers

    def all_proposals_matched(self):
        for cell in self.grid.coord_iter():
            agents = cell[0]
            if len(agents) > 1:
                if any(isinstance(agent, WorkersCouncilAgent) for agent in agents) and \
                   any(isinstance(agent, ConsumersCouncilAgent) for agent in agents):
                    continue
                else:
                    return False
        return True

    def place_agent_randomly(self, agent):
        x = random.randrange(self.grid.width)
        y = random.randrange(self.grid.height)
        while not self.grid.is_cell_empty((x, y)):
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
        self.grid.place_agent(agent, (x, y))
