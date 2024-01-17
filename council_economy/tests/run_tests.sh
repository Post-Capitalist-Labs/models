#!/bin/bash

# Call the Python script to set up the Python path
python3 setup_python_path.py

# Define ranges for parameters
num_workers_councils_range=(50 100 150)
num_consumers_councils_range=(50 100 150)
worker_adjustment_range=(5 10 15)
consumer_adjustment_range=(5 10 15)
acceptable_proposal_difference_range=(10 20 30)
stability_window_range=(100 200 300)
min_unmatched_threshold_range=(5 10 15)

# Directory to store output files
output_dir="simulation_outputs"
mkdir -p $output_dir

# Function to run the simulation with specified parameters
run_simulation() {
    filename="${output_dir}/sim_${1}_${2}_${3}_${4}_${5}_${6}_${7}.txt"
    echo "Running simulation with parameters: $1 $2 $3 $4 $5 $6 $7"
    python3 ../council_economy/council_economy.py --num_workers_councils $1 --num_consumers_councils $2 --worker_adjustment $3 --consumer_adjustment $4 --acceptable_proposal_difference $5 --stability_window $6 --min_unmatched_threshold $7 > $filename
}

# Loop through parameter ranges to run simulations
for num_workers in "${num_workers_councils_range[@]}"; do
    for num_consumers in "${num_consumers_councils_range[@]}"; do
        for worker_adj in "${worker_adjustment_range[@]}"; do
            for consumer_adj in "${consumer_adjustment_range[@]}"; do
                for proposal_diff in "${acceptable_proposal_difference_range[@]}"; do
                    for stability_window in "${stability_window_range[@]}"; do
                        for min_unmatched in "${min_unmatched_threshold_range[@]}"; do
                            run_simulation $num_workers $num_consumers $worker_adj $consumer_adj $proposal_diff $stability_window $min_unmatched
                        done
                    done
                done
            done
        done
    done
done
