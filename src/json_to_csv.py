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
import itertools


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
    half_length = int(rows/2)
    bool_list = [True, False] * half_length
    if len(bool_list) < rows:
        bool_list.append(True)
    df.loc[bool_list, 'submitter_treatment_id'] = ""
    reverse_list = [not x for x in bool_list]
    df.loc[reverse_list, 'submitter_primary_diagnosis_id'] = ""
    return df


def add_extra_donors():
    donors = [{
        "cause_of_death": "Unknown",
        "date_of_death": {
            "month_interval": 90,
            "day_interval": 2700
        },
        "gender": "Woman",
        "is_deceased": True,
        "primary_site": [
            "Floor of mouth",
            "Other and unspecified parts of mouth"
        ],
        "program_id": "SYNTHETIC-2",
        "sex_at_birth": "Other",
        "submitter_donor_id": "DONOR_011"
    },
    {
        "submitter_donor_id": "DONOR_000",
        "program_id": "SYNTHETIC-2"
    }]
    return donors


def add_pds():
    pds = [
        {
            "basis_of_diagnosis": "Specific tumour markers",
            "cancer_type_code": "C67.6",
            "clinical_m_category": "M1a(1)",
            "clinical_n_category": "N0b (no biopsy)",
            "clinical_t_category": "TX",
            "date_of_diagnosis": {
                "month_interval": 69,
                "day_interval": 2070
            },
            "laterality": "Right",
            "lymph_nodes_examined_method": "Imaging",
            "lymph_nodes_examined_status": "No lymph nodes found in resected specimen",
            "number_lymph_nodes_positive": 10,
            "submitter_primary_diagnosis_id": "PRIMARY_DIAGNOSIS_016",
            "program_id": "SYNTHETIC-2",
            "submitter_donor_id": "DONOR_011"
        },
        {
            "submitter_primary_diagnosis_id": "PRIMARY_DIAGNOSIS_1a",
            "submitter_donor_id": "DONOR_000",
            "program_id": "SYNTHETIC-2"
        }]
    return pds


def add_specimens():
    specimens = [
        {
            "pathological_m_category": "M1e",
            "pathological_n_category": "N0a",
            "pathological_stage_group": "Stage IIIC",
            "pathological_t_category": "Tis",
            "pathological_tumour_staging_system": "AJCC 7th edition",
            "percent_tumour_cells_range": "0-19%",
            "reference_pathology_confirmed_tumour_presence": "No",
            "specimen_anatomic_location": "C43.9",
            "specimen_collection_date": {
                "month_interval": 20,
                "day_interval": 600
            },
            "specimen_laterality": "Right",
            "specimen_processing": "Cryopreservation in liquid nitrogen (dead tissue)",
            "submitter_specimen_id": "SPECIMEN_022",
            "program_id": "SYNTHETIC-2",
            "submitter_donor_id": "DONOR_011",
            "tumour_grade": "Low",
            "tumour_histological_type": "8962/1"
        },
        {
            "submitter_specimen_id": "SPECIMEN_1a",
            "submitter_donor_id": "DONOR_000",
            "submitter_primary_diagnosis_id": "PRIMARY_DIAGNOSIS_1a",
            "program_id": "SYNTHETIC-2"
        }]
    return specimens


def add_samples():
    samples = [{
        "sample_type": "ctDNA",
        "specimen_tissue_source": "Fetal blood",
        "specimen_type": "Normal",
        "submitter_sample_id": "SAMPLE_REGISTRATION_28",
        "tumour_normal_designation": "Tumour",
        "program_id": "SYNTHETIC-2",
        "submitter_donor_id": "DONOR_011"
    },
        {
            "submitter_sample_id": "SAMPLE_REGISTRATION_1a",
            "submitter_specimen_id": "SPECIMEN_1a",
            "submitter_donor_id": "DONOR_000",
            "program_id": "SYNTHETIC-2"
        },
        {
            "submitter_sample_id": "SAMPLE_REGISTRATION_2a",
            "submitter_specimen_id": "SPECIMEN_1a",
            "submitter_donor_id": "DONOR_000",
            "program_id": "SYNTHETIC-2"
        }
    ]
    return samples


