
import argparse
import os
from clinical_etl import CSVConvert
from clinical_etl.schema import ValidationError
from pathlib import Path
from json_to_csv import sort_key
import pandas as pd
import math


def ranged_type(value_type, min_value, max_value):
    """
    from: https://stackoverflow.com/questions/55324449/how-to-specify-a-minimum-or-maximum-float-value-with-argparse
    Return function handle of an argument type function for ArgumentParser checking a range:
        min_value <= arg <= max_value

    Parameters
    ----------
    value_type  - value-type to convert arg to
    min_value   - minimum acceptable argument
    max_value   - maximum acceptable argument

    Returns
    -------
    function handle of an argument type function for ArgumentParser


    Usage
    -----
        ranged_type(float, 0.0, 1.0)

    """

    def range_checker(arg: str):
        try:
            f = value_type(arg)
        except ValueError:
            raise argparse.ArgumentTypeError(f'must be a valid {value_type}')
        if f < min_value or f > max_value:
            raise argparse.ArgumentTypeError(f'must be within [{min_value}, {max_value}]')
        return f

    # Return function handle to checking function
    return range_checker


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--size',
        type=str,
        default='s',
        choices=['s', 'm', 'l'],
        help="Size of the synthetic dataset to convert, options: 's' for small, 'm' for medium, 'l' for large (default:"
             " small)"
    )
    parser.add_argument('--sample',
                        type=ranged_type(int, 1, 4999),
                        required=False,
                        help="Subsets the large dataset to the number of donors supplied in the argument. "
                             "(There will also be the three extra custom donors)")
    parser.add_argument('--prefix',
                        type=str,
                        required=False,
                        help="")
    args = parser.parse_args()
    return args


def _subsample_csv(donor_number):
    # large dataset is 5000 donors and 10 programs + 3 additional custom donors
    size = 'large'
    repo_dir = os.path.dirname(os.path.dirname(__file__))
    csv_output_folder = os.path.join(repo_dir, f"custom_dataset_csv_{donor_number}", "raw_data")
    csv_input_folder = os.path.join(repo_dir, f"{size}_dataset_csv", "raw_data")
    Path(csv_output_folder).mkdir(parents=True, exist_ok=True)
    donors_per_program = int(donor_number/10)
    extra_donors = donor_number - (donors_per_program * 10)

    print(f"Subsampling csv files from {csv_input_folder}...")

    file_list = list(os.listdir(csv_input_folder))
    donor_df = pd.read_csv(f"{csv_input_folder}/Donor.csv")
    custom_donors = ['DONOR_ALL_01', 'DONOR_ALL_02', 'DONOR_NULL']
    donor_df['donor_index'] = donor_df.groupby(['program_id']).cumcount()
    subsampled_donor_df = donor_df.loc[donor_df.donor_index.isin(range(0, donors_per_program)) |
                                       donor_df.submitter_donor_id.isin(custom_donors)]
    extra_donors_df = donor_df.loc[donor_df.program_id.isin([donor_df.program_id[0]]) &
                                   donor_df.donor_index.isin(range(donors_per_program,
                                                                   donors_per_program + extra_donors))]
    subsampled_donor_df = pd.concat([subsampled_donor_df, extra_donors_df]).drop(columns="donor_index")
    subsampled_donor_df.to_csv(f"{csv_output_folder}/Donor.csv", index=False)
    for file in file_list:
        if file == "Donor.csv":
            continue
        else:
            csv_df = pd.read_csv(f"{csv_input_folder}/{file}")
            subsampled_csv = csv_df.loc[csv_df.submitter_donor_id.isin(subsampled_donor_df.submitter_donor_id)]
            subsampled_csv.to_csv(f"{csv_output_folder}/{file}", index=False)
    return csv_output_folder


def main():
    args = parse_args()
    size_mapping = {'s': 'small', 'm': 'medium', 'l': 'large'}
    repo_dir = os.path.dirname(os.path.dirname(__file__))
    if args.sample:
        dataset_path = _subsample_csv(args.sample)
        size = size_mapping['l']
        manifest_path = f"{repo_dir}/{size}_dataset_csv/"
    else:
        size = size_mapping[args.size]
        manifest_path = f"{repo_dir}/{size}_dataset_csv/"
        dataset_path = f"{manifest_path}raw_data"

    packets, errors = CSVConvert.csv_convert(input_path=dataset_path, manifest_file=f"{manifest_path}/manifest.yml",
                                             minify=True, index_output=False)
    if errors:
        raise ValidationError("Validation failed, errors must be corrected before ingest.")


if __name__ == "__main__":
    main()
