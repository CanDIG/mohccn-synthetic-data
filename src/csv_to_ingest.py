import argparse
import os
from clinical_etl import CSVConvert
from clinical_etl.schema import ValidationError
from pathlib import Path
import pandas as pd
import sys
import json
import requests
import re
import random
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
        choices=['xs', 's', 'm', 'l'],
        help="Size of the synthetic dataset to convert, options: 'xs' for extra small, 's' for small, 'm' for medium, 'l' for large (default:"
             " small)"
    )
    parser.add_argument('--sample',
                        type=ranged_type(int, 1, 1999),
                        required=False,
                        help="Subsets the large dataset equally across the 4 programs based on the total number of "
                             "donors specified. (There will also be the three extra custom donors)")
    parser.add_argument('--donors-per-program', '-dp',
                        type=ranged_type(int, 1, 500),
                        required='--number-of-programs' in sys.argv,
                        help="Subsets the large dataset to the number of donors supplied in the argument. "
                             "--number-of-programs must also be specified.")
    parser.add_argument('--number-of-programs', '-np',
                        type=ranged_type(int, 1, 4),
                        required='--donors-per-program' in sys.argv,
                        help="Subsets the large dataset to the number of programs supplied in the argument. "
                             "--donors-per-program must also be specified.")
    parser.add_argument('--prefix',
                        type=str,
                        required=False,
                        help="Adds a `prefix`+`-` to all `submitter_<object>_id`s to differentiate datasets.")
    args = parser.parse_args()
    return args

def add_prefix_df(prefix: str, object_df: pd.DataFrame, file_name):
    """ Prepend all identifiers in a df with the specified prefix """
    if file_name == "Specimen.csv":
        submitter_fields = ["submitter_specimen_id", "submitter_donor_id", "submitter_primary_diagnosis_id"]
        object_df.loc[:, object_df.columns.str.startswith('submitter_')] = (object_df.filter(submitter_fields).
                                                                            apply(lambda x: prefix + "-" + x))
    else:
        object_df.loc[:, object_df.columns.str.startswith('submitter_')] = (object_df.filter(regex="^submitter").
                                                                            apply(lambda x: prefix + "-" + x))
    object_df.loc[:, object_df.columns.str.startswith('program_')] = (object_df.filter(items=["program_id"]).
                                                                      apply(lambda x: prefix + "-" + x))
    if 'reference_radiation_treatment_id' in object_df.columns:
        object_df.loc[:, object_df.columns.str.startswith('reference_radiation_treatment_id')] = \
            (object_df.filter(items=["reference_radiation_treatment_id"]).
             apply(lambda x: prefix + "-" + x))
    return object_df


def add_prefix_json(prefix: str, object_json: list):
    for file_set in object_json:
        file_set['program_id'] = f"{prefix}-{file_set['program_id']}"
        file_set['genomic_file_id'] = f"{prefix}-{file_set['genomic_file_id']}"
        for sample in file_set['samples']:
            sample['genomic_file_sample_id'] = f"{prefix}-{sample['genomic_file_sample_id']}"
            sample['submitter_sample_id'] = f"{prefix}-{sample['submitter_sample_id']}"
    return object_json


def replace_identifiers(prefix: str, input_folder: str):
    """ Iterate through all files in the input folder and prepend the prefix"""
    file_list = list(os.listdir(input_folder))
    print("Replacing identifiers ... ", end="")
    repo_dir = os.path.dirname(os.path.dirname(__file__))
    output_folder = os.path.join(repo_dir, f"custom_dataset_csv-{prefix}", "raw_data")
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    for file in file_list:
        print(f"processing {file}")
        csv_df = pd.read_csv(f"{input_folder}/{file}")
        csv_df = add_prefix_df(prefix, csv_df, file)
        csv_df.to_csv(f"{output_folder}/{file}", index=False)
    print(f"All identifiers prepended with {prefix}-.")


