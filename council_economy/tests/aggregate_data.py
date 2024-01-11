import pandas as pd
import os
import glob

def aggregate_data(input_folder):
    all_files = glob.glob(os.path.join(input_folder, "*.txt"))
    df_list = []

    for file in all_files:
        data = pd.read_csv(file, sep=" ", header=None)  # Adjust depending on data format
        df_list.append(data)

    combined_df = pd.concat(df_list, ignore_index=True)
    combined_df.to_csv("aggregated_data.csv", index=False)

if __name__ == "__main__":
    aggregate_data("simulation_outputs")
