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

# Aggregate data and save to CSV
df = aggregate_data("simulation_outputs")
df.to_csv("output_aggregated_data.csv", index=False)
