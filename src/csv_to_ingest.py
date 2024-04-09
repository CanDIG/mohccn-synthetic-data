import argparse
import os
from clinical_etl import CSVConvert
from clinical_etl.schema import ValidationError
from pathlib import Path
import pandas as pd
import sys
import json
pd.options.mode.chained_assignment = None


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
                        help="Subsets the large dataset equally across the 10 programs based on the total number of "
                             "donors specified. (There will also be the three extra custom donors)")
    parser.add_argument('--donors-per-program', '-dp',
                        type=ranged_type(int, 1, 500),
                        required='--number-of-programs' in sys.argv,
                        help="Subsets the large dataset to the number of donors supplied in the argument. "
                             "--number-of-programs must also be specified.")
    parser.add_argument('--number-of-programs', '-np',
                        type=ranged_type(int, 1, 10),
                        required='--donors-per-program' in sys.argv,
                        help="Subsets the large dataset to the number of programs supplied in the argument. "
                             "--donors-per-program must also be specified.")
    parser.add_argument('--prefix',
                        type=str,
                        required=False,
                        help="Adds a `prefix`+`-` to all `submitter_<object>_id`s to differentiate datasets.")
    args = parser.parse_args()
    return args


def add_prefix_df(prefix: str, object_df: pd.DataFrame):
    """ Prepend all identifiers in a df with the specified prefix """
    object_df.loc[:, object_df.columns.str.startswith('submitter_')] = (object_df.filter(regex="^submitter").
                                                                        apply(lambda x: prefix + "-" + x))
    object_df.loc[:, object_df.columns.str.startswith('program_')] = (object_df.filter(items=["program_id"]).
                                                                      apply(lambda x: prefix + "-" + x))
    if 'reference_radiation_treatment_id' in object_df.columns:
        object_df.loc[:, object_df.columns.str.startswith('reference_radiation_treatment_id')] = \
            (object_df.filter(items=["reference_radiation_treatment_id"]).
             apply(lambda x: prefix + "-" + x))
    return object_df


def _add_prefix_json(prefix: str, object_json: dict, output_dir):
    for file_set in object_json:
        file_set['program_id'] = f"{prefix}-{file_set['program_id']}"
        file_set['genomic_file_id'] = f"{prefix}-{file_set['genomic_file_id']}"
        for sample in file_set['samples']:
            sample['genomic_file_sample_id'] = f"{prefix}-{sample['genomic_file_sample_id']}"
            sample['submitter_sample_id'] = f"{prefix}-{sample['submitter_sample_id']}"
    with open(f'{output_dir}/genomic.json', 'w+') as f:
        json.dump(object_json, f, indent=4)


def replace_identifiers(prefix: str, input_folder: str):
    """ Iterate through all files in the input folder and prepend the prefix"""
    file_list = list(os.listdir(input_folder))
    print("Replacing identifiers ... ", end="")
    repo_dir = os.path.dirname(os.path.dirname(__file__))
    output_folder = os.path.join(repo_dir, f"custom_dataset_csv-{prefix}", "raw_data")
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    for file in file_list:
        csv_df = pd.read_csv(f"{input_folder}/{file}")
        csv_df = add_prefix_df(prefix, csv_df)
        csv_df.to_csv(f"{output_folder}/{file}")
    print(f"All identifiers prepended with {prefix}-.")