def add_treatments():
    treatments = [
        {
            "days_per_cycle": 2,
            "is_primary_treatment": "No",
            "line_of_treatment": 4,
            "number_of_cycles": 4,
            "response_to_treatment": "Complete remission with incomplete hematologic recovery (CRi)",
            "response_to_treatment_criteria_method": "Physician Assessed Response Criteria",
            "status_of_treatment": "Not applicable",
            "submitter_treatment_id": "TREATMENT_0025",
            "submitter_primary_diagnosis_id": "PRIMARY_DIAGNOSIS_016",
            "program_id": "SYNTHETIC-2",
            "submitter_donor_id": "DONOR_011",
            "treatment_end_date": {
                "month_interval": 87,
                "day_interval": 2610
            },
            "treatment_setting": "Induction",
            "treatment_start_date": {
                "month_interval": 25,
                "day_interval": 750
            },
            "treatment_type": ["Immunotherapy", "Surgery", "Photodynamic therapy"]
        },
        {
            "days_per_cycle": 2,
            "is_primary_treatment": "No",
            "line_of_treatment": 4,
            "number_of_cycles": 4,
            "response_to_treatment": "Complete remission with incomplete hematologic recovery (CRi)",
            "response_to_treatment_criteria_method": "Physician Assessed Response Criteria",
            "status_of_treatment": "Not applicable",
            "submitter_treatment_id": "TREATMENT_0026",
            "submitter_primary_diagnosis_id": "PRIMARY_DIAGNOSIS_016",
            "program_id": "SYNTHETIC-2",
            "submitter_donor_id": "DONOR_011",
            "treatment_end_date": {
                "month_interval": 87,
                "day_interval": 2610
            },
            "treatment_setting": "Induction",
            "treatment_start_date": {
                "month_interval": 25,
                "day_interval": 750
            },
            "treatment_type": "Chemotherapy"
        },
        {
            "days_per_cycle": 2,
            "is_primary_treatment": "No",
            "line_of_treatment": 4,
            "number_of_cycles": 4,
            "response_to_treatment": "Complete remission with incomplete hematologic recovery (CRi)",
            "response_to_treatment_criteria_method": "Physician Assessed Response Criteria",
            "status_of_treatment": "Not applicable",
            "submitter_treatment_id": "TREATMENT_0027",
            "submitter_primary_diagnosis_id": "PRIMARY_DIAGNOSIS_016",
            "program_id": "SYNTHETIC-2",
            "submitter_donor_id": "DONOR_011",
            "treatment_end_date": {
                "month_interval": 87,
                "day_interval": 2610
            },
            "treatment_setting": "Induction",
            "treatment_start_date": {
                "month_interval": 25,
                "day_interval": 750
            },
            "treatment_type": "Hormonal therapy"
        },
        {
            "days_per_cycle": 2,
            "is_primary_treatment": "No",
            "line_of_treatment": 4,
            "number_of_cycles": 4,
            "response_to_treatment": "Complete remission with incomplete hematologic recovery (CRi)",
            "response_to_treatment_criteria_method": "Physician Assessed Response Criteria",
            "status_of_treatment": "Not applicable",
            "submitter_treatment_id": "TREATMENT_0034",
            "submitter_primary_diagnosis_id": "PRIMARY_DIAGNOSIS_016",
            "program_id": "SYNTHETIC-2",
            "submitter_donor_id": "DONOR_011",
            "treatment_end_date": {
                "month_interval": 87,
                "day_interval": 2610
            },
            "treatment_setting": "Induction",
            "treatment_start_date": {
                "month_interval": 25,
                "day_interval": 750
            },
            "treatment_type": "Hormonal therapy"
        },
        {
            "days_per_cycle": 2,
            "is_primary_treatment": "No",
            "line_of_treatment": 4,
            "number_of_cycles": 4,
            "response_to_treatment": "Complete remission with incomplete hematologic recovery (CRi)",
            "response_to_treatment_criteria_method": "Physician Assessed Response Criteria",
            "status_of_treatment": "Not applicable",
            "submitter_treatment_id": "TREATMENT_0028",
            "submitter_primary_diagnosis_id": "PRIMARY_DIAGNOSIS_016",
            "program_id": "SYNTHETIC-2",
            "submitter_donor_id": "DONOR_011",
            "treatment_end_date": {
                "month_interval": 87,
                "day_interval": 2610
            },
            "treatment_setting": "Induction",
            "treatment_start_date": {
                "month_interval": 25,
                "day_interval": 750
            },
            "treatment_type": "No treatment"
        },
        {
            "days_per_cycle": 2,
            "is_primary_treatment": "No",
            "line_of_treatment": 4,
            "number_of_cycles": 4,
            "response_to_treatment": "Complete remission with incomplete hematologic recovery (CRi)",
            "response_to_treatment_criteria_method": "Physician Assessed Response Criteria",
            "status_of_treatment": "Not applicable",
            "submitter_treatment_id": "TREATMENT_0029",
            "submitter_primary_diagnosis_id": "PRIMARY_DIAGNOSIS_016",
            "program_id": "SYNTHETIC-2",
            "submitter_donor_id": "DONOR_011",
            "treatment_end_date": {
                "month_interval": 87,
                "day_interval": 2610
            },
            "treatment_setting": "Induction",
            "treatment_start_date": {
                "month_interval": 25,
                "day_interval": 750
            },
            "treatment_type": "Other targeting molecular therapy"
        },
        {
            "days_per_cycle": 2,
            "is_primary_treatment": "No",
            "line_of_treatment": 4,
            "number_of_cycles": 4,
            "response_to_treatment": "Complete remission with incomplete hematologic recovery (CRi)",
            "response_to_treatment_criteria_method": "Physician Assessed Response Criteria",
            "status_of_treatment": "Not applicable",
            "submitter_treatment_id": "TREATMENT_0030",
            "submitter_primary_diagnosis_id": "PRIMARY_DIAGNOSIS_016",
            "program_id": "SYNTHETIC-2",
            "submitter_donor_id": "DONOR_011",
            "treatment_end_date": {
                "month_interval": 87,
                "day_interval": 2610
            },
            "treatment_setting": "Induction",
            "treatment_start_date": {
                "month_interval": 25,
                "day_interval": 750
            },
            "treatment_type": "Photodynamic therapy"
        },
        {
            "days_per_cycle": 2,
            "is_primary_treatment": "No",
            "line_of_treatment": 4,
            "number_of_cycles": 4,
            "response_to_treatment": "Complete remission with incomplete hematologic recovery (CRi)",
            "response_to_treatment_criteria_method": "Physician Assessed Response Criteria",
            "status_of_treatment": "Not applicable",
            "submitter_treatment_id": "TREATMENT_0031",
            "submitter_primary_diagnosis_id": "PRIMARY_DIAGNOSIS_016",
            "program_id": "SYNTHETIC-2",
            "submitter_donor_id": "DONOR_011",
            "treatment_end_date": {
                "month_interval": 87,
                "day_interval": 2610
            },
            "treatment_setting": "Induction",
            "treatment_start_date": {
                "month_interval": 25,
                "day_interval": 750
            },
            "treatment_type": "Stem cell transplant"
        },
        {
            "days_per_cycle": 2,
            "is_primary_treatment": "No",
            "line_of_treatment": 4,
            "number_of_cycles": 4,
            "response_to_treatment": "Complete remission with incomplete hematologic recovery (CRi)",
            "response_to_treatment_criteria_method": "Physician Assessed Response Criteria",
            "status_of_treatment": "Not applicable",
            "submitter_treatment_id": "TREATMENT_0033",
            "submitter_primary_diagnosis_id": "PRIMARY_DIAGNOSIS_016",
            "program_id": "SYNTHETIC-2",
            "submitter_donor_id": "DONOR_011",
            "treatment_end_date": {
                "month_interval": 87,
                "day_interval": 2610
            },
            "treatment_setting": "Induction",
            "treatment_start_date": {
                "month_interval": 25,
                "day_interval": 750
            },
            "treatment_type": "Stem cell transplant"
        },
        {
            "days_per_cycle": 2,
            "is_primary_treatment": "No",
            "line_of_treatment": 4,
            "number_of_cycles": 4,
            "response_to_treatment": "Complete remission with incomplete hematologic recovery (CRi)",
            "response_to_treatment_criteria_method": "Physician Assessed Response Criteria",
            "status_of_treatment": "Not applicable",
            "submitter_treatment_id": "TREATMENT_0032",
            "submitter_primary_diagnosis_id": "PRIMARY_DIAGNOSIS_016",
            "program_id": "SYNTHETIC-2",
            "submitter_donor_id": "DONOR_011",
            "treatment_end_date": {
                "month_interval": 87,
                "day_interval": 2610
            },
            "treatment_setting": "Induction",
            "treatment_start_date": {
                "month_interval": 25,
                "day_interval": 750
            },
            "treatment_type": "Surgery"
        },
        {
            "submitter_treatment_id": "TREATMENT_1a",
            "submitter_donor_id": "DONOR_000",
            "submitter_primary_diagnosis_id": "PRIMARY_DIAGNOSIS_1a",
            "program_id": "SYNTHETIC-2"
        },
        {
            "submitter_treatment_id": "TREATMENT_2a",
            "submitter_donor_id": "DONOR_000",
            "submitter_primary_diagnosis_id": "PRIMARY_DIAGNOSIS_1a",
            "program_id": "SYNTHETIC-2"
        }
    ]
    return treatments


