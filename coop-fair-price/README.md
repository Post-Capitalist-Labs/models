![](https://github.com/Post-Capitalist-Labs/models/blob/main/coop-fair-price/assets/Screenshot%202024-01-10%20at%2009.50.29.png?raw=true)
<i>Screenshot: Node colors represent the co-op's economic status with red for economically advantaged, yellow for under-resourced, and green for equitable distribution. The size of the node indicates the economic advantage level, with larger nodes representing more advantaged co-ops.</i>

# Equitable Pricing Formula in a Cooperative Economy

This model simulates an equitable pricing formula in an economy of cooperatives, inspired by Economist Robin Hahnel's work "[Reducing Inequities among Worker-Owned Cooperatives: A Proposal](http://www.jstor.org/stable/20642477)". It aims to redistribute surplus among worker-owned cooperatives to reduce inequities and maintain balance within the community.

## Definitions

- `C_p`: Production cost for a co-op.
- `P_m`: Market price in a competitive market without equity adjustments.
- `S`: Surplus, calculated as `P_m - C_p`.
- `REA%`: Relative Economic Advantage percentage, a metric used to measure the economic position of a cooperative relative to others within the same market or ecosystem.
- `α (alpha)`: Redistribution rate for the surplus.
- `E`: Equity adjustment amount.

## The Formula

`P_e = P_m + E`, where `E` depends on the co-op's `REA%`:

- Co-ops with `REA% < 100` charge more for additional support.
- Co-ops with `REA% > 100` reduce their price to redistribute benefits.
- Co-ops with `REA% = 100` charge the market price `P_m`.

## Model Implementation

The model uses the Mesa framework in Python and includes:

- **Agents**: Represent co-op enterprises.
- **Market**: For transactions.
- **Scheduler**: Controls event sequence.
- **DataCollector**: Gathers and reports data.

### Node Colors and Sizes

- **Red Nodes**: Indicate economically advantaged co-ops. They have achieved a higher equitable price due to their surplus and redistribution settings.
- **Yellow Nodes**: Represent under-resourced co-ops, which sell below the equitable distribution threshold.
- **Green Nodes**: Signify co-ops in equitable distribution, positioned closely around the market price `P_m`.
- **Node Sizes**: Larger nodes represent more economically advantaged co-ops, determined by whether their equitable price exceeds a set threshold.

## Sliders

- **Number of Co-ops (N)**: Adjusts the total number of cooperative agents in the simulation.
- **Production Cost**: Sets the base cost of production for goods/services across co-ops.
- **REA Percent**: Determines the relative economic advantage/disadvantage percentage.
- **Market Price**: Controls the base market price before equity adjustments.
- **Alpha Value**: Adjusts the rate of surplus redistribution among co-ops.

## Running the Model

1. Install Python 3.12.1+ and Mesa.
2. Clone the repository.
3. Navigate to `coop-fair-price`.
4. Execute `mesa runserver`.

Access the interactive model at `http://127.0.0.1:8521/`.

## Conclusion

This model provides a foundational approach to fostering equity within cooperative economies, ensuring community members can thrive regardless of their economic standing.
