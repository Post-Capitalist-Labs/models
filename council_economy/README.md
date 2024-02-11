https://github.com/Post-Capitalist-Labs/models/assets/58642686/6b5a610b-24f4-495d-bb47-b8ad5fdee311

# Simple Council Economy Model v0.02

The Simple Council Economy model `v0.02` builds on the foundational framework introduced in `v0.01`, maintaining the concept of worker and consumer councils that make proposals regarding production and consumption. This version incorporates enhanced feedback mechanisms and equilibrium tracking features to more closely simulate the dynamics of a council-based economy. The model iterates these proposals towards achieving a balance between supply and demand, reflecting a more nuanced approach to reaching equilibrium. Finally, this version delivers a powerful suite of bulk simulation tools capable of generating big data analysis of the Council Economy Model, details below.

## Enhanced Features in v0.02

- **Feedback Mechanism Improvements**: Agents now incorporate a more sophisticated feedback loop in their proposal adjustments, taking into account their past encounters to refine future proposals.
- **Equilibrium Tracking**: Additional attributes track the time to reach various forms of equilibrium, such as balanced proposals, matched versus unmatched proposals, and stability in adjustments. This allows for a deeper analysis of the model's dynamics over time.
- **Improved Proposal Adjustment Logic**: The logic for adjusting proposals has been refined, including a learning factor based on past encounters and a more dynamic adjustment mechanism that responds to the distance from target plans and global averages.

## Model Components

- **`CouncilAgent`**: Represents both worker and consumer councils, each starting with a random initial proposal.
- **`WorkersCouncilAgent`** and **`ConsumersCouncilAgent`**: Subclasses of `CouncilAgent` with specific initial proposal ranges and step functions.
- **`CouncilBasedEconomyModel`**: The main model class that initializes the agents and runs the simulation, tracking the overall state of the economy.

## How to Use This Model

To explore the dynamics of a council-based economy and test its efficiency and viability under various conditions, you can adjust parameters and introduce different scenarios:

### Running the Model

1. Ensure Python 3.12.1 or higher and Mesa are installed in your environment.
2. Clone the repository and navigate to the `council_economy` directory.
3. Execute `mesa runserver` in your command line.

### Interactive Model and Visualization

Upon running, you'll access:
- A browser-based interactive model at `http://127.0.0.1:8521/`.
- Terminal logs output from `text_visualization`, providing detailed insights into each simulation step.

### Experimentation Suggestions

- **Adjust Proposal Adjustments**: Modify the range and logic of adjustments to explore different equilibrium dynamics.
- **Vary Council Numbers**: Test the model with different numbers of worker and consumer councils to analyze effects on decentralization and consensus time.
- **Introduce External Factors**: Simulate random events or gradual changes in the environment to assess the model's resilience.
- **Analyze Stability and Efficiency**: Measure the time to equilibrium and the stability of economic plans over extended periods.

## New Bulk Simulation Tools

The Simple Council Economy model now includes powerful tools for conducting bulk simulations, allowing users to explore a wide range of scenarios and parameter combinations. This suite of tools is designed to facilitate large-scale analysis, offering insights into the dynamics and potential outcomes of different council-based economic scenarios.

The potential number of simulations, given the parameter ranges defined by the model's sliders, reaches approximately 6.6 trillion combinations, making exhaustive exploration impractical. To address this, we have designed scenario analysis scripts other efficient sampling methods to explore the parameter space meaningfully without running an unfeasibly large number of simulations.

## Link to Full Text on Bulk Simulation Tools

For detailed information on how to utilize the bulk simulation tools effectively, including examples of specific scenarios and sampling techniques, [please refer to the full text in the  tests README.md document](tests/README.md).

The addition of bulk simulation tools to the Simple Council Economy model v0.02 opens up new avenues for comprehensive analysis and exploration of council-based economic systems. By leveraging these tools, researchers and enthusiasts can gain deeper insights into the viability and efficiency of such systems under a wide range of conditions. We look forward to seeing the community's contributions and insights as we continue to develop and refine this model.

## Contributing Your Simulations

We encourage users to run their own bulk simulations and analysis. The repository [includes data from bulk scenario simulations for initial exploration](tests/simulation_outputs). However, users are invited to share their own data and insights, which could potentially be added to the project. If you use our bulk simulation tools, we would love to see your data and analysis.

## Related Reading: Our Writings
- [How Democracy Can Be Revitalized With an Ancient Twist and a Tech Upgrade: A Peek Into the Future](https://hackernoon.com/how-democracy-can-be-revitalized-with-an-ancient-twist-and-a-tech-upgrade-a-peek-into-the-future)
- [Revisiting Chaulieu’s Workers’ Councils and the Economics of a Self-Managed Society](https://aorb.info/index.php/category/pamphlets/2023/12/28/revisiting-self-managed-society/index.html/)
- [Decentralized Horizons: Empowering a Participatory Economy with Blockchain and AI](https://delegate0x.substack.com/p/decentralized-horizons-empowering)
- See also our ongoing series: [A Post-Capitalist Critique of Cryptoeconomics](https://github.com/Post-Capitalist-Labs/publications/blob/main/README.md#our-series-developing-a-post-capitalist-cryptoeconomics)

### Contribution

Fork this repository and submit a pull request with your enhancements or fixes to contribute to the model's development.

## Conclusion

The Simple Council Economy model v0.02 offers a more complex simulation environment for studying the feasibility and dynamics of a council-based economic system. By adjusting parameters and introducing new scenarios, researchers and enthusiasts can gain insights into the potential of such an economy to adapt and thrive under various conditions.
