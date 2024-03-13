
import argparse
import os
from clinical_etl import CSVConvert


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
    size = size_mapping[args.size]
    repo_dir = os.path.dirname(os.path.dirname(__file__))
    manifest_path = f"{repo_dir}/{size}_dataset_csv/"
    dataset_path = f"{manifest_path}raw_data"
    CSVConvert.csv_convert(input_path=dataset_path, manifest_file=f"{manifest_path}/manifest.yml", minify=True, index_output=False)


if __name__ == "__main__":
    main()
