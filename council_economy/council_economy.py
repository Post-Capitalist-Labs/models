from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import random

class CouncilAgent(Agent):
    def __init__(self, unique_id, model, initial_plan_min, initial_plan_max):
        super().__init__(unique_id, model)
        self.plan = random.randint(initial_plan_min, initial_plan_max)
        self.attempts_without_match = 0
        self.met_unmatched = False
        self.encountered_proposals = []

    def teleport_if_unmatched(self, max_attempts):
        if self.attempts_without_match > max_attempts:
            x = random.randrange(self.model.grid.width)
            y = random.randrange(self.model.grid.height)
            self.model.grid.move_agent(self, (x, y))
            self.attempts_without_match = 0

    def adjust_proposal(self, global_average, min_value, max_value):
        old_plan = self.plan
        learning_factor = self.calculate_learning_factor()
        self.plan += (global_average - self.plan) * learning_factor
        self.plan = max(min_value, min(self.plan, max_value))
        global_average = self.model.calculate_global_average_plan()
        self.plan = (self.plan + global_average) // 2  # Move towards the global average
        self.plan += random.randint(-5, 5)  # Random fluctuation
        self.plan = max(min_value, min(max_value, self.plan))
        target_plan = self.calculate_target_plan()
        distance = abs(self.plan - target_plan)
        distance_to_average = abs(self.plan - global_average)
        adjustment = max(1, distance // 4)  # Dynamic adjustment based on distance

        if self.met_unmatched:
            self.plan += adjustment
        else:
            self.plan -= adjustment
        self.plan = max(min_value, min(max_value, self.plan))
        print(f"Agent {self.unique_id} adjusted plan from {old_plan} to {self.plan}")

        # Feedback Mechanism: Incorporate success/failure history into adjustment
        if self.met_unmatched:
            self.plan += self.calculate_feedback_adjustment()
        else:
            self.plan -= self.calculate_feedback_adjustment()
        self.plan = max(min_value, min(max_value, self.plan))

    def calculate_learning_factor(self):
            # Implement a learning factor based on past encounters
            if not self.encountered_proposals:
                return 1  # Default factor if no encounters

            # Calculate learning factor based on historical data
            return sum(self.encountered_proposals) / len(self.encountered_proposals) / self.plan

    def calculate_target_plan(self):
        if not self.encountered_proposals:
            return self.plan  # Return current plan if no encounters

        average_encounter = sum(self.encountered_proposals) / len(self.encountered_proposals)
        target = average_encounter * 0.8  # Targeting less than 5 proposals per agent
        return target

    def move_towards_unmatched(self, adjustment):
        max_steps = adjustment // 2
        for _ in range(max_steps):
            possible_steps = self.model.grid.get_neighborhood(
                self.pos, moore=True, include_center=False)
            new_position = random.choice(possible_steps)
            self.model.grid.move_agent(self, new_position)

    def check_for_potential_matches(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if isinstance(self, WorkersCouncilAgent):
            self.met_unmatched = any(isinstance(agent, ConsumersCouncilAgent) for agent in cellmates)
        elif isinstance(self, ConsumersCouncilAgent):
            self.met_unmatched = any(isinstance(agent, WorkersCouncilAgent) for agent in cellmates)
        self.attempts_without_match = 0 if self.met_unmatched else self.attempts_without_match + 1

    def record_encounter(self, encountered_plan):
        self.encountered_proposals.append(encountered_plan)   
        
    def calculate_global_average_plan(self):
        print("Incorrect method call to calculate_global_average_plan on agent")
        return 0  # Dummy return

class WorkersCouncilAgent(CouncilAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model, 50, 100)

    def step(self):
        self.check_for_potential_matches()
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for agent in cellmates:
            if isinstance(agent, ConsumersCouncilAgent):
                self.record_encounter(agent.plan)
        self.move_towards_unmatched(self.model.worker_adjustment)
        self.teleport_if_unmatched(max_attempts=400)

    def calculate_feedback_adjustment(self):

        global_average_plan = self.model.calculate_global_average_plan()
        self.adjust_proposal(global_average_plan, 50, 150)

class ConsumersCouncilAgent(CouncilAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model, 60, 120)

    def step(self):
        self.check_for_potential_matches()
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for agent in cellmates:
            if isinstance(agent, WorkersCouncilAgent):
                self.record_encounter(agent.plan)
        self.move_towards_unmatched(self.model.consumer_adjustment)
        self.teleport_if_unmatched(max_attempts=400)
    def calculate_feedback_adjustment(self):

        global_average_plan = self.model.calculate_global_average_plan()
        self.adjust_proposal(global_average_plan, 60, 130)

class CouncilBasedEconomyModel(Model):
    def __init__(self, num_workers_councils, num_consumers_councils, worker_adjustment, consumer_adjustment, width, height, acceptable_proposal_difference, stability_window, min_unmatched_threshold):
        super().__init__()
        self.num_workers_councils = num_workers_councils
        self.num_consumers_councils = num_consumers_councils
        self.worker_adjustment = worker_adjustment
        self.consumer_adjustment = consumer_adjustment
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.acceptable_proposal_difference = acceptable_proposal_difference
        self.stability_window = stability_window
        self.min_unmatched_threshold = min_unmatched_threshold
        self.proposal_history = []
        self.datacollector = DataCollector(
            model_reporters={
                "Worker Council Production Proposals": lambda m: sum(agent.plan for agent in m.schedule.agents if isinstance(agent, WorkersCouncilAgent)),
                "Consumer Council Consumption Proposals": lambda m: sum(agent.plan for agent in m.schedule.agents if isinstance(agent, ConsumersCouncilAgent))
            }
        )

        for i in range(self.num_workers_councils):
            agent = WorkersCouncilAgent(i, self)
            self.schedule.add(agent)
            self.place_agent_randomly(agent)

        for i in range(self.num_consumers_councils):
            agent = ConsumersCouncilAgent(i + self.num_workers_councils, self)
            self.schedule.add(agent)
            self.place_agent_randomly(agent)

        self.total_matched_proposals = 0
        self.total_unmatched_proposals = 0
        self.time_to_equilibrium = None

    def place_agent_randomly(self, agent):
        x = random.randrange(self.grid.width)
        y = random.randrange(self.grid.height)
        while not self.grid.is_cell_empty((x, y)):
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
        self.grid.place_agent(agent, (x, y))

    def calculate_global_average_plan(self):
        total_plan = sum(agent.plan for agent in self.schedule.agents)
        return total_plan / len(self.schedule.agents) if self.schedule.agents else 0

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

        matched, unmatched_consumers, unmatched_workers = self.proposals_status()
        self.proposal_history.append((matched, unmatched_consumers, unmatched_workers))
        if len(self.proposal_history) > self.stability_window:
            self.proposal_history.pop(0)  # Remove oldest record

        if self.check_balanced_proposals() and self.check_stability_in_proposals() and self.check_minimal_unmatched_proposals():
            self.running = False

        self.text_visualization()

    def check_balanced_proposals(self):
        worker_proposals = sum(agent.plan for agent in self.schedule.agents if isinstance(agent, WorkersCouncilAgent))
        consumer_proposals = sum(agent.plan for agent in self.schedule.agents if isinstance(agent, ConsumersCouncilAgent))
        return abs(worker_proposals - consumer_proposals) <= self.acceptable_proposal_difference

    def check_stability_in_proposals(self):
        if len(self.proposal_history) < self.stability_window:
            return False
        avg_matched = sum(hist[0] for hist in self.proposal_history) / self.stability_window
        return all(abs(hist[0] - avg_matched) <= self.acceptable_proposal_difference for hist in self.proposal_history)

    def check_minimal_unmatched_proposals(self):
        return all(hist[1] + hist[2] <= self.min_unmatched_threshold for hist in self.proposal_history)

    def text_visualization(self):
        matched, unmatched_consumers, unmatched_workers = self.proposals_status()
        self.total_matched_proposals += matched
        self.total_unmatched_proposals += (unmatched_consumers + unmatched_workers)

        print(f"Step: {self.schedule.steps}")
        print(f"Number of Workers' Councils: {self.num_workers_councils}")
        print(f"Number of Consumers' Councils: {self.num_consumers_councils}")
        print(f"Worker Adjustment: {self.worker_adjustment}")
        print(f"Consumer Adjustment: {self.consumer_adjustment}")
        print(f"Matched Proposals This Step: {matched}")
        print(f"Unmatched Consumer Proposals This Step: {unmatched_consumers}")
        print(f"Unmatched Worker Proposals This Step: {unmatched_workers}")
        print(f"Total Matched Proposals: {self.total_matched_proposals}")
        print(f"Total Unmatched Proposals: {self.total_unmatched_proposals}")
        print(f"Acceptable Proposal Difference: {self.acceptable_proposal_difference}")
        print(f"Stability Window: {self.stability_window}")
        print(f"Minimal Unmatched Threshold: {self.min_unmatched_threshold}")
        if self.time_to_equilibrium is not None:
            print(f"Time to Equilibrium: {self.time_to_equilibrium} steps")
        else:
            print("Equilibrium not yet reached.")
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
