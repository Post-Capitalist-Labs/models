### About our bulk simulations

The Simple Council Economy model now includes powerful tools for conducting bulk simulations, allowing users to explore a wide range of scenarios and parameter combinations. This suite of tools is designed to facilitate large-scale analysis, offering insights into the dynamics and potential outcomes of different council-based economic scenarios.

However, the potential number of simulations, given the parameter ranges defined by the model's sliders, reaches approximately 6.6 trillion combinations, making exhaustive exploration impractical. 
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

Running a comprehensive simulation for every possible combination of parameters in the given ranges is indeed impractical due to the sheer number of simulations required. To meaningfully explore the range of possibilities without running an unfeasibly large number of simulations, we provide scripts for a variety of simulaitons:
- a basic simulation (`basic_simulation.py`): A script that automates iterations through predefined ranges of six key parameters, number of worker and consumer councils, worker and consumer adjustment values, acceptable proposal difference, stability window, and minimal unmatched threshold—executing the `council_economy.py` script for each unique set of parameters. This allows for comprehensive exploration and analysis of the model's behavior under different conditions.
- an optimal balance simulation (`optimal_balance.py`): This script is designed to execute simulations focusing specifically on finding an optimal balance within a narrower range of parameters. It targets simulations by varying the number of worker and consumer councils within specified increments, while keeping other parameters like worker and consumer adjustment values, acceptable proposal difference, stability window, and minimal unmatched threshold at constant or moderately varied levels. This approach allows for a concentrated exploration of parameter spaces that are hypothesized to offer the most balanced or efficient outcomes, aiding in the identification of optimal settings for the model's performance.
- scenario analysis simulations (`scenario_analysis.py`): This script is tailored for running a variety of predefined scenarios, each with a specific set of base parameters to simulate different economic conditions. For each scenario, it iterates multiple times, slightly varying the parameters around the base values to explore the outcomes under slightly different conditions. This approach allows for a more nuanced analysis of how small changes in parameters can impact the model's behavior. This structured approach facilitates a comprehensive exploration of different economic dynamics, such as baseline conditions, high or low activity levels, tolerance to proposal mismatches, and crisis situations, thereby providing valuable insights into the model's response to various economic environments.

Scenario analysis can be particularly effective in focusing simulations on relevant and insightful aspects of the model. Here are a few scenario-based approaches to in our script, tailored to the parameters of the Council Based Economy Model:

Baseline Scenario:
This scenario would use the default or most common settings for each parameter. It serves as a reference point to understand the model's behavior under typical conditions.

Example: 100 Worker and Consumer Councils each, Worker Adjustment 10, Consumer Adjustment 10, Acceptable Proposal Difference 20, Stability Window 200, Minimal Unmatched Threshold 10.

High Activity Scenario:
A scenario where both worker and consumer councils are at their maximum, representing a highly active and dynamic economy.
Example: 200 Worker and Consumer Councils each, higher Worker and Consumer Adjustments (e.g., 15 or 20), and a wider Stability Window (e.g., 300 or 400).

Low Activity Scenario:
Here, the model operates with minimal councils and adjustments, simulating a less dynamic economy or a starting phase.
Example: 50 Worker and Consumer Councils each, lower Worker and Consumer Adjustments (e.g., 5), and a shorter Stability Window (e.g., 100).

High Tolerance for Mismatch:
This scenario explores the effects of a higher threshold for acceptable proposal differences and unmatched proposals, which might simulate a more tolerant or flexible economy.

Example: Standard number of councils, with higher Acceptable Proposal Difference (e.g., 40 or 50) and higher Minimal Unmatched Threshold (e.g., 15 or 20).

Low Tolerance for Mismatch:
Opposite to the above, this scenario represents a more rigid economy with low tolerance for mismatch.

Example: Standard number of councils, with lower Acceptable Proposal Difference (e.g., 10) and lower Minimal Unmatched Threshold (e.g., 5).
Crisis Scenario:

Designed to simulate economic stress or crisis conditions, perhaps by creating a large disparity between worker and consumer councils, or extreme adjustment values.

Example: A significant imbalance in the number of Worker and Consumer Councils (e.g., 150 workers vs. 50 consumers), with extreme values for adjustments.