def subsample_csv(donors_per_program: int, number_of_programs: int, prefix: str = None, size: str = 'large'):
    repo_dir = os.path.dirname(os.path.dirname(__file__))
    total_donors = (donors_per_program * number_of_programs)
    csv_output_folder = os.path.join(repo_dir, f"custom_dataset_csv-{total_donors}", "raw_data")
    csv_input_folder = os.path.join(repo_dir, f"{size}_dataset_csv", "raw_data")
    Path(csv_output_folder).mkdir(parents=True, exist_ok=True)

    print(f"Subsampling csv files from {csv_input_folder}...")
    file_list = list(os.listdir(csv_input_folder))
    donor_df = pd.read_csv(f"{csv_input_folder}/Donor.csv")
    program_list = list(set(donor_df.program_id))
    program_list.sort()
    program_list = program_list[:number_of_programs]
    donor_df['donor_index'] = donor_df.groupby(['program_id']).cumcount()
    donor_df = donor_df.loc[donor_df.donor_index < donors_per_program]
    subsampled_donor_df = donor_df.loc[donor_df.program_id.isin(program_list)]
    donor_list = list(subsampled_donor_df['submitter_donor_id'])
    if prefix:
        subsampled_donor_df = add_prefix_df(prefix, subsampled_donor_df, "Donor.json")
        subsampled_donor_df.to_csv(f"{csv_output_folder}/Donor.csv", index=False)
    else:
        subsampled_donor_df.to_csv(f"{csv_output_folder}/Donor.csv", index=False)
    for file in file_list:
        if file == "Donor.csv":
            continue
        else:
            csv_df = pd.read_csv(f"{csv_input_folder}/{file}")
            subsampled_csv = csv_df.loc[csv_df.submitter_donor_id.isin(donor_list)]
            if len(subsampled_csv.index) == 0:
                continue
            else:
                if prefix:
                    subsampled_csv = add_prefix_df(prefix, subsampled_csv, file)
                    subsampled_csv.to_csv(f"{csv_output_folder}/{file}", index=False)
                else:
                    subsampled_csv.to_csv(f"{csv_output_folder}/{file}", index=False)
    return csv_output_folder, program_list


def get_file_list():
    response = requests.get("https://api.github.com/repos/CanDIG/htsget_app/git/trees/develop?recursive=1")
    response_json = response.json()
    paths = [x['path'] for x in response_json['tree']]
    data_files = [x for x in paths if re.match("^data/files/.*\\.(vcf\\.gz$|cram$|bam$)", x)]
    data_files = [x.split('/')[2] for x in data_files]
    return data_files


def get_index_file(file_name):
    if file_name.endswith("vcf.gz"):
        return file_name + ".tbi"
    if file_name.endswith("bam"):
        return file_name + ".bai"
    if file_name.endswith("cram"):
        return file_name + ".crai"


def get_sequence_type(file_name):
    if file_name.endswith("vcf.gz"):
        return "wgs"
    if file_name.endswith("bam"):
        return random.choice(["wgs", "wts"])
    if file_name.endswith("cram"):
        return random.choice(["wgs", "wts"])


def get_data_type(file_name):
    if file_name.endswith("vcf.gz"):
        return "variant"
    if file_name.endswith("bam"):
        return "read"
    if file_name.endswith("cram"):
        return "read"


def create_genomic_json(samples_df):
    files = get_file_list()
    with open("htsget_variant_sample_matching.json") as f:
        variant_samples = json.load(f)
    linkages = []
    with open("htsget_variant_sample_matching.json", "r") as f:
        vcf_samples = json.load(f)
    samples_dict = samples_df.to_dict('records')
    id_index = 0
    file_index = 0
    for sample in samples_dict:
        file_to_link = files[file_index]
        index_file = get_index_file(file_to_link)
        linkage = {
            "program_id": sample["program_id"],
            "genomic_file_id": file_to_link.split(".")[0] + "-" + str(id_index),
            "main": {
                "access_method": f"file:////app/htsget_server/data/files/{file_to_link}",
                "name": file_to_link
            },
            "index": {
                "access_method": f"file:////app/htsget_server/data/files/{index_file}",
                "name": index_file
            },
            "metadata": {
                "sequence_type": get_sequence_type(file_to_link),
                "data_type": get_data_type(file_to_link),
                "reference": "hg38"
            }
        }
        if file_to_link in variant_samples.keys():
            file_samples = [{
                "genomic_file_sample_id": variant_samples[file_to_link][0],
                "submitter_sample_id": sample["submitter_sample_id"]
            }]
            if len(variant_samples[file_to_link]) > 1:
                sample_name = sample["submitter_sample_id"].split("_")[:-1]
                if len(sample_name) > 1:
                    sample_name = sample_name[0] + "_" + sample_name[1]
                else:
                    sample_name = sample_name[0]
                sample_num = int(sample["submitter_sample_id"].split("_")[-1])
                sample_num -= 1
                file_samples.append({
                "genomic_file_sample_id": variant_samples[file_to_link][1],
                "submitter_sample_id": sample_name + "_" + str(sample_num).zfill(4)
                })
            linkage["samples"] = file_samples
        else:
            linkage["samples"] = [{"genomic_file_sample_id": file_to_link.split(".")[0],
                                   "submitter_sample_id": sample["submitter_sample_id"]}]
        linkages.append(linkage)
        id_index += 1
        if file_index < len(files) - 1:
            file_index += 1
        else:
            file_index = 0

    return linkages


