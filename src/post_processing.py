"""
Processing methods to ensure that synthetic data meets conditional requirements of the model.
"""
import ast
import os
import json
import math

import pandas as pd


def modify_date_interval(interval, size, resolution="month"):
    """ modify a date interval and return the modified date interval

    Args:
        interval: the date_interval to be modified
        size: the amount to manipulate, negative or positive
        resolution: whether to manipulate based on the day or month

    Returns:
        A date interval dict with modified values, or the original interval if none
    """
    try:
        if interval is None:
            return interval
        if "str" in str(type(interval)):
            interval = ast.literal_eval(interval)
        if "day_interval" in interval.keys() and resolution == "day":
            shifted_day = int(interval["day_interval"] + size)
            if shifted_day >= 0:
                modified_interval = {"day_interval": shifted_day, "month_interval": int(math.floor(shifted_day / 30))}
            else:
                modified_interval = {"day_interval": 0, "month_interval": 0}
            return modified_interval
        elif resolution == "month":
            shifted_month = int(interval["month_interval"] + size)
            if shifted_month >= 0:
                modified_interval = {"month_interval": shifted_month}
            else:
                modified_interval = {"month_interval": 0}
            if "day_interval" in interval:
                modified_interval["day_interval"] = int(modified_interval["month_interval"] * 30)
            return modified_interval
        else:
            return interval
    except AttributeError:
        return interval


def grab_month_interval(date_interval):
    if "str" in str(type(date_interval)) and date_interval != '':
        date_interval = ast.literal_eval(date_interval)
    try:
        return int(date_interval["month_interval"])
    except TypeError:
        return None


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
    condition = df['date_resolution'].isna() & df.date_of_birth.astype('str').str.contains('day_interval')
    df.loc[condition, 'date_resolution'] = "month"
    condition = df['date_resolution'].isna() & df.date_of_birth.astype('str').str.contains('day_interval')
    df.loc[condition, 'date_resolution'] = "day"
    if 'date_of_death' in df.columns:
        df['death_month_interval'] = df['date_of_death'].apply(lambda x: grab_month_interval(x))
        condition = df['death_month_interval'] < 10
        df.loc[condition, 'date_of_death'] = "{'month_interval': 20, 'day_interval': 600}"
        df = df.drop(columns=['death_month_interval'])
    return df


def process_comorbidity(df):
    if 'prior_malignancy' in df.columns and 'laterality_of_prior_malignancy' in df.columns:
        condition = (df['prior_malignancy'] != "Yes") & df['laterality_of_prior_malignancy'].notna()
        df.loc[condition, 'laterality_of_prior_malignancy'] = ""
    return df


def process_exposure(df):
    if 'tobacco_smoking_status' in df.columns and 'tobacco_type' in df.columns:
        condition = df['tobacco_smoking_status'].isin(['Smoking history not documented',
                                                       'Lifelong non-smoker (<100 cigarettes smoked in lifetime)',
                                                       'Not applicable'])
        df.loc[condition, 'tobacco_type'] = ""
        condition = df['tobacco_smoking_status'].isin(['Smoking history not documented',
                                                       'Lifelong non-smoker (<100 cigarettes smoked in lifetime)',
                                                       'Not applicable'])
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


def process_primary_diagnoses(df, output_dir):
    # Ensure there is always a 0 date primary diagnosis
    df['row_num'] = df.groupby(['submitter_donor_id']).cumcount()
    df.loc[df.row_num == 0, 'date_of_diagnosis'] = \
        "{'month_interval': 0, 'day_interval': 0}"
    df.loc[df.submitter_donor_id == 'DONOR_NULL', 'date_of_diagnosis'] = None
    # diagnosis should be between date of birth and date of death, must be >= 0
    try:
        donor_csv_file_path = os.path.join(output_dir, "Donor.csv")
        donor_df = pd.read_csv(donor_csv_file_path, usecols=["submitter_donor_id", "date_of_death"])
        donor_df['death_month_interval'] = donor_df['date_of_death'].apply(lambda x: grab_month_interval(x))
        df['diagnosis_month_interval'] = df['date_of_diagnosis'].apply(lambda x: grab_month_interval(x))
        df['diagnosis_month_interval'] = df['date_of_diagnosis'].apply(lambda x: grab_month_interval(x))
        df = pd.merge(df, donor_df, on='submitter_donor_id')
        df["month_diff"] = df['death_month_interval'] - df['diagnosis_month_interval']
        condition = df['month_diff'] < 0
        df.loc[condition, 'date_of_diagnosis'] = (df.loc[condition].
                                                  apply(lambda x: modify_date_interval(x['date_of_diagnosis'],
                                                                                       size=(x['month_diff'] - 5),
                                                                                       resolution="month"), axis=1))
        df = df.drop(columns=['month_diff', 'row_num', 'death_month_interval', 'diagnosis_month_interval', 'date_of_death'])
    except KeyError as e:
        print(e)
    except TypeError as e:
        print(e)
    return df


