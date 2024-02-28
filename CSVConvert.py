import os
import json
import pandas as pd
import argparse


def convert_csv(path, output_folder):
    # Get the absolute path to the synthetic data folder
    script_dir = os.path.dirname(__file__)
    synthetic_data_folder = os.path.join(script_dir, f"{path}/synthetic_data")
    output_dir = os.path.join(script_dir, output_folder)

    # Iterate through all JSON files in the synthetic_data_folder
    for filename in os.listdir(synthetic_data_folder):
        if filename.endswith('.json'):
            json_file_path = os.path.join(synthetic_data_folder, filename)

            with open(json_file_path, 'r') as f:
                data = json.load(f)
                df = pd.DataFrame(data)

                # Concatenate values for all columns with list-type values
                for column in df.columns:
                    if df[column].apply(lambda x: isinstance(x, list)).any():
                        df[column] = df[column].apply(lambda x: '|'.join(x) if isinstance(x, list) else x)

                # Save the DataFrame to a CSV file in the output directory
                output_csv_file = os.path.join(output_dir, f"{filename.replace('.json', '.csv')}")
                df.to_csv(output_csv_file, index=False)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--size',
        type=str,
        default='s',
        choices=['s', 'm', 'l'],
        help="Size of the synthetic dataset to convert, options: 's' for small, 'm' for medium, 'l' for large (default: small)"
    )
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    size_mapping = {'s': 'small', 'm': 'medium', 'l': 'large'}
    path = f"{size_mapping[args.size]}_dataset"
    convert_csv(path, f"{path}_csv")


if __name__ == "__main__":
    main()
