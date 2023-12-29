![ALT](/simple-council-economy-mesa-model/-/raw/main/assets/Screenshot_2023-12-29_at_22.26.55.png)

# How to run this model

1. Make sure your local environment has these resources installed:
- Python 3.12.1 or higher
- Mesa

2. Clone this respo
3. `cd`into `council_economy`
4. Run the cmd `mesa runserver` 


Upon running you will see: 
- a browser based interactive model running on `http://127.0.0.1:8521/` 
 - terminal logs output from `text_visualization`: 
```-----------------------------------
{"type":"get_step","step":856}
Step: 856
Number of Workers Councils: 100
Number of Consumers Councils: 91
Worker Adjustment: 10
Consumer Adjustment: 10
Matched Proposals This Step: 22
Total Matched Proposals: 15279
Unmatched Consumer Proposals This Step: 68
Unmatched Worker Proposals This Step: 76
Total Unmatched Proposals: 129293
Equilibrium not yet reached.
-----------------------------------
```
To contribute fork this repo and submit a pull request with your changes.

# About this model

 A simple council-based economy model comprising worker and consumer councils. Each council will make proposals regarding production and consumption, and the model will iterate these proposals until a balance is achieved between supply and demand. We'll set up 100 workers' councils and 100 consumers' councils as specified.

- **WorkersCouncilAgent** and **ConsumersCouncilAgent**:
  - Each starts with a random initial proposal for production and consumption, respectively.
- **Adjustment Process**:
  - In each step, agents adjust their plans based on simplified logic, such as random adjustments in this example.
  - For a more detailed model, adjustments would involve complex interactions based on actual economic factors.
- **Model Execution**:
  - The model runs for a specified number of steps.
  - After each step, it prints the total production and consumption across all councils.
  - In a more complex version, the iteration would continue until the total production closely matches the total consumption.
- **Framework and Realism**:
  - This code serves as a foundational framework.
  - To enhance realism, detailed mechanisms for proposal adjustment based on feedback from the other type of council need to be implemented.
- **Mesa Model and Future Development**:
  - This Mesa model provides a basic simulation of the proposed council-based economy.
  - It allows for further complexity and detail to be added as needed.


## Ways to use this model
To effectively challenge and validate this model of a council-based economy, where workers and consumers democratically plan production and consumption without a central authority or market mechanisms, you can experiment with various parameters and scenarios. The goal is to explore how different conditions affect the efficiency and viability of such an economy. Here are several approaches to consider:

### 1. Adjusting Adjustment Factors
- **Varying Adjustment Levels**: Experiment with different ranges for `worker_adjustment` and `consumer_adjustment`. These adjustments simulate the degree of flexibility or responsiveness in production and consumption plans. Test scenarios with very rigid plans (small adjustments) and very flexible plans (large adjustments) to observe how this impacts the time taken to reach an equilibrium.
- **Asymmetric Adjustments**: Try scenarios where one group (either workers or consumers) is more flexible than the other. This could simulate real-world scenarios where, for example, consumer demand is more volatile than production capacity.

### 2. Changing the Number of Councils
- **Scale Variations**: Test how the model behaves with different numbers of workers' and consumers' councils. A larger number of councils could represent a more decentralized economy. Observe how this decentralization impacts the time taken to reach a consensus.
- **Imbalance in Council Numbers**: Create scenarios where the number of workers' councils significantly differs from the number of consumers' councils. This could highlight challenges in coordination and agreement when one side of the economic equation is more heavily represented than the other.

### 3. Introducing External Influences
- **Random Events**: Introduce random events that could affect production or consumption plans, like natural disasters, technological breakthroughs, or changes in consumer preferences. This can test the resilience and adaptability of the council-based model.
- **Gradual Changes**: Implement gradual changes in the environment, like slowly increasing consumer preferences for certain goods, to see if the councils can adapt over time.

### 4. Analyzing Different Metrics
- **Time to Equilibrium**: Measure how long it takes for production and consumption proposals to match. This is a direct measure of the efficiency of the economic planning process.
- **Stability Over Time**: Run the simulation for extended periods even after the first equilibrium is reached to observe the stability of the economic plan. Frequent mismatches after achieving initial equilibrium could indicate a lack of sustainability.

### 5. Scenario Simulations
- **Crisis Scenarios**: Simulate economic crises, such as sudden drops in production capabilities or spikes in consumer demand, to test the robustness of the council-based system.
- **Comparative Analysis**: Run the council-based model against a simulated market-based or centrally planned model under identical conditions. This comparative approach can provide insights into the relative strengths and weaknesses of each system.

### 6. Parameter Sweeps
- **Systematic Variation**: Perform parameter sweeps where you systematically vary key parameters (like the number of councils, adjustment levels, etc.) and observe the outcomes. This can help identify thresholds or tipping points in the model’s behavior.

### 7. Visualization and Data Analysis
- **Visualization Tools**: Utilize different visualization tools to observe the dynamics of the model over time. Heatmaps, time-series graphs, and network diagrams can provide valuable insights.
- **Statistical Analysis**: Apply statistical analysis to the simulation data to understand trends, correlations, and variability in the model’s performance under different conditions.

### 8. Incorporating Feedback Mechanisms
- **Learning Algorithms**: Implement simple learning algorithms for agents to adjust their behavior based on past experiences. This could simulate learning and adaptation within councils.

### Conclusion
By exploring these different approaches, you can challenge this model under a variety of conditions and gain a deeper understanding of the dynamics and feasibility of a council-based economic system. The key is to identify parameters that significantly impact the model's behavior and explore their implications in depth.