def add_chemo():
    chemos = [
        {
            "submitter_treatment_id": "TREATMENT_2a",
            "actual_cumulative_drug_dose": 60,
            "submitter_donor_id": "DONOR_000",
            "program_id": "SYNTHETIC-2"
        },
        {
            "submitter_treatment_id": "TREATMENT_2a",
            "prescribed_cumulative_drug_dose": 4600,
            "submitter_donor_id": "DONOR_000",
            "program_id": "SYNTHETIC-2"
        },
        {
            "submitter_treatment_id": "TREATMENT_1a",
            "drug_name": "Gemcitabine",
            "drug_reference_database": "NCI Thesaurus",
            "submitter_donor_id": "DONOR_000",
            "program_id": "SYNTHETIC-2"
        }
    ]
    return chemos


def add_followups():
    followups = [
        {
            "submitter_treatment_id": "TREATMENT_0025",
            "submitter_follow_up_id": "FOLLOW_UP_0025",
            "program_id": "SYNTHETIC-2",
            "submitter_donor_id": "DONOR_011",
            "anatomic_site_progression_or_recurrence": ["C00.9", "C01.9"]
        },
        {
            "submitter_follow_up_id": "FOLLOW_UP_2a",
            "submitter_treatment_id": "TREATMENT_1a",
            "submitter_primary_diagnosis_id": "PRIMARY_DIAGNOSIS_1a",
            "submitter_donor_id": "DONOR_000",
            "program_id": "SYNTHETIC-2"
        },
        {
            "submitter_follow_up_id": "FOLLOW_UP_1a",

            "submitter_treatment_id": "TREATMENT_1a",
            "submitter_donor_id": "DONOR_000",
            "program_id": "SYNTHETIC-2"
        },
        {
            "submitter_follow_up_id": "FOLLOW_UP_3a",
            "submitter_donor_id": "DONOR_000",
            "program_id": "SYNTHETIC-2"
        }
    ]
    return followups


