"""
Script to create csvs from a set of generated mockaroo jsons. See chord_metadata_service/mohpackets/data
https://github.com/CanDIG/katsu/tree/develop/chord_metadata_service/mohpackets/data for more information on how to
generate the data. Shouldn't need to be regenerated unless the underlying MoH model changes significantly.
"""

import os
import json
import pandas as pd
import argparse
from pathlib import Path
import random


def process_donor(df):
    if 'is_deceased' in df.columns and 'cause_of_death' in df.columns:
        condition = df['is_deceased'] == False
        df.loc[condition, 'cause_of_death'] = ""
        df.loc[condition, 'date_of_death'] = ""
        condition = df['is_deceased'].isna()
        df.loc[condition, 'date_of_death'] = ""
        df.loc[condition, 'cause_of_death'] = ""
        condition = df['is_deceased'] == ""
        df.loc[condition, 'date_of_death'] = ""
        df.loc[condition, 'cause_of_death'] = ""
        condition = (df['is_deceased'] == True)
        df.loc[condition, 'lost_to_followup_reason'] = ""
        df.loc[condition, 'lost_to_followup_after_clinical_event_identifier'] = ""
        df.loc[condition, 'date_alive_after_lost_to_followup'] = ""
    if 'lost_to_followup_reason' in df.columns and 'lost_to_followup_after_clinical_event_identifier' in df.columns:
        condition = df['lost_to_followup_after_clinical_event_identifier'].isna()
        df.loc[condition, 'lost_to_followup_reason'] = ""
        condition = df['lost_to_followup_after_clinical_event_identifier'] == ""
        df.loc[condition, 'lost_to_followup_reason'] = ""
    condition = df['date_resolution'].isna() & ~df.date_of_birth.astype('str').str.contains('day_interval')
    df.loc[condition, 'date_resolution'] = "month"
    condition = df['date_resolution'].isna() & df.date_of_birth.astype('str').str.contains('day_interval')
    df.loc[condition, 'date_resolution'] = "day"
    return df


def process_comorbidity(df):
    if 'prior_malignancy' in df.columns and 'laterality_of_prior_malignancy' in df.columns:
        condition = (df['prior_malignancy'] != "Yes") & df['laterality_of_prior_malignancy'].notna()
        df.loc[condition, 'laterality_of_prior_malignancy'] = ""
    return df


def process_exposure(df):
    if 'tobacco_smoking_status' in df.columns and 'tobacco_type' in df.columns:
        condition = df['tobacco_smoking_status'].isin(['Smoking history not documented', 'Lifelong non-smoker (<100 cigarettes smoked in lifetime)', 'Not applicable'])
        df.loc[condition, 'tobacco_type'] = ""
        condition = df['tobacco_smoking_status'].isin(['Smoking history not documented', 'Lifelong non-smoker (<100 cigarettes smoked in lifetime)', 'Not applicable'])
        df.loc[condition, 'pack_years_smoked'] = None
    return df


def process_followups(df):
    rows = df.shape[0]
    bool_list = random.choices([True, False], k=rows)
    df.loc[bool_list, 'submitter_treatment_id'] = ""
    reverse_list = [not x for x in bool_list]
    df.loc[reverse_list, 'submitter_primary_diagnosis_id'] = ""
    return df


def add_extra_donors():
    donor_11 = {
            "cause_of_death": "Unknown",
            "date_of_death": {
                "month_interval": 90,
                "day_interval": 2700
            },
            "gender": "Woman",
            "is_deceased": True,
            "primary_site": [
                "Floor of mouth"
            ],
            "program_id": "SYNTHETIC-2",
            "sex_at_birth": "Other",
            "submitter_donor_id": "DONOR_11"
        }
    # the null donor
    donor_12 = {
            "submitter_donor_id": "DONOR_12",
            "program_id": "SYNTHETIC-2"
        }
    return donor_11, donor_12


def add_pds():
    donor_12 = [{
        "submitter_primary_diagnosis_id": "PRIMARY_DIAGNOSIS_1a",
        "submitter_donor_id": "DONOR_12",
        "program_id": "SYNTHETIC-2"
    }]
    return donor_12


def add_specimens():
    donor_12 = [{
        "submitter_specimen_id": "SPECIMEN_1a",
        "submitter_donor_id": "DONOR_12",
        "submitter_primary_diagnosis_id": "PRIMARY_DIAGNOSIS_1a",
        "program_id": "SYNTHETIC-2"
    }]
    return donor_12


def add_samples():
    donor_12 = [
        {
            "submitter_sample_id": "SAMPLE_REGISTRATION_1a",
            "submitter_specimen_id": "SPECIMEN_1a",
            "submitter_donor_id": "DONOR_12",
            "program_id": "SYNTHETIC-2"
        },
        {
            "submitter_sample_id": "SAMPLE_REGISTRATION_2a",
            "submitter_specimen_id": "SPECIMEN_1a",
            "submitter_donor_id": "DONOR_12",
            "program_id": "SYNTHETIC-2"
        }
    ]
    return donor_12


