# Frequently Asked Questions (WIP)

### Q. What causes the simulation to stop running?

### A. In the provided code from the CouncilBasedEconomyModel class, the simulation stops running when a specific condition is met, as determined by the step method of the model. This condition is checked in the all_proposals_matched method. Here's how it works:

#### `all_proposals_matched` Method
This method checks whether all proposals have been matched across the entire grid. It iterates over each cell in the grid and looks for cells containing agents.

If a cell contains agents of both types (`WorkersCouncilAgent` and `ConsumersCouncilAgent`), it implies that proposals in that cell are matched, and the method continues checking other cells.

If any cell is found with only one type of agent or no agents at all, it means not all proposals have been matched, and the method returns False.

#### Stopping the Simulation
The simulation's main loop is governed by the step method. Within this method, after each step of the simulation (which involves updating agents and collecting data), the `all_proposals_matched` method is called.

If `all_proposals_matched` returns `True`, indicating that all proposals across the grid are matched, the running attribute of the model is set to `False`.

The setting of `self.running = False` acts as a signal for the simulation to stop running. This typically happens in agent-based models where the simulation is designed to run until a certain condition is met.

#### In Summary
The simulation in your `CouncilBasedEconomyModel` stops running when the `all_proposals_matched` method returns `True`, indicating that every cell in the grid either has matched proposals (both workers' and consumers' agents present) or is empty. This condition is meant to represent a state where all economic proposals have been successfully matched, fulfilling the simulation's primary objective.

### Q. What does it mean when the simulation stops with unmatched proposals?

### A. If the simulation in your CouncilBasedEconomyModel stops while there are still unmatched proposals, it implies that the model has reached a state where it can no longer proceed under the given rules and conditions, yet it has not achieved a complete matching of all proposals. This outcome can be significant and may indicate several things about the model or the scenario being simulated:

#### 1. Inherent System Limitations:
- Inefficiency in Coordination: The inability to match all proposals might reflect a limitation in the model's representation of coordination or negotiation processes between worker and consumer councils.

- Model Constraints: The rules and mechanisms defined in the model might not be sufficient to facilitate a complete match under certain conditions.

#### 2. Scenario-Specific Challenges:
- Complex Dynamics: In real-world terms, this could represent a situation where the economic system fails to meet the demands or production capabilities fully, leading to imbalances or inefficiencies.

- Stagnation or Deadlock: The simulation might be illustrating a scenario where the system reaches a deadlock due to conflicting interests or inflexibilities in proposals.

#### 3. Parameters and Initialization:
- Impact of Initial Parameters: The initial conditions and parameters (like the number of councils, adjustment factors, etc.) might lead to a situation where achieving equilibrium is inherently difficult or impossible.

- Randomness and Agent Behavior: The random elements in agent behavior or initial placement might create scenarios where matching is unattainable due to chance or unfortunate initial conditions.

#### 4. Insights and Implications:
- Need for Additional Mechanisms: This outcome could suggest the necessity for additional mechanisms or rules in the model (such as negotiation or external intervention) to facilitate better coordination and matching, eg something approximating a [Plan Factory](https://aorb.info/index.php/category/pamphlets/2023/12/28/revisiting-self-managed-society/) or [Iteration Facilitation Board](https://en.wikipedia.org/wiki/Facilitation_board), but with the need to minimize bureaucracy as much as possible.

- Reflecting Real-World Complexity: It could also reflect the complexity and challenges of real-world economic planning in a decentralized, council-based system without a central authority or market forces (which have their own tradeoffs) to mediate.

#### Conclusion:
When the simulation stops with unmatched proposals, it offers valuable insights into the limitations and challenges of the simulated economic system. It prompts a closer examination of the model's rules, the impact of initial conditions, and the potential need for more sophisticated mechanisms to achieve equilibrium. This outcome can be a significant part of the learning and analysis process, guiding further refinements to the model or leading to deeper investigations into the dynamics of decentralized economic planning.
