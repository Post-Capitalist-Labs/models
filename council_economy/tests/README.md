### Instructions:
1. From the the `council_economy` folder, run the bash script `bash ./tests/run_tests.sh`. This will generate output files for each simulation run in the `simulation_outputs` directory.
2. Run the Python script `python3 aggregate_data.py`. This script reads all the output files, aggregates the data, and saves it into a single CSV file `aggregated_data.csv`.

You can also run the council_economy.py script from the command line with specific parameters. For example:
`python council_economy.py --num_workers_councils 100 --num_consumers_councils 100 --worker_adjustment 10 --consumer_adjustment 10 --acceptable_proposal_difference 20 --stability_window 200 --min_unmatched_threshold 10 --num_steps 100`
