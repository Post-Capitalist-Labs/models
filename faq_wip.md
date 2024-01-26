# Frequently Asked Questions (WIP)

### Q. What causes the simulation to stop running?
A. In the provided code from the CouncilBasedEconomyModel class, the simulation stops running when a specific condition is met, as determined by the step method of the model. This condition is checked in the all_proposals_matched method. Here's how it works:

- `all_proposals_matched` Method
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
A. If the simulation in your CouncilBasedEconomyModel stops while there are still unmatched proposals, it implies that the model has reached a state where it can no longer proceed under the given rules and conditions, yet it has not achieved a complete matching of all proposals. This outcome can be significant and may indicate several things about the model or the scenario being simulated:

1. Inherent System Limitations:
- Inefficiency in Coordination: The inability to match all proposals might reflect a limitation in the model's representation of coordination or negotiation processes between worker and consumer councils.

- Model Constraints: The rules and mechanisms defined in the model might not be sufficient to facilitate a complete match under certain conditions.

2. Scenario-Specific Challenges:
- Complex Dynamics: In real-world terms, this could represent a situation where the economic system fails to meet the demands or production capabilities fully, leading to imbalances or inefficiencies.

- Stagnation or Deadlock: The simulation might be illustrating a scenario where the system reaches a deadlock due to conflicting interests or inflexibilities in proposals.

3. Parameters and Initialization:
- Impact of Initial Parameters: The initial conditions and parameters (like the number of councils, adjustment factors, etc.) might lead to a situation where achieving equilibrium is inherently difficult or impossible.

- Randomness and Agent Behavior: The random elements in agent behavior or initial placement might create scenarios where matching is unattainable due to chance or unfortunate initial conditions.

4. Insights and Implications:
- Need for Additional Mechanisms: This outcome could suggest the necessity for additional mechanisms or rules in the model (such as negotiation or external intervention) to facilitate better coordination and matching, eg something approximating a [Plan Factory](https://aorb.info/index.php/category/pamphlets/2023/12/28/revisiting-self-managed-society/) or [Iteration Facilitation Board](https://en.wikipedia.org/wiki/Facilitation_board), but with the need to minimize bureaucracy as much as possible.

- Reflecting Real-World Complexity: It could also reflect the complexity and challenges of real-world economic planning in a decentralized, council-based system without a central authority or market forces (which have their own tradeoffs) to mediate.

#### Conclusion:
When the simulation stops with unmatched proposals, it offers valuable insights into the limitations and challenges of the simulated economic system. It prompts a closer examination of the model's rules, the impact of initial conditions, and the potential need for more sophisticated mechanisms to achieve equilibrium. This outcome can be a significant part of the learning and analysis process, guiding further refinements to the model or leading to deeper investigations into the dynamics of decentralized economic planning.

## Tooling for bulk simulations

### Q. How many simulations would the script have to run to run every possible combination of parameters?
A. To run every possible combination of parameters based on the model's sliders, the script would need to perform approximately 6,638,720,000,000 simulations. 

```python
# Defining the ranges for each parameter based on the sliders
num_workers_councils_range = range(1, 201)  # 1 to 200
num_consumers_councils_range = range(1, 201)  # 1 to 200
worker_adjustment_range = range(1, 21)  # 1 to 20
consumer_adjustment_range = range(1, 21)  # 1 to 20
acceptable_proposal_difference_range = range(5, 51)  # 5 to 50
stability_window_range = range(50, 501)  # 50 to 500
min_unmatched_threshold_range = range(1, 21)  # 1 to 20

# Calculating the total number of simulations by multiplying the number of options for each parameter
total_simulations = (
    len(num_workers_councils_range) *
    len(num_consumers_councils_range) *
    len(worker_adjustment_range) *
    len(consumer_adjustment_range) *
    len(acceptable_proposal_difference_range) *
    len(stability_window_range) *
    len(min_unmatched_threshold_range)
)

total_simulations
```
This is an extremely large number and suggests that exploring every single combination of these parameter ranges would be impractical.

### Q. What would be a more practicle way to sample, survey or spot check the range of possabilities in these simulations?
A. Running a comprehensive simulation for every possible combination of parameters in the given ranges is indeed impractical due to the sheer number of simulations required. To meaningfully explore the range of possibilities without running an unfeasibly large number of simulations, consider the following approaches:

1. **Random Sampling**: Randomly select a set number of parameter combinations to simulate. This method ensures a broad, unbiased coverage across the parameter space but may miss some specific combinations of interest.

2. **Stratified Sampling**: Divide the parameter space into distinct strata or segments and randomly sample within each stratum. This ensures that each part of the parameter space is represented, allowing for a more systematic exploration than purely random sampling.

3. **Latin Hypercube Sampling**: This statistical method samples points in such a way that each parameter is evenly sampled across its range. This provides a more efficient and representative sampling of the parameter space compared to simple random sampling.

4. **Design of Experiments (DoE)**: Techniques like factorial design, fractional factorial design, or response surface methodology can be used. They provide structured approaches to explore interactions between parameters systematically. For example, a fractional factorial design can reduce the number of required simulations significantly while still capturing the main effects and interactions of the parameters.

5. **Adaptive Sampling**: Begin with a broad, sparse sampling across the parameter space. Analyze these initial results to identify regions of interest or unusual behavior, and then focus more detailed sampling in these areas.

6. **Sensitivity Analysis**: Identify which parameters have the most significant impact on the simulation outcomes. Focus on sampling more densely around different values of these key parameters, while less critical parameters can be sampled more sparsely.

7. **Scenario Analysis**: Instead of sampling across the entire range, focus on certain plausible or interesting scenarios. Define these scenarios based on combinations of parameters that are of particular interest or relevance to the research questions or practical applications.

8. **Combining Techniques**: Often, a combination of the above methods yields the best results. For instance, you could use Latin Hypercube Sampling to get a broad overview and then apply sensitivity analysis to focus on key parameters.

Each method has its advantages and limitations, and the choice depends on the specific goals of your simulation, the computational resources available, and the nature of the system being modeled.