def process_treatments(df, output_dir):
    df["start_month_interval"] = df["treatment_start_date"].apply(lambda x: grab_month_interval(x))
    df["end_month_interval"] = df["treatment_end_date"].apply(lambda x: grab_month_interval(x))
    # treatment dates need to be compatible with diagnosis dates, death date, birth date
    donor_csv_file_path = os.path.join(output_dir, "Donor.csv")
    donor_df = pd.read_csv(donor_csv_file_path)
    donor_df_select = donor_df[['submitter_donor_id', 'date_of_death', 'date_of_birth']]
    donor_df_select.insert(0, column="death_month_interval",
                           value=donor_df_select.date_of_death.apply(lambda x: grab_month_interval(x)))
    donor_df_select.insert(0, column="birth_month_interval",
                           value=donor_df_select.date_of_birth.apply(lambda x: grab_month_interval(x)))
    diagnosis_csv_file_path = os.path.join(output_dir, "PrimaryDiagnosis.csv")
    diagnosis_df = pd.read_csv(diagnosis_csv_file_path, usecols=['submitter_primary_diagnosis_id', 'date_of_diagnosis'])
    diagnosis_df['diagnosis_month_interval'] = diagnosis_df['date_of_diagnosis'].apply(lambda x: grab_month_interval(x))
    df = pd.merge(df, diagnosis_df, on='submitter_primary_diagnosis_id', how='left')
    df = pd.merge(df, donor_df_select, on='submitter_donor_id', how='left')
    # treatment start after diagnosis
    df["start_diagnosis_diff"] = df['diagnosis_month_interval'] - df['start_month_interval']
    condition = df["start_diagnosis_diff"] > 0
    df.loc[condition, 'treatment_start_date'] = (df.loc[condition].
                                                 apply(lambda x: modify_date_interval(x['treatment_start_date'],
                                                                                      size=(x["start_diagnosis_diff"] + 1),
                                                                                      resolution="month"), axis=1))
    df["start_month_interval"] = df["treatment_start_date"].apply(lambda x: grab_month_interval(x))

    # treatment start not after death
    df["start_death_diff"] = df['death_month_interval'] - df['start_month_interval']
    condition = df["start_death_diff"] < 0
    df.loc[condition, 'treatment_start_date'] = (df.loc[condition].
                                                 apply(lambda x: modify_date_interval(x['treatment_start_date'],
                                                                                      size=(x["start_death_diff"] -
                                                                                            int(math.floor(x["start_death_diff"]/2))),
                                                                                      resolution="month"), axis=1))
    df["start_month_interval"] = df["treatment_start_date"].apply(lambda x: grab_month_interval(x))

    # treatment end after treatment start
    df['start_end_diff'] = df['start_month_interval'] - df['end_month_interval']
    condition = df['start_end_diff'] > 0
    df.loc[condition, 'treatment_end_date'] = (df.loc[condition].
                                               apply(lambda x: modify_date_interval(x['treatment_end_date'],
                                                                                    size=x['start_end_diff'] + 1,
                                                                                    resolution="month"), axis=1))
    df["end_month_interval"] = df["treatment_end_date"].apply(lambda x: grab_month_interval(x))

    # treatment end after diagnosis
    df["end_diagnosis_diff"] = df['diagnosis_month_interval'] - df['end_month_interval']
    condition = df["end_diagnosis_diff"] > 0
    df.loc[condition, 'treatment_end_date'] = (df.loc[condition].
                                                 apply(lambda x: modify_date_interval(x['treatment_end_date'],
                                                                                      size=(x["end_diagnosis_diff"] + 6),
                                                                                      resolution="month"), axis=1))
    df["end_month_interval"] = df["treatment_end_date"].apply(lambda x: grab_month_interval(x))

    # treatment end before death, if after death, shift the death date longer
    df["end_death_diff"] = df['end_month_interval'] - df['death_month_interval']
    condition = df["end_death_diff"] > 0
    death_shift = df.loc[condition, ['submitter_donor_id', 'end_death_diff']].sort_values('end_death_diff', ascending=False).drop_duplicates(['submitter_donor_id'])
    condition = donor_df.submitter_donor_id.isin(death_shift.submitter_donor_id)
    donor_df = pd.merge(donor_df, death_shift, on='submitter_donor_id', how="left")
    donor_df.loc[condition, 'date_of_death'] = (
        donor_df.loc[condition].apply(lambda x: modify_date_interval(x['date_of_death'],
                                                                     size=(x['end_death_diff'] + 10),
                                                                     resolution="month"), axis=1))
    donor_df = donor_df.drop(columns=['end_death_diff'])
    output_csv_file = os.path.join(output_dir, "Donor.csv")
    donor_df.to_csv(output_csv_file, index=False)

    df = df.drop(columns=['start_end_diff', 'end_month_interval', 'start_month_interval',
                          'diagnosis_month_interval', 'death_month_interval', 'birth_month_interval',
                          'end_death_diff', 'start_diagnosis_diff', 'start_death_diff', 'date_of_death',
                          'date_of_birth', 'date_of_diagnosis', 'end_diagnosis_diff'])
    return df


def process_objects(filename, df, output_dir):
    match filename:
        case "Donor.json":
            return process_donor(df)
        case "Comorbidity.json":
            return process_comorbidity(df)
        case "Exposure.json":
            return process_exposure(df)
        case "FollowUp.json":
            return process_followups(df)
        case "PrimaryDiagnosis.json":
            return process_primary_diagnoses(df, output_dir)
        case "Treatment.json":
            return process_treatments(df, output_dir)
        case _:
            return df