def main():
    args = parse_args()
    size_mapping = {'xs': 'extra_small', 's': 'small', 'm': 'medium', 'l': 'large'}
    repo_dir = os.path.dirname(os.path.dirname(__file__))

    if args.sample:
        donors_per_program = int(args.sample / 4)
        if donors_per_program < 20:
            size = size_mapping['s']
        elif donors_per_program < 200:
            size = size_mapping['m']
        else:
            size = size_mapping['l']
        sample_result = subsample_csv(donors_per_program=donors_per_program,
                                      number_of_programs=4, prefix=args.prefix,
                                      size=size)
        dataset_path = Path(sample_result[0])
        manifest_path = f"{repo_dir}/{size}_dataset_csv/"
        if args.prefix:
            with open(f"{repo_dir}/{size}_dataset_csv/genomic.json") as f:
                genomic_json = json.load(f)
            output_dir = dataset_path.parent.absolute()
            genomic_json = add_prefix_json(args.prefix, genomic_json)
            with open(f'{output_dir}/genomic.json', 'w+') as f:
                json.dump(genomic_json, f, indent=4)
    elif args.donors_per_program:
        if args.donors_per_program < 20:
            size = size_mapping['s']
        elif args.donors_per_program < 200:
            size = size_mapping['m']
        else:
            size = size_mapping['l']

        manifest_path = f"{repo_dir}/{size}_dataset_csv/"
        sample_result = subsample_csv(donors_per_program=args.donors_per_program,
                                      number_of_programs=args.number_of_programs,
                                      prefix=args.prefix, size = size)
        dataset_path = Path(sample_result[0])
        with open(f"{repo_dir}/{size}_dataset_csv/genomic.json") as f:
            genomic_json = json.load(f)
        output_dir = dataset_path.parent.absolute()
        genomic_json = [x for x in genomic_json if x['program_id'] in sample_result[1]]
        if args.prefix:
            genomic_json = add_prefix_json(args.prefix, genomic_json)
        with open(f'{output_dir}/genomic.json', 'w+') as f:
            json.dump(genomic_json, f, indent=4)

    else:
        size = size_mapping[args.size]
        manifest_path = f"{repo_dir}/{size}_dataset_csv/"
        dataset_path = Path(f"{manifest_path}raw_data")
        if args.prefix:
            replace_identifiers(args.prefix, dataset_path)
            dataset_path = Path(f"{repo_dir}/custom_dataset_csv-{args.prefix}/raw_data")
        with open(f"{dataset_path}/SampleRegistration.csv") as f:
            samples_csv = pd.read_csv(f)
        output_dir = dataset_path.parent.absolute()
        genomic_json = create_genomic_json(samples_csv)
        with open(f'{output_dir}/genomic-test.json', 'w+') as f:
            json.dump(genomic_json, f, indent=4)

    packets, errors = CSVConvert.csv_convert(input_path=dataset_path, manifest_file=f"{manifest_path}/manifest.yml",
                                             minify=True, index_output=False)

    if errors:
        raise ValidationError("Validation failed, errors must be corrected before ingest.")


if __name__ == "__main__":
    main()
