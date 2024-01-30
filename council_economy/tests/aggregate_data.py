import os
import pandas as pd

def extract_data_from_file(file_path):
    data = {}
    with open(file_path, 'r') as file:
        for line in file:
            if ':' in line:
                key, value = line.split(':', 1)
                data[key.strip()] = value.strip()
    return data

def aggregate_data(directory):
    all_data = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            file_data = extract_data_from_file(file_path)
            all_data.append(file_data)

    df = pd.DataFrame(all_data)
    return df

# Aggregate data.
# Uncomment according to data you want aggregated.
# df = aggregate_data("simulation_outputs")
df = aggregate_data("simulation_outputs/Baseline")
# df = aggregate_data("simulation_outputs/Crisis")
# df = aggregate_data("simulation_outputs/High_Activity")
# df = aggregate_data("simulation_outputs/High_Tolerance_Mismatch")
# df = aggregate_data("simulation_outputs/Low_Activity")
# df = aggregate_data("simulation_outputs/Low_Tolerance_Mismatch")
# df = aggregate_data("simulation_outputs/Optimal_Balance_Search")

# Dump data to CSV
# Uncomment according to filename.
# df.to_csv("simulation_outputs/output_aggregated_data.csv", index=False)
df.to_csv("simulation_outputs/Baseline_data.csv", index=False)
# df.to_csv("simulation_outputs/Crisis_data.csv", index=False)
# df.to_csv("simulation_outputs/High_Activity_data.csv", index=False)
# df.to_csv("simulation_outputs/High_Tolerance_Mismatch_data.csv", index=False)
# df.to_csv("simulation_outputs/Low_Activity_data.csv", index=False)
# df.to_csv("simulation_outputs/Low_Tolerance_Mismatch_data.csv", index=False)
# df.to_csv("simulation_outputs/Optimal_Balance_Search_data.csv", index=False)