Optimal Balance Search:
This scenario attempts to find the optimal balance between different parameters for the most stable and efficient economy.

Example: Gradually adjust the number of councils and other parameters to find a combination where the system reaches equilibrium fastest or operates most efficiently.

By running these scenarios, you can gain insights into how different aspects of the economic model behave under various conditions. These insights can be useful for understanding the dynamics of the model, identifying key drivers, and making informed decisions or predictions based on the model's outcomes.

### How to use our tooling for bulk simulations
1. From the the `council_economy` folder, run the bash script for the scenario of your choice, for example: `bash ./tests/basic_simulation.sh`. This will generate output files for each simulation run in the `simulation_outputs` directory.
2. Run the Python script `python3 aggregate_data.py`: This script is designed to compile and organize simulation data from multiple text files into a single, structured CSV file for easier analysis. To do so you must edit `aggregate_data.py` and uncomment the lins according to data you want aggregated, and also do the same for the CSV filename you want it to output:
```
# Uncomment according to data you want aggregated.
# df = aggregate_data("simulation_outputs")
df = aggregate_data("simulation_outputs/Baseline")
# df = aggregate_data("simulation_outputs/Crisis")

# Dump data to CSV
# Uncomment according to filename.
# df.to_csv("simulation_outputs/output_aggregated_data.csv", index=False)
df.to_csv("simulation_outputs/Baseline_data.csv", index=False)
# df.to_csv("simulation_outputs/Crisis_data.csv", index=False)
```

3. `aggregate_data.py` works by reading each text file within a specified directory (e.g., for different simulation scenarios like Baseline, Crisis, High Activity, etc.), extracting key-value pairs of simulation parameters and results, and then aggregating this data into a pandas DataFrame. This DataFrame is then exported as a CSV file, named according to the scenario it represents, facilitating a comprehensive and consolidated view of the simulation outcomes. This process enables efficient and systematic analysis of the model's behavior across a range of conditions, supporting in-depth exploration and understanding of the simulated council-based economy dynamics.

You can also run the council_economy.py script from the command line with specific parameters. For example:
`python council_economy.py --num_workers_councils 100 --num_consumers_councils 100 --worker_adjustment 10 --consumer_adjustment 10 --acceptable_proposal_difference 20 --stability_window 200 --min_unmatched_threshold 10 --num_steps 100`

### Call to Action: Use our models, share your data!

We would love for you to share the data you produce with our models. Here are ideas for other types of analysis:

1. **Random Sampling**: Randomly select a set number of parameter combinations to simulate. This method ensures a broad, unbiased coverage across the parameter space but may miss some specific combinations of interest.

2. **Stratified Sampling**: Divide the parameter space into distinct strata or segments and randomly sample within each stratum. This ensures that each part of the parameter space is represented, allowing for a more systematic exploration than purely random sampling.

3. **Latin Hypercube Sampling**: This statistical method samples points in such a way that each parameter is evenly sampled across its range. This provides a more efficient and representative sampling of the parameter space compared to simple random sampling.

4. **Design of Experiments (DoE)**: Techniques like factorial design, fractional factorial design, or response surface methodology can be used. They provide structured approaches to explore interactions between parameters systematically. For example, a fractional factorial design can reduce the number of required simulations significantly while still capturing the main effects and interactions of the parameters.

5. **Adaptive Sampling**: Begin with a broad, sparse sampling across the parameter space. Analyze these initial results to identify regions of interest or unusual behavior, and then focus more detailed sampling in these areas.

6. **Sensitivity Analysis**: Identify which parameters have the most significant impact on the simulation outcomes. Focus on sampling more densely around different values of these key parameters, while less critical parameters can be sampled more sparsely.

7. **Scenario Analysis**: Instead of sampling across the entire range, focus on certain plausible or interesting scenarios. Define these scenarios based on combinations of parameters that are of particular interest or relevance to the research questions or practical applications.

8. **Combining Techniques**: Often, a combination of the above methods yields the best results. For instance, you could use Latin Hypercube Sampling to get a broad overview and then apply sensitivity analysis to focus on key parameters.

Each method has its advantages and limitations, and the choice depends on the specific goals of your simulation, the computational resources available, and the nature of the system being modeled.

