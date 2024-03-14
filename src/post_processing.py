"""
Processing methods to ensure that synthetic data meets conditional requirements of the model.
"""


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