def add_treatments():
    donor_12 = [
        {
            "submitter_treatment_id": "TREATMENT_1a",
            "submitter_donor_id": "DONOR_12",
            "submitter_primary_diagnosis_id": "PRIMARY_DIAGNOSIS_1a",
            "program_id": "SYNTHETIC-2"
        },
        {
            "submitter_treatment_id": "TREATMENT_2a",
            "submitter_donor_id": "DONOR_12",
            "submitter_primary_diagnosis_id": "PRIMARY_DIAGNOSIS_1a",
            "program_id": "SYNTHETIC-2"
        }
    ]
    return donor_12


def add_chemo():
    donor_12 = [
        {
            "submitter_treatment_id": "TREATMENT_2a",
            "actual_cumulative_drug_dose": 60,
            "submitter_donor_id": "DONOR_12",
            "program_id": "SYNTHETIC-2"
        },
        {
            "submitter_treatment_id": "TREATMENT_2a",
            "prescribed_cumulative_drug_dose": 4600,
            "submitter_donor_id": "DONOR_12",
            "program_id": "SYNTHETIC-2"
        },
        {
            "submitter_treatment_id": "TREATMENT_1a",
            "drug_name": "Gemcitabine",
            "drug_reference_database": "NCI Thesaurus",
            "submitter_donor_id": "DONOR_12",
            "program_id": "SYNTHETIC-2"
        }
    ]
    return donor_12


def add_followups():
    donor_12 = [
        {
            "submitter_follow_up_id": "FOLLOW_UP_2a",
            "submitter_treatment_id": "TREATMENT_1a",
            "submitter_donor_id": "DONOR_12",
            "program_id": "SYNTHETIC-2"
        },
        {
            "submitter_follow_up_id": "FOLLOW_UP_1a",
            "submitter_primary_diagnosis_id": "PRIMARY_DIAGNOSIS_1a",
            "submitter_donor_id": "DONOR_12",
            "program_id": "SYNTHETIC-2"
        }
    ]
    return donor_12


def add_comorbidities():
    donor_12 = [{
        "age_at_comorbidity_diagnosis": 56,
        "comorbidity_type_code": "C43.9",
        "submitter_donor_id": "DONOR_12",
        "program_id": "SYNTHETIC-2"
    },
        {
            "comorbidity_treatment": "Photodynamic therapy",
            "submitter_donor_id": "DONOR_12",
            "program_id": "SYNTHETIC-2"
        },
        {
            "prior_malignancy": "Yes",
            "submitter_donor_id": "DONOR_12",
            "program_id": "SYNTHETIC-2"
        }

    ]
    return donor_12


def add_exposures():
    donor_12 = [
        {
            "tobacco_smoking_status": "Current smoker",
            "submitter_donor_id": "DONOR_12",
            "program_id": "SYNTHETIC-2"
        },
        {
            "pack_years_smoked": 72,
            "submitter_donor_id": "DONOR_12",
            "program_id": "SYNTHETIC-2"
        }
    ]
    return donor_12


def add_biomarkers():
    donor_12 = [
        {
            "test_date": {
                "month_interval": 49,
                "day_interval": 1470
            }
        },
        {
            "ca125": 109,
        },
        {
            "hpv_strain": [
                "HPV52",
                "HPV58",
                "HPV35"
            ]
        },
        {
            "er_status": "Not applicable",
            "her2_ihc_status": "Cannot be determined",
            "her2_ish_status": "Positive",
        },
        {
            "cea": 5,
        }
    ]
    return donor_12


def add_hormone_therapies():
    donor_12 = [
        {
            "submitter_treatment_id": "TREATMENT_2a",
            "drug_name": "Cabergoline",
            "submitter_donor_id": "DONOR_12",
            "program_id": "SYNTHETIC-2"
        },
        {
            "submitter_treatment_id": "TREATMENT_2a",
            "drug_name": "Lutetium Lu 177 Dotatate",
            "drug_reference_identifier": "557845",
            "submitter_donor_id": "DONOR_12",
            "program_id": "SYNTHETIC-2"
        },
        {
            "submitter_treatment_id": "TREATMENT_1a",
            "prescribed_cumulative_drug_dose": 106,
            "actual_cumulative_drug_dose": 85,
            "submitter_donor_id": "DONOR_12",
            "program_id": "SYNTHETIC-2"
        }
    ]
    return donor_12