def add_comorbidities():
    comorbidities = [{
        "age_at_comorbidity_diagnosis": 56,
        "comorbidity_type_code": "C43.9",
        "submitter_donor_id": "DONOR_000",
        "program_id": "SYNTHETIC-2"
    },
        {
            "comorbidity_treatment": "Photodynamic therapy",
            "submitter_donor_id": "DONOR_000",
            "program_id": "SYNTHETIC-2"
        },
        {
            "prior_malignancy": "Yes",
            "submitter_donor_id": "DONOR_000",
            "program_id": "SYNTHETIC-2"
        }

    ]
    return comorbidities


def add_exposures():
    exposures = [
        {
            "tobacco_smoking_status": "Current smoker",
            "submitter_donor_id": "DONOR_000",
            "program_id": "SYNTHETIC-2"
        },
        {
            "pack_years_smoked": 72,
            "submitter_donor_id": "DONOR_000",
            "program_id": "SYNTHETIC-2"
        },
        {
            "program_id": "SYNTHETIC-2",
            "submitter_donor_id": "DONOR_011",
            "tobacco_type": ["Cigar", "Cigarettes", "Roll-ups", "Pipe"]
        }
    ]
    return exposures


def add_biomarkers():
    biomarkers = [
        {
            "test_date": {
                "month_interval": 49,
                "day_interval": 1470,

            },
            "submitter_donor_id": "DONOR_000",
            "program_id": "SYNTHETIC-2"
        },
        {
            "ca125": 109,
            "submitter_donor_id": "DONOR_000",
            "program_id": "SYNTHETIC-2"
        },
        {
            "hpv_strain": [
                "HPV52",
                "HPV58",
                "HPV35"
            ],
            "submitter_donor_id": "DONOR_000",
            "program_id": "SYNTHETIC-2"
        },
        {
            "er_status": "Not applicable",
            "her2_ihc_status": "Cannot be determined",
            "her2_ish_status": "Positive",
            "submitter_donor_id": "DONOR_000",
            "program_id": "SYNTHETIC-2"
        },
        {
            "cea": 5,
            "submitter_donor_id": "DONOR_000",
            "program_id": "SYNTHETIC-2"
        },
        {
            "program_id": "SYNTHETIC-2",
            "submitter_donor_id": "DONOR_011",
            "hpv_strain": [
                "HPV16",
                "HPV68",
                "HPV31",
                "HPV59"
            ],
        }
    ]
    return biomarkers


