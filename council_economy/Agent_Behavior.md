## How do agents make their choices?

There are several factors influencing how council agent's alter their proposals and why. Let's break this down to understand how it works:

1. Learning Factor Adjustment
   - The `calculate_learning_factor` method is called to determine the learning factor based on past encounters.
   - The current proposal (`self.plan`) is adjusted towards the global average proposal, scaled by the learning factor.

2. Moving Towards Global Average
   - After applying the learning factor, the agent's plan is averaged with the global average plan. This represents a tendency to move towards the average proposal value in the model.

3. Random Fluctuation
   - A random fluctuation (between -5 to +5) is added to introduce some variability and prevent the system from becoming too deterministic.

4. Target Plan Calculation
   - The `calculate_target_plan` method computes a target plan based on the average of previously encountered proposals, aiming for less than 5 proposals per agent.

5. Adjustment Based on Distance to Target
   - The agent calculates the distance between its current plan and the target plan, and between its plan and the global average.
   - Based on these distances, an adjustment factor is determined (maximum of 1 and one-fourth of the distance to the target).

6. Adjustment Based on Encounter Outcome
   - If the agent met an unmatched agent in the previous step (`self.met_unmatched` is `True`), it increases its plan by the adjustment factor; otherwise, it decreases its plan by this factor.

7. Feedback Mechanism
   - An additional adjustment is made based on whether the agent met an unmatched agent. This is calculated by the `calculate_feedback_adjustment` method, which likely considers the history of successes and failures in matching proposals.

8. Clamping the Proposal Value
   - Finally, the proposal (`self.plan`) is clamped to ensure it stays within the specified minimum and maximum values.