def add_immunotherapies():
    donor_12 = [
        {
            "submitter_treatment_id": "TREATMENT_2a",
            "immunotherapy_type": "Other immunomodulatory substances",
            "submitter_donor_id": "DONOR_12",
            "program_id": "SYNTHETIC-2"
        },
        {
            "submitter_treatment_id": "TREATMENT_2a",
            "drug_name": "Nivolumab",
            "drug_reference_identifier": "987654",
            "drug_reference_database": "PubChem",
            "submitter_donor_id": "DONOR_12",
            "program_id": "SYNTHETIC-2"
        },
        {
            "submitter_treatment_id": "TREATMENT_1a",
            "immunotherapy_drug_dose_units": "mg/kg",
            "submitter_donor_id": "DONOR_12",
            "program_id": "SYNTHETIC-2"
        }
    ]
    return donor_12


def add_radiations():
    donor_12 = [
        {
            "submitter_treatment_id": "TREATMENT_2a",
            "radiation_therapy_type": "Internal",
            "submitter_donor_id": "DONOR_12",
            "program_id": "SYNTHETIC-2"
        },
        {
            "submitter_treatment_id": "TREATMENT_2a",
            "radiation_therapy_modality": "Teleradiotherapy neutrons (procedure)",
            "submitter_donor_id": "DONOR_12",
            "program_id": "SYNTHETIC-2"
        },
        {
            "submitter_treatment_id": "TREATMENT_1a",
            "anatomical_site_irradiated": "Right Maxilla",
            "submitter_donor_id": "DONOR_12",
            "program_id": "SYNTHETIC-2"
        }
    ]
    return donor_12


def add_surgeries():
    donor_12 = [
        {
            "submitter_treatment_id": "TREATMENT_2a",
            "submitter_specimen_id": "SPECIMEN_1a",
            "surgery_type": "Wide Local Excision",
            "submitter_donor_id": "DONOR_12",
            "program_id": "SYNTHETIC-2"
        },
        {
            "submitter_treatment_id": "TREATMENT_2a",
            "submitter_specimen_id": "SPECIMEN_1a",
            "surgery_site": "C11",
            "submitter_donor_id": "DONOR_12",
            "program_id": "SYNTHETIC-2"
        },
        {
            "submitter_treatment_id": "TREATMENT_1a",
            "submitter_specimen_id": "SPECIMEN_1a",
            "surgery_location": "Metastatic",
            "submitter_donor_id": "DONOR_12",
            "program_id": "SYNTHETIC-2"
        }
    ]
    return donor_12


def add_objects(filename):
    match filename:
        case "Donor.json":
            return add_extra_donors()
        case "PrimaryDiagnosis.json":
            return add_pds()
        case "Treatment.json":
            return add_treatments()
        case "Chemotherapy.json":
            return add_chemo()
        case "Comorbidity.json":
            return add_comorbidities()
        case "Exposure.json":
            return add_exposures()
        case "FollowUp.json":
            return add_followups()
        case "HormoneTherapy.json":
            return add_hormone_therapies()
        case "Immunotherapy.json":
            return add_immunotherapies()
        case "Radiation.json":
            return add_radiations()
        case "SampleRegistration.json":
            return add_samples()
        case "Specimen.json":
            return add_specimens()
        case "Surgery.json":
            return add_surgeries()
        case "Biomarker.json":
            return add_biomarkers()
        case _:
            return


def convert_to_csv(size, input_path):
    # Get the absolute path to the synthetic data folder
    repo_dir = os.path.dirname(os.path.dirname(__file__))
    synthetic_data_folder = input_path
    output_dir = os.path.join(repo_dir, f"{size}_dataset_csv/raw_data")
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Iterate through all JSON files in the synthetic_data_folder
    for filename in os.listdir(synthetic_data_folder):
        if filename.endswith('.json') and not filename.startswith("Program"):
            json_file_path = os.path.join(synthetic_data_folder, filename)
            with open(json_file_path, 'r') as f:
                data = json.load(f)
                extra_objects = add_objects(filename)
                if extra_objects:
                    data.extend(extra_objects)
                df = pd.DataFrame(data)
                if filename.startswith("Donor"):
                    df = process_donor(df)
                elif filename.startswith("Comorbidity"):
                    df = process_comorbidity(df)
                elif filename.startswith("Exposure"):
                    df = process_exposure(df)
                elif filename.startswith("FollowUp"):
                    df = process_followups(df)

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
    parser.add_argument(
        '--input',
        type=str,
        required=True,
        help="Path to generated mockaroo files. Assumes a folder structure such as 'mockaroo_data/small_dataset/synthetic_data/*.json' such as generated by katsu data_converter.py script."
    )
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    size_mapping = {'s': 'small', 'm': 'medium', 'l': 'large'}
    convert_to_csv(size_mapping[args.size], f"{args.input}/{size_mapping[args.size]}_dataset/synthetic_data")


if __name__ == "__main__":
    main()