def subsample_csv(donors_per_program: int, number_of_programs: int, extra_donors: int = 0, prefix: str = None):
    # large dataset is 5000 donors and 10 programs + 3 additional custom donors
    size = 'large'
    repo_dir = os.path.dirname(os.path.dirname(__file__))
    total_donors = (donors_per_program * number_of_programs) + extra_donors
    csv_output_folder = os.path.join(repo_dir, f"custom_dataset_csv-{total_donors}", "raw_data")
    csv_input_folder = os.path.join(repo_dir, f"{size}_dataset_csv", "raw_data")
    Path(csv_output_folder).mkdir(parents=True, exist_ok=True)

    print(f"Subsampling csv files from {csv_input_folder}...")
    file_list = list(os.listdir(csv_input_folder))
    donor_df = pd.read_csv(f"{csv_input_folder}/Donor.csv")
    program_list = list(set(donor_df.program_id))[:number_of_programs]
    custom_donors = ['DONOR_ALL_01', 'DONOR_ALL_02', 'DONOR_NULL']
    donor_df['donor_index'] = donor_df.groupby(['program_id']).cumcount()
    subsampled_donor_df = donor_df.loc[donor_df.program_id.isin(program_list)]
    subsampled_donor_df = subsampled_donor_df.loc[subsampled_donor_df.donor_index.isin(range(0, donors_per_program)) |
                                                  subsampled_donor_df.submitter_donor_id.isin(custom_donors)]
    extra_donors_df = donor_df.loc[donor_df.program_id.isin([donor_df.program_id[0]]) &
                                   donor_df.donor_index.isin(range(donors_per_program,
                                                                   donors_per_program + extra_donors))]
    subsampled_donor_df = pd.concat([subsampled_donor_df, extra_donors_df]).drop(columns="donor_index")
    donor_list = list(subsampled_donor_df['submitter_donor_id'])
    if prefix:
        subsampled_donor_df = add_prefix_df(prefix, subsampled_donor_df)
        subsampled_donor_df.to_csv(f"{csv_output_folder}/Donor.csv", index=False)
    else:
        subsampled_donor_df.to_csv(f"{csv_output_folder}/Donor.csv", index=False)
    for file in file_list:
        if file == "Donor.csv":
            continue
        else:
            csv_df = pd.read_csv(f"{csv_input_folder}/{file}")
            subsampled_csv = csv_df.loc[csv_df.submitter_donor_id.isin(donor_list)]
            if prefix:
                subsampled_csv = add_prefix_df(prefix, subsampled_csv)
                subsampled_csv.to_csv(f"{csv_output_folder}/{file}", index=False)
            else:
                subsampled_csv.to_csv(f"{csv_output_folder}/{file}", index=False)
    return csv_output_folder


def main():
    args = parse_args()
    size_mapping = {'s': 'small', 'm': 'medium', 'l': 'large'}
    repo_dir = os.path.dirname(os.path.dirname(__file__))

    if args.sample:
        donors_per_program = int(args.sample / 10)
        extra_donors = args.sample - (donors_per_program * 10)
        dataset_path = Path(subsample_csv(donors_per_program=donors_per_program,
                                          number_of_programs=10, extra_donors=extra_donors,
                                          prefix=args.prefix))
        size = size_mapping['l']
        manifest_path = f"{repo_dir}/{size}_dataset_csv/"
        if args.prefix:
            with open(f"{repo_dir}/{size}_dataset_csv/genomic.json") as f:
                genomic_json = json.load(f)
            output_dir = dataset_path.parent.absolute()
            _add_prefix_json(args.prefix, genomic_json, output_dir)
    elif args.donors_per_program:
        size = size_mapping['l']
        manifest_path = f"{repo_dir}/{size}_dataset_csv/"
        dataset_path = Path(subsample_csv(donors_per_program=args.donors_per_program,
                                          number_of_programs=args.number_of_programs,
                                          prefix=args.prefix))
        if args.prefix:
            with open(f"{repo_dir}/{size}_dataset_csv/genomic.json") as f:
                genomic_json = json.load(f)
            output_dir = dataset_path.parent.absolute()
            _add_prefix_json(args.prefix, genomic_json, output_dir)
    else:
        size = size_mapping[args.size]
        manifest_path = f"{repo_dir}/{size}_dataset_csv/"
        dataset_path = f"{manifest_path}raw_data"
        if args.prefix:
            replace_identifiers(args.prefix, dataset_path)
            dataset_path = Path(f"{repo_dir}/custom_dataset_csv-{args.prefix}/raw_data")
            with open(f"{repo_dir}/{size}_dataset_csv/genomic.json") as f:
                genomic_json = json.load(f)
            output_dir = dataset_path.parent.absolute()
            _add_prefix_json(args.prefix, genomic_json, output_dir)

    packets, errors = CSVConvert.csv_convert(input_path=dataset_path, manifest_file=f"{manifest_path}/manifest.yml",
                                             minify=True, index_output=False)

    if errors:
        raise ValidationError("Validation failed, errors must be corrected before ingest.")


if __name__ == "__main__":
    main()
