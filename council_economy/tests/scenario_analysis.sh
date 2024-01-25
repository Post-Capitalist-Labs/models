#!/bin/bash

# Define ranges for parameters
num_workers_councils_range=(50 100 200)
num_consumers_councils_range=(50 100 200)
worker_adjustment_range=(5 10 20)
consumer_adjustment_range=(5 10 200)
acceptable_proposal_difference_range=(10 20 50)
stability_window_range=(100 250 500)
min_unmatched_threshold_range=(5 10 20)


# Function to run the simulation with specified parameters
run_simulation() {
    output_dir="tests/simulation_outputs/$8"
    mkdir -p $output_dir
    filename="${output_dir}/sim_${1}_${2}_${3}_${4}_${5}_${6}_${7}.txt"
    echo "Running $8 with parameters: $1 $2 $3 $4 $5 $6 $7"
    python3 council_economy.py --num_workers_councils $1 --num_consumers_councils $2 --worker_adjustment $3 --consumer_adjustment $4 --acceptable_proposal_difference $5 --stability_window $6 --min_unmatched_threshold $7 > $filename
}

# 1. Baseline Scenario
run_simulation 100 100 10 10 20 200 10 "Baseline"

# 2. High Activity Scenario
run_simulation 200 200 20 20 30 400 15 "High_Activity"

# 3. Low Activity Scenario
run_simulation 50 50 5 5 10 100 5 "Low_Activity"

# 4. High Tolerance for Mismatch
run_simulation 100 100 10 10 50 300 20 "High_Tolerance_Mismatch"

# 5. Low Tolerance for Mismatch
run_simulation 100 100 10 10 10 200 5 "Low_Tolerance_Mismatch"

# 6. Crisis Scenario
run_simulation 150 50 25 25 20 300 10 "Crisis"

# 7. Optimal Balance Search
# Example range - Adjust as needed
for worker_count in {75..125..25}; do
    for consumer_count in {75..125..25}; do
        run_simulation $worker_count $consumer_count 10 10 20 200 10 "Optimal_Balance_Search"
    done
done
