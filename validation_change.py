import os
import pandas as pd
import argparse


def process_csv(path, filename):
    script_dir = os.path.dirname(__file__)
    file = os.path.join(script_dir, f"{path}/{filename}")

    # Read the CSV file into a DataFrame
    df = pd.read_csv(file)

    # Modify the DataFrame using the specified process function
    if filename == "Donor.csv":
        df = process_donor(df)
    elif filename == "Comorbidity.csv":
        df = process_comorbidity(df)
    elif filename == "Exposure.csv":
        df = process_exposure(df)

    # Save the modified DataFrame to a new CSV file
    df.to_csv(file, index=False)

def process_donor(df):
    if 'is_deceased' in df.columns and 'cause_of_death' in df.columns:
        condition = (df['is_deceased'] == False) & df['cause_of_death'].notna()
        df.loc[condition, 'cause_of_death'] = ""
        condition = df['is_deceased'].isna() & df['cause_of_death'].notna()
        print(df['is_deceased'].isna())
        df.loc[condition, 'cause_of_death'] = ""
        condition = (df['is_deceased'] == True) & df['lost_to_followup_reason'].notna()
        df.loc[condition, 'lost_to_followup_reason'] = ""
        condition = (df['is_deceased'] == True) & df['lost_to_followup_after_clinical_event_identifier'].notna()
        df.loc[condition, 'lost_to_followup_after_clinical_event_identifier'] = ""
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
    return df

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--size',
        type=str,
        default='s',
        choices=['s', 'm', 'l'],
        help="Size of the synthetic dataset to modify, options: 's' for small, 'm' for medium, 'l' for large (default: small)"
    )
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    size_mapping = {'s': 'small', 'm': 'medium', 'l': 'large'}
    path = f"{size_mapping[args.size]}_dataset_csv"
    process_csv(path, "Donor.csv")
    process_csv(path, "Comorbidity.csv")
    process_csv(path, "Exposure.csv")
    process_csv(path, "FollowUp.csv")

if __name__ == "__main__":
    main()
