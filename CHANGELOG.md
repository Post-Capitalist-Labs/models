# Changelog

## [v0.02] - 02/10/2024

### Added
- **Bulk Simulation Tools**: Introduced tools for running bulk simulations and aggregating results, enhancing the model's capability for large-scale analysis.
- **Equilibrium Tracking**: New attributes in agents for tracking time to equilibrium in various forms, providing a more nuanced understanding of economic dynamics.
- **Dynamic Proposal Adjustment Logic**: Enhanced the logic for agents adjusting their proposals, including a learning factor based on past encounters.
- **Guidance on Sampling Methods**: Included recommendations for efficient sampling methods to explore the parameter space without the need for running an impractical number of simulations.
- **Repository Data for Analysis**: Added initial data from bulk scenario simulations to the repository for user analysis.
- **Contribution Encouragement**: Encouraged users to contribute their own bulk simulation data and findings.

### Improved
- **Feedback Mechanisms**: Strengthened the feedback loop in proposal adjustments, allowing agents to refine their future proposals based on past performance.
- **Simulation Control**: Enhanced control over the simulation through improved equilibrium tracking and feedback mechanisms.

### Changed
- **Documentation**: Updated the README.md to include detailed instructions on using the new bulk simulation tools and contributing to the project.

## [v0.01] - 12/2023

### Added
- **Agent Classes**: Introduced `WorkersCouncilAgent` and `ConsumersCouncilAgent` for representing workers' and consumers' councils.
- **Model Class - CouncilBasedEconomyModel**: Established the simulation environment, including configurable parameters and agent interactions.
- **Dynamic Agent Behavior**: Enabled agents to move within a grid and adjust their proposals dynamically.
- **Data Collection**: Utilized Mesa's `DataCollector` for tracking key metrics like total production and consumption proposals.
- **Simulation Control**: Implemented a model that runs until all proposals are matched, with a text-based visualization of key metrics after each step.
- **Technical Implementation**: Employed `RandomActivation` and `MultiGrid` from Mesa for agent activation and environment representation.

### Use Cases
- Outlined the model's applicability for economic simulations and educational purposes.

### Requirements
- Specified Python 3.x and Mesa package as prerequisites.

### Installation
- Provided instructions for cloning the repository and installing necessary dependencies.
