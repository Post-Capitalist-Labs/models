#!/bin/bash

# Function to run the simulation with specified parameters
run_simulation() {
    output_dir="tests/simulation_outputs/$8"
    mkdir -p $output_dir
    filename="${output_dir}/sim_${1}_${2}_${3}_${4}_${5}_${6}_${7}_$9.txt"
    echo "Running $8 with parameters: $1 $2 $3 $4 $5 $6 $7"
    python3 council_economy.py --num_workers_councils $1 --num_consumers_councils $2 --worker_adjustment $3 --consumer_adjustment $4 --acceptable_proposal_difference $5 --stability_window $6 --min_unmatched_threshold $7 > $filename
}

# Function to run scenarios with multiple iterations and specific parameter variations
run_scenarios() {
    scenario_name=$1
    base_num_workers_councils=$2
    base_num_consumers_councils=$3
    base_worker_adjustment=$4
    base_consumer_adjustment=$5
    base_acceptable_proposal_difference=$6
    base_stability_window=$7
    base_min_unmatched_threshold=$8

    for i in {1..10}; do
        # Generate variations around the base parameters for each iteration
        num_workers_councils=$(($base_num_workers_councils + $RANDOM % 20 - 10))
        num_consumers_councils=$(($base_num_consumers_councils + $RANDOM % 20 - 10))
        worker_adjustment=$(($base_worker_adjustment + $RANDOM % 5 - 2))
        consumer_adjustment=$(($base_consumer_adjustment + $RANDOM % 5 - 2))
        acceptable_proposal_difference=$(($base_acceptable_proposal_difference + $RANDOM % 10 - 5))
        stability_window=$(($base_stability_window + $RANDOM % 50 - 25))
        min_unmatched_threshold=$(($base_min_unmatched_threshold + $RANDOM % 5 - 2))

        # Clamp values to prevent them from going below a minimum threshold
        num_workers_councils=$(($num_workers_councils < 1 ? 1 : $num_workers_councils))
        num_consumers_councils=$(($num_consumers_councils < 1 ? 1 : $num_consumers_councils))
        worker_adjustment=$(($worker_adjustment < 1 ? 1 : $worker_adjustment))
        consumer_adjustment=$(($consumer_adjustment < 1 ? 1 : $consumer_adjustment))

        run_simulation $num_workers_councils $num_consumers_councils $worker_adjustment $consumer_adjustment $acceptable_proposal_difference $stability_window $min_unmatched_threshold "${scenario_name}" $i
    done
}

# Run each scenario with its base parameters and iterate through variations
run_scenarios "Baseline" 100 100 10 10 20 200 10
run_scenarios "High_Activity" 200 200 20 20 30 400 15
run_scenarios "Low_Activity" 50 50 5 5 10 100 5
run_scenarios "High_Tolerance_Mismatch" 100 100 10 10 50 300 20
run_scenarios "Low_Tolerance_Mismatch" 100 100 10 10 10 200 5
run_scenarios "Crisis" 150 50 25 25 20 300 10