def add_hormone_therapies():
    hormone_therapies = [
        {
            "submitter_treatment_id": "TREATMENT_2a",
            "drug_name": "Cabergoline",
            "submitter_donor_id": "DONOR_000",
            "program_id": "SYNTHETIC-2"
        },
        {
            "submitter_treatment_id": "TREATMENT_2a",
            "drug_name": "Lutetium Lu 177 Dotatate",
            "drug_reference_identifier": "557845",
            "submitter_donor_id": "DONOR_000",
            "program_id": "SYNTHETIC-2"
        },
        {
            "submitter_treatment_id": "TREATMENT_1a",
            "prescribed_cumulative_drug_dose": 106,
            "actual_cumulative_drug_dose": 85,
            "submitter_donor_id": "DONOR_000",
            "program_id": "SYNTHETIC-2"
        }
    ]
    return hormone_therapies


def add_immunotherapies():
    immunotherapies = [
        {
            "submitter_treatment_id": "TREATMENT_2a",
            "immunotherapy_type": "Other immunomodulatory substances",
            "submitter_donor_id": "DONOR_000",
            "program_id": "SYNTHETIC-2"
        },
        {
            "submitter_treatment_id": "TREATMENT_2a",
            "drug_name": "Nivolumab",
            "drug_reference_identifier": "987654",
            "drug_reference_database": "PubChem",
            "submitter_donor_id": "DONOR_000",
            "program_id": "SYNTHETIC-2"
        },
        {
            "submitter_treatment_id": "TREATMENT_1a",
            "immunotherapy_drug_dose_units": "mg/kg",
            "submitter_donor_id": "DONOR_000",
            "program_id": "SYNTHETIC-2"
        }
    ]
    return immunotherapies


