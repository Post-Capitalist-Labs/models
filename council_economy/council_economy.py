import argparse
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
        min_value = 0   # Example of a widened minimum value
        max_value = 100 # Example of a widened maximum value
        fixed_adjustment = 5  # A fixed adjustment value
        self.plan += fixed_adjustment # Apply the fixed adjustment
        old_plan = self.plan
        learning_factor = self.calculate_learning_factor()
        self.plan += (global_average - self.plan) * learning_factor
        self.plan = max(min_value, min(self.plan, max_value))
        global_average = self.model.calculate_global_average_plan()
        self.plan = (self.plan * 1 + global_average * 2) // 3  # Weight the global average X 2. Move towards the global average
        self.plan += random.randint(-1, 1)  # Random fluctuation
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

    def calculate_learning_factor(self):
        max_learning_rate = 0.5  # Maximum learning rate
        increase_per_attempt = 0.01  # Increase in learning rate per unmatched attempt

        # The learning factor increases with each unmatched attempt, up to a maximum
        return min(max_learning_rate, increase_per_attempt * self.attempts_without_match)

    def calculate_target_plan(self):
        # Use a global metric, like the average of all current plans
        global_average_plan = self.model.calculate_global_average_plan()
        return global_average_plan

    def move_towards_unmatched(self, adjustment):
        max_steps = adjustment // 2
        for _ in range(max_steps):
            possible_steps = self.model.grid.get_neighborhood(
                self.pos, moore=True, include_center=False)
            new_position = random.choice(possible_steps)
            self.model.grid.move_agent(self, new_position)

    def check_for_potential_matches(self):
        if self.pos is None:
            print(f"Agent {self.unique_id} has no position.")
            return  # Skip further processing for this agent
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
    def __init__(self, num_workers_councils, num_consumers_councils, worker_adjustment, consumer_adjustment, acceptable_proposal_difference, stability_window, min_unmatched_threshold):
        super().__init__()
        self.num_workers_councils = num_workers_councils
        self.num_consumers_councils = num_consumers_councils
        self.worker_adjustment = worker_adjustment
        self.consumer_adjustment = consumer_adjustment
        self.grid = MultiGrid(20, 20, True) # Fixed grid size
        self.schedule = RandomActivation(self)
        self.datacollector = DataCollector(
            model_reporters={
                "Worker Council Proposals": lambda m: sum(agent.plan for agent in m.schedule.agents if isinstance(agent, WorkersCouncilAgent)),
                "Consumer Council Proposals": lambda m: sum(agent.plan for agent in m.schedule.agents if isinstance(agent, ConsumersCouncilAgent))
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

        self.acceptable_proposal_difference = acceptable_proposal_difference
        self.stability_window = stability_window
        self.min_unmatched_threshold = min_unmatched_threshold
        self.total_matched_proposals = 0
        self.total_unmatched_proposals = 0
        self.proposal_history = []
        self.time_to_equilibrium = None
        self.matched_proposals_history = []
        self.total_steps = 0

    def place_agent_randomly(self, agent):
        max_attempts = 200  # Set a maximum number of attempts
        attempt = 0

        while attempt < max_attempts:
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            if self.grid.is_cell_empty((x, y)):
               self.grid.place_agent(agent, (x, y))
               return
            attempt += 1

         # If an empty cell is not found, expand the grid size
        print("Attempting to expand grid...")  # Debug print
        self.expand_grid()
        self.place_agent_randomly(agent)  # Retry placing the agent

    def expand_grid(self):
        print("Expanding grid...")  # Debug print

        # Determine the new size; here we're increasing by a fixed amount
        new_width = self.grid.width + 10
        new_height = self.grid.height + 10

        # Create a new grid with the new size
        new_grid = MultiGrid(new_width, new_height, True)

        # Transfer agents from the old grid to the new grid
        for cell in self.grid.coord_iter():
            cell_content, (x, y) = cell  # Corrected unpacking
            for agent in cell_content:
                new_grid.place_agent(agent, (x, y))

        # Replace the old grid with the new grid
        self.grid = new_grid

    def calculate_global_average_plan(self):
        total_plan = sum(agent.plan for agent in self.schedule.agents)
        return total_plan / len(self.schedule.agents) if self.schedule.agents else 0

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
        self.total_steps += 1

        self.update_matched_proposals()
        self.check_proposal_equilibrium()
        self.check_thresholds_and_windows()

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

    def update_matched_proposals(self):
        matched_proposals = 0
        for cell_contents in self.grid.coord_iter():
            agents = cell_contents[0]
            if any(isinstance(agent, WorkersCouncilAgent) for agent in agents) and \
               any(isinstance(agent, ConsumersCouncilAgent) for agent in agents):
                matched_proposals += 1
        self.matched_proposals_history.append(matched_proposals)

    def check_proposal_equilibrium(self):
        if self.total_steps > 1:  # Avoid division by zero
            matched_ratio = self.matched_proposals_history[-1] / self.total_steps
            if matched_ratio >= 0.9:  # 90% matched proposals
                print(f"Proposal Equilibrium reached at step {self.total_steps}")

    def check_thresholds_and_windows(self):
        worker_proposals = sum(agent.plan for agent in self.schedule.agents if isinstance(agent, WorkersCouncilAgent))
        consumer_proposals = sum(agent.plan for agent in self.schedule.agents if isinstance(agent, ConsumersCouncilAgent))
        proposal_diff = abs(worker_proposals - consumer_proposals)

        if len(self.matched_proposals_history) >= max(self.num_workers_councils, self.num_consumers_councils):
            if proposal_diff <= worker_proposals * 0.2:  # 20% threshold
                print(f"Threshold and Stability Window reached at step {self.total_steps}")

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

        print(f"Step: {self.schedule.steps},")
        print(f"Number of Workers' Councils: {self.num_workers_councils},")
        print(f"Number of Consumers' Councils: {self.num_consumers_councils},")
        print(f"Worker Adjustment: {self.worker_adjustment},")
        print(f"Consumer Adjustment: {self.consumer_adjustment},")
        print(f"Matched Proposals This Step: {matched},")
        print(f"Unmatched Consumer Proposals This Step: {unmatched_consumers},")
        print(f"Unmatched Worker Proposals This Step: {unmatched_workers},")
        print(f"Total Matched Proposals: {self.total_matched_proposals},")
        print(f"Total Unmatched Proposals: {self.total_unmatched_proposals},")
        # COMMENTED OUT AS OUTPUTS DUPLICATE DATA:  print(f"Proposal History: {self.proposal_history}")
        print(f"Acceptable Proposal Difference: {self.acceptable_proposal_difference},")
        print(f"Stability Window: {self.stability_window},")
        print(f"Minimal Unmatched Threshold: {self.min_unmatched_threshold}")
        # Commented out till overall eqaulibrium is refined.
        # if self.time_to_equilibrium is not None:
        #    print(f"Time to overall equilibrium: {self.time_to_equilibrium} steps",)
        # else:
        #    print("Overall equilibrium not yet reached.")
        print("-----------------------------------")

        # For printing to stdout, you can print your desired output here
        # Example:
        # COMMENTED OUT AS OUTPUTS DUPLICATE DATA:
        # matched, unmatched_consumers, unmatched_workers = self.proposals_status()
        # print(f"Step {self.schedule.steps}: Matched: {matched}, Unmatched Consumers: {unmatched_consumers}, Unmatched Workers: {unmatched_workers}")

# Function to run the model with command-line arguments
def run_model(args):
    print("Running model...")  # Debug print
    model = CouncilBasedEconomyModel(
        num_workers_councils=args.num_workers_councils,
        num_consumers_councils=args.num_consumers_councils,
        worker_adjustment=args.worker_adjustment,
        consumer_adjustment=args.consumer_adjustment,
        acceptable_proposal_difference=args.acceptable_proposal_difference,
        stability_window=args.stability_window,
        min_unmatched_threshold=args.min_unmatched_threshold
    )

    for _ in range(args.num_steps):
        model.step()

# Main script execution
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Council Based Economy Model")
    parser.add_argument("--num_workers_councils", type=int, default=100)
    parser.add_argument("--num_consumers_councils", type=int, default=100)
    parser.add_argument("--worker_adjustment", type=int, default=10)
    parser.add_argument("--consumer_adjustment", type=int, default=10)
    parser.add_argument("--acceptable_proposal_difference", type=int, default=20)
    parser.add_argument("--stability_window", type=int, default=200)
    parser.add_argument("--min_unmatched_threshold", type=int, default=10)
    parser.add_argument("--num_steps", type=int, default=100, help="Number of steps to run the model")

    args = parser.parse_args()
    run_model(args)