def add_radiations():
    radiations = [
        {
            "submitter_treatment_id": "TREATMENT_2a",
            "radiation_therapy_type": "Internal",
            "submitter_donor_id": "DONOR_000",
            "program_id": "SYNTHETIC-2"
        },
        {
            "submitter_treatment_id": "TREATMENT_2a",
            "radiation_therapy_modality": "Teleradiotherapy neutrons (procedure)",
            "submitter_donor_id": "DONOR_000",
            "program_id": "SYNTHETIC-2"
        },
        {
            "submitter_treatment_id": "TREATMENT_1a",
            "anatomical_site_irradiated": "Right Maxilla",
            "submitter_donor_id": "DONOR_000",
            "program_id": "SYNTHETIC-2"
        }
    ]
    return radiations


def add_surgeries():
    surgeries = [
        {
            "submitter_treatment_id": "TREATMENT_0025",
            "program_id": "SYNTHETIC-2",
            "submitter_donor_id": "DONOR_011",
            "margin_types_involved": ["Proximal margin", "Distal margin"],
            "margin_types_not_involved": ["Common bile duct margin", "Circumferential resection margin"],
            "margin_types_not_assessed": ["Unknown", "Not applicable"]
        },
        {
            "submitter_treatment_id": "TREATMENT_2a",
            "submitter_specimen_id": "SPECIMEN_1a",
            "surgery_type": "Wide Local Excision",
            "submitter_donor_id": "DONOR_000",
            "program_id": "SYNTHETIC-2"
        },
        {
            "submitter_treatment_id": "TREATMENT_2a",
            "submitter_specimen_id": "SPECIMEN_1a",
            "surgery_site": "C11",
            "submitter_donor_id": "DONOR_000",
            "program_id": "SYNTHETIC-2"
        },
        {
            "submitter_treatment_id": "TREATMENT_1a",
            "submitter_specimen_id": "SPECIMEN_1a",
            "surgery_location": "Metastatic",
            "submitter_donor_id": "DONOR_000",
            "program_id": "SYNTHETIC-2"
        }
    ]
    return surgeries


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


def process_objects(filename, df):
    match filename:
        case "Donor.json":
            return process_donor(df)
        case "Comorbidity.json":
            return process_comorbidity(df)
        case "Exposure.json":
            return process_exposure(df)
        case "FollowUp.json":
            return process_followups(df)
        case _:
            return df


def convert_to_csv(size, input_path):
    # Get the absolute path to the synthetic data folder
    repo_dir = os.path.dirname(os.path.dirname(__file__))
    synthetic_data_folder = input_path
    output_dir = os.path.join(repo_dir, f"{size}_dataset_csv/raw_data")
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Iterate through all JSON files in the synthetic_data_folder
    print(f"Processing json files from {synthetic_data_folder}...")
    for filename in os.listdir(synthetic_data_folder):
        if filename.endswith('.json') and not filename.startswith("Program"):
            print(filename)
            json_file_path = os.path.join(synthetic_data_folder, filename)
            with open(json_file_path, 'r') as f:
                data = json.load(f)
                extra_objects = add_objects(filename)
                if extra_objects:
                    data.extend(extra_objects)
                df = pd.DataFrame(data)
                df = process_objects(filename, df)


                # Concatenate values for all columns with list-type values
                for column in df.columns:
                    if df[column].apply(lambda x: isinstance(x, list)).any():
                        df[column] = df[column].apply(lambda x: '|'.join(x) if isinstance(x, list) else x)

                # Save the DataFrame to a CSV file in the output directory
                output_csv_file = os.path.join(output_dir, f"{filename.replace('.json', '.csv')}")
                df.to_csv(output_csv_file, index=False)
    print("All done!")


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
