"""
File with extra donor information to test specific functionality of the stack.
"""


def add_donors():
    donors = [
        {
            # every field except followups as is_deceased
            "cause_of_death": "Unknown",
            "date_of_birth": {
                "month_interval": -700,
                "day_interval": -21292
            },
            "gender": "Woman",
            "is_deceased": True,
            "date_of_death": {
                "month_interval": 120,
                "day_interval": 3653
            },
            "primary_site": [
                "Floor of mouth",
                "Other and unspecified parts of mouth"
            ],
            "program_id": "SYNTHETIC-2",
            "submitter_donor_id": "DONOR_ALL_02",
            "sex_at_birth": "Other",
        },
        {
            # every field except date_of_death as not is_deceased
            "date_of_birth": {
                "month_interval": -700,
                "day_interval": -21292
            },
            "gender": "Woman",
            "is_deceased": False,
            "primary_site": [
                "Floor of mouth",
                "Other and unspecified parts of mouth"
            ],
            "program_id": "SYNTHETIC-2",
            "submitter_donor_id": "DONOR_ALL_01",
            "sex_at_birth": "Other",
            "lost_to_followup_after_clinical_event_identifier": "TREATMENT_0033",
            "lost_to_followup_reason": "Withdrew from study",
            "date_alive_after_lost_to_followup": {
                "month_interval": 90,
                "day_interval": 2700
            }
        },
        {
            "submitter_donor_id": "DONOR_NULL",
            "program_id": "SYNTHETIC-2"
        }]
    return donors


def add_pds():
    pds = [
        {
            # all valid fields with a value
            "basis_of_diagnosis": "Specific tumour markers",
            "cancer_type_code": "C67.6",
            "clinical_m_category": "M1a(1)",
            "clinical_n_category": "N0b (no biopsy)",
            "clinical_t_category": "TX",
            "clinical_tumour_staging_system": "AJCC 8th edition",
            "clinical_stage_group": "Stage II",
            "date_of_diagnosis": {
                "month_interval": 0,
                "day_interval": 0
            },
            "laterality": "Right",
            "lymph_nodes_examined_method": "Imaging",
            "lymph_nodes_examined_status": "No lymph nodes found in resected specimen",
            "number_lymph_nodes_positive": 10,
            "submitter_primary_diagnosis_id": "PRIMARY_DIAGNOSIS_ALL_02",
            "program_id": "SYNTHETIC-2",
            "submitter_donor_id": "DONOR_ALL_02"
        },
        {
            # all valid fields with a value
            "basis_of_diagnosis": "Specific tumour markers",
            "cancer_type_code": "C67.6",
            "clinical_m_category": "M1a(1)",
            "clinical_n_category": "N0b (no biopsy)",
            "clinical_t_category": "TX",
            "clinical_tumour_staging_system": "AJCC 8th edition",
            "clinical_stage_group": "Stage II",
            "date_of_diagnosis": {
                "month_interval": 0,
                "day_interval": 0
            },
            "laterality": "Right",
            "lymph_nodes_examined_method": "Imaging",
            "lymph_nodes_examined_status": "No lymph nodes found in resected specimen",
            "number_lymph_nodes_positive": 10,
            "submitter_primary_diagnosis_id": "PRIMARY_DIAGNOSIS_ALL_01",
            "program_id": "SYNTHETIC-2",
            "submitter_donor_id": "DONOR_ALL_01"
        },
        {
            "submitter_primary_diagnosis_id": "PRIMARY_DIAGNOSIS_NULL_01",
            "submitter_donor_id": "DONOR_NULL",
            "program_id": "SYNTHETIC-2"
        }]
    return pds


def add_specimens():
    specimens = [
        {
            # All specimen fields filled in
            "pathological_m_category": "M1e",
            "pathological_n_category": "N0a",
            "pathological_stage_group": "Stage IIIC",
            "pathological_t_category": "Tis",
            "pathological_tumour_staging_system": "AJCC 8th edition",
            "percent_tumour_cells_range": "0-19%",
            "percent_tumour_cells_measurement_method": "Pathology estimate by percent nuclei",
            "reference_pathology_confirmed_tumour_presence": "No",
            "reference_pathology_confirmed_diagnosis": "Not done",
            "specimen_anatomic_location": "C43.9",
            "specimen_collection_date": {
                "month_interval": 20,
                "day_interval": 600
            },
            "specimen_laterality": "Right",
            "specimen_processing": "Cryopreservation in liquid nitrogen (dead tissue)",
            "specimen_storage": "Frozen in -70 freezer",
            "program_id": "SYNTHETIC-2",
            "submitter_specimen_id": "SPECIMEN_ALL_02",
            "submitter_primary_diagnosis_id": "PRIMARY_DIAGNOSIS_ALL_02",
            "submitter_donor_id": "DONOR_ALL_02",
            "tumour_grade": "Low",
            "tumour_grading_system": "Scarff-Bloom-Richardson grading system",
            "tumour_histological_type": "8962/1"
        },
        {
            # All specimen fields filled in
            "pathological_m_category": "M1e",
            "pathological_n_category": "N0a",
            "pathological_stage_group": "Stage IIIC",
            "pathological_t_category": "Tis",
            "pathological_tumour_staging_system": "AJCC 8th edition",
            "percent_tumour_cells_range": "0-19%",
            "percent_tumour_cells_measurement_method": "Pathology estimate by percent nuclei",
            "reference_pathology_confirmed_tumour_presence": "No",
            "reference_pathology_confirmed_diagnosis": "Not done",
            "specimen_anatomic_location": "C43.9",
            "specimen_collection_date": {
                "month_interval": 20,
                "day_interval": 600
            },
            "specimen_laterality": "Right",
            "specimen_processing": "Cryopreservation in liquid nitrogen (dead tissue)",
            "specimen_storage": "Frozen in -70 freezer",
            "program_id": "SYNTHETIC-2",
            "submitter_specimen_id": "SPECIMEN_ALL_01",
            "submitter_primary_diagnosis_id": "PRIMARY_DIAGNOSIS_ALL_01",
            "submitter_donor_id": "DONOR_ALL_01",
            "tumour_grade": "Low",
            "tumour_grading_system": "Scarff-Bloom-Richardson grading system",
            "tumour_histological_type": "8962/1"
        },
        {
            "submitter_specimen_id": "SPECIMEN_NULL_01",
            "submitter_donor_id": "DONOR_NULL",
            "submitter_primary_diagnosis_id": "PRIMARY_DIAGNOSIS_NULL_01",
            "program_id": "SYNTHETIC-2"
        }]
    return specimens


def add_samples():
    samples = [
        {
            "sample_type": "Total DNA",
            "specimen_tissue_source": "Solid tissue",
            "specimen_type": "Primary tumour - additional new primary",
            "submitter_sample_id": "SAMPLE_REGISTRATION_ALL_02",
            "tumour_normal_designation": "Tumour",
            "program_id": "SYNTHETIC-2",
            "submitter_donor_id": "DONOR_ALL_02",
            "submitter_specimen_id": "SPECIMEN_ALL_02",
        },
        {
            "sample_type": "Total DNA",
            "specimen_tissue_source": "Solid tissue",
            "specimen_type": "Primary tumour - additional new primary",
            "submitter_sample_id": "SAMPLE_REGISTRATION_ALL_01",
            "tumour_normal_designation": "Tumour",
            "program_id": "SYNTHETIC-2",
            "submitter_donor_id": "DONOR_ALL_01",
            "submitter_specimen_id": "SPECIMEN_ALL_01",
        },
        {
            "submitter_sample_id": "SAMPLE_REGISTRATION_NULL_01",
            "submitter_specimen_id": "SPECIMEN_NULL_01",
            "submitter_donor_id": "DONOR_NULL",
            "program_id": "SYNTHETIC-2"
        },
        {
            "submitter_sample_id": "SAMPLE_REGISTRATION_NULL_02",
            "submitter_specimen_id": "SPECIMEN_NULL_01",
            "submitter_donor_id": "DONOR_NULL",
            "program_id": "SYNTHETIC-2"
        }
    ]
    return samples


def add_treatments():
    treatments = [
        {   # All fields with at least one valid value
            "days_per_cycle": 2,
            "is_primary_treatment": "No",
            "line_of_treatment": 4,
            "number_of_cycles": 4,
            "response_to_treatment": "Complete remission with incomplete hematologic recovery (CRi)",
            "response_to_treatment_criteria_method": "Physician Assessed Response Criteria",
            "status_of_treatment": "Treatment completed as prescribed",
            "submitter_treatment_id": "TREATMENT_ALL_01",
            "submitter_primary_diagnosis_id": "PRIMARY_DIAGNOSIS_ALL_01",
            "program_id": "SYNTHETIC-2",
            "submitter_donor_id": "DONOR_ALL_01",
            "treatment_intent": "Curative",
            "treatment_end_date": {
                "month_interval": 87,
                "day_interval": 2610
            },
            "treatment_setting": "Induction",
            "treatment_start_date": {
                "month_interval": 25,
                "day_interval": 750
            },
            "treatment_type": ["Immunotherapy", "Surgery", "Chemotherapy", "Hormonal therapy", "Radiation therapy"]
        },
        {  # All fields with at least one valid value
            "days_per_cycle": 2,
            "is_primary_treatment": "No",
            "line_of_treatment": 4,
            "number_of_cycles": 4,
            "response_to_treatment": "Complete remission with incomplete hematologic recovery (CRi)",
            "response_to_treatment_criteria_method": "Physician Assessed Response Criteria",
            "status_of_treatment": "Treatment completed as prescribed",
            "submitter_treatment_id": "TREATMENT_ALL_02",
            "submitter_primary_diagnosis_id": "PRIMARY_DIAGNOSIS_ALL_02",
            "program_id": "SYNTHETIC-2",
            "submitter_donor_id": "DONOR_ALL_02",
            "treatment_intent": "Curative",
            "treatment_end_date": {
                "month_interval": 87,
                "day_interval": 2610
            },
            "treatment_setting": "Induction",
            "treatment_start_date": {
                "month_interval": 25,
                "day_interval": 750
            },
            "treatment_type": ["Immunotherapy", "Surgery", "Chemotherapy", "Hormonal therapy", "Radiation therapy"]
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
            "submitter_primary_diagnosis_id": "PRIMARY_DIAGNOSIS_ALL_01",
            "program_id": "SYNTHETIC-2",
            "submitter_donor_id": "DONOR_ALL_01",
            "treatment_end_date": {
                "month_interval": 87,
                "day_interval": 2610
            },
            "treatment_setting": "Induction",
            "treatment_start_date": {
                "month_interval": 25,
                "day_interval": 750
            },
            "treatment_type": "Radiation therapy"
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
            "submitter_primary_diagnosis_id": "PRIMARY_DIAGNOSIS_ALL_01",
            "program_id": "SYNTHETIC-2",
            "submitter_donor_id": "DONOR_ALL_01",
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
            "submitter_treatment_id": "TREATMENT_0034",
            "submitter_primary_diagnosis_id": "PRIMARY_DIAGNOSIS_ALL_01",
            "program_id": "SYNTHETIC-2",
            "submitter_donor_id": "DONOR_ALL_01",
            "treatment_end_date": {
                "month_interval": 87,
                "day_interval": 2610
            },
            "treatment_setting": "Induction",
            "treatment_start_date": {
                "month_interval": 25,
                "day_interval": 750
            },
            "treatment_type": "Bone marrow transplant"
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
            "submitter_primary_diagnosis_id": "PRIMARY_DIAGNOSIS_ALL_01",
            "program_id": "SYNTHETIC-2",
            "submitter_donor_id": "DONOR_ALL_01",
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
            "submitter_primary_diagnosis_id": "PRIMARY_DIAGNOSIS_ALL_01",
            "program_id": "SYNTHETIC-2",
            "submitter_donor_id": "DONOR_ALL_01",
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
            "submitter_primary_diagnosis_id": "PRIMARY_DIAGNOSIS_ALL_01",
            "program_id": "SYNTHETIC-2",
            "submitter_donor_id": "DONOR_ALL_01",
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
            "submitter_primary_diagnosis_id": "PRIMARY_DIAGNOSIS_ALL_01",
            "program_id": "SYNTHETIC-2",
            "submitter_donor_id": "DONOR_ALL_01",
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
            "submitter_primary_diagnosis_id": "PRIMARY_DIAGNOSIS_ALL_01",
            "program_id": "SYNTHETIC-2",
            "submitter_donor_id": "DONOR_ALL_01",
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
            "submitter_treatment_id": "TREATMENT_NULL_01",
            "submitter_donor_id": "DONOR_NULL",
            "submitter_primary_diagnosis_id": "PRIMARY_DIAGNOSIS_NULL_01",
            "program_id": "SYNTHETIC-2"
        },
        {
            "submitter_treatment_id": "TREATMENT_NULL_02",
            "submitter_donor_id": "DONOR_NULL",
            "submitter_primary_diagnosis_id": "PRIMARY_DIAGNOSIS_NULL_01",
            "program_id": "SYNTHETIC-2"
        }
    ]
    return treatments


def add_chemo():
    chemos = [
        {   # All fields with valid value
            "submitter_treatment_id": "TREATMENT_ALL_01",
            "submitter_primary_diagnosis_id": "PRIMARY_DIAGNOSIS_ALL_01",
            "program_id": "SYNTHETIC-2",
            "submitter_donor_id": "DONOR_ALL_01",
            "actual_cumulative_drug_dose": 60,
            "prescribed_cumulative_drug_dose": 4600,
            "drug_name": "Gemcitabine",
            "drug_reference_database": "NCI Thesaurus",
            "drug_reference_identifier": "C66876",
            "chemotherapy_drug_dose_units": "mg/m2"
        },
        {  # All fields with valid value
            "submitter_treatment_id": "TREATMENT_ALL_02",
            "submitter_primary_diagnosis_id": "PRIMARY_DIAGNOSIS_ALL_02",
            "program_id": "SYNTHETIC-2",
            "submitter_donor_id": "DONOR_ALL_02",
            "actual_cumulative_drug_dose": 60,
            "prescribed_cumulative_drug_dose": 4600,
            "drug_name": "Gemcitabine",
            "drug_reference_database": "NCI Thesaurus",
            "drug_reference_identifier": "C66876",
            "chemotherapy_drug_dose_units": "mg/m2"
        },
        {
            "submitter_treatment_id": "TREATMENT_NULL_02",
            "actual_cumulative_drug_dose": 60,
            "submitter_donor_id": "DONOR_NULL",
            "program_id": "SYNTHETIC-2"
        },
        {
            "submitter_treatment_id": "TREATMENT_NULL_02",
            "prescribed_cumulative_drug_dose": 4600,
            "submitter_donor_id": "DONOR_NULL",
            "program_id": "SYNTHETIC-2"
        },
        {
            "submitter_treatment_id": "TREATMENT_NULL_01",
            "drug_name": "Gemcitabine",
            "drug_reference_database": "NCI Thesaurus",
            "submitter_donor_id": "DONOR_NULL",
            "program_id": "SYNTHETIC-2"
        }
    ]
    return chemos


def add_followups():
    followups = [
        {
            "submitter_treatment_id": "TREATMENT_ALL_01",
            "submitter_follow_up_id": "FOLLOW_UP_ALL_01",
            "program_id": "SYNTHETIC-2",
            "submitter_donor_id": "DONOR_ALL_01",
            "anatomic_site_progression_or_recurrence": ["C00.9", "C01.9"],
            "date_of_followup": {
                "month_interval": 89,
                "day_interval": 2670
            },
            "disease_status_at_followup": "Loco-regional progression",
            "relapse_type": "Local recurrence",
            "date_of_relapse": {
                "month_interval": 88,
                "day_interval": 2640
            },
            "method_of_progression_status": [
                "Laboratory data interpretation (procedure)",
                "Tumor marker measurement (procedure)"
            ],
            "recurrence_t_category": "T4b(s)",
            "recurrence_m_category": "M1a(0)",
            "recurrence_stage_group": "Stage IVES",
            "recurrence_tumour_staging_system": "AJCC 8th edition",
        },
        {
            "submitter_primary_diagnosis_id": "PRIMARY_DIAGNOSIS_ALL_01",
            "submitter_follow_up_id": "FOLLOW_UP_ALL_02",
            "program_id": "SYNTHETIC-2",
            "submitter_donor_id": "DONOR_ALL_01",
            "anatomic_site_progression_or_recurrence": ["C00.9", "C01.9"],
            "date_of_followup": {
                "month_interval": 89,
                "day_interval": 2670
            },
            "disease_status_at_followup": "Loco-regional progression",
            "relapse_type": "Local recurrence",
            "date_of_relapse": {
                "month_interval": 88,
                "day_interval": 2640
            },
            "method_of_progression_status": [
                "Laboratory data interpretation (procedure)",
                "Tumor marker measurement (procedure)"
            ],
            "recurrence_t_category": "T4b(s)",
            "recurrence_m_category": "M1a(0)",
            "recurrence_stage_group": "Stage IVES",
            "recurrence_tumour_staging_system": "AJCC 8th edition",
        },
        {
            "submitter_treatment_id": "TREATMENT_ALL_02",
            "submitter_follow_up_id": "FOLLOW_UP_ALL_03",
            "program_id": "SYNTHETIC-2",
            "submitter_donor_id": "DONOR_ALL_02",
            "anatomic_site_progression_or_recurrence": ["C00.9", "C01.9"],
            "date_of_followup": {
                "month_interval": 89,
                "day_interval": 2670
            },
            "disease_status_at_followup": "Loco-regional progression",
            "relapse_type": "Local recurrence",
            "date_of_relapse": {
                "month_interval": 88,
                "day_interval": 2640
            },
            "method_of_progression_status": [
                "Laboratory data interpretation (procedure)",
                "Tumor marker measurement (procedure)"
            ],
            "recurrence_t_category": "T4b(s)",
            "recurrence_m_category": "M1a(0)",
            "recurrence_stage_group": "Stage IVES",
            "recurrence_tumour_staging_system": "AJCC 8th edition",
        },
        {
            "submitter_follow_up_id": "FOLLOW_UP_NULL_02",
            "submitter_treatment_id": "TREATMENT_NULL_01",
            "submitter_primary_diagnosis_id": "PRIMARY_DIAGNOSIS_NULL_01",
            "submitter_donor_id": "DONOR_NULL",
            "program_id": "SYNTHETIC-2"
        },
        {
            "submitter_follow_up_id": "FOLLOW_UP_NULL_01",
            "submitter_treatment_id": "TREATMENT_NULL_01",
            "submitter_donor_id": "DONOR_NULL",
            "program_id": "SYNTHETIC-2"
        },
        {
            "submitter_follow_up_id": "FOLLOW_UP_NULL_03",
            "submitter_donor_id": "DONOR_NULL",
            "program_id": "SYNTHETIC-2"
        }
    ]
    return followups


def add_comorbidities():
    comorbidities = [
        {   # all fields filled out
            "submitter_donor_id": "DONOR_ALL_01",
            "program_id": "SYNTHETIC-2",
            "prior_malignancy": "Yes",
            "laterality_of_prior_malignancy": "Right",
            "age_at_comorbidity_diagnosis": 56,
            "comorbidity_type_code": "C43.9",
            "comorbidity_treatment_status": "No",
            "comorbidity_treatment": "Surgery"
        },
        {  # all fields filled out
            "submitter_donor_id": "DONOR_ALL_02",
            "program_id": "SYNTHETIC-2",
            "prior_malignancy": "Yes",
            "laterality_of_prior_malignancy": "Right",
            "age_at_comorbidity_diagnosis": 56,
            "comorbidity_type_code": "C43.9",
            "comorbidity_treatment_status": "No",
            "comorbidity_treatment": "Surgery"
        },
        {
            "age_at_comorbidity_diagnosis": 56,
            "comorbidity_type_code": "C43.9",
            "submitter_donor_id": "DONOR_NULL",
            "program_id": "SYNTHETIC-2"
        },
        {
            "comorbidity_treatment": "Photodynamic therapy",
            "submitter_donor_id": "DONOR_NULL",
            "program_id": "SYNTHETIC-2"
        },
        {
            "prior_malignancy": "Yes",
            "submitter_donor_id": "DONOR_NULL",
            "program_id": "SYNTHETIC-2"
        }
    ]
    return comorbidities


def add_exposures():
    exposures = [
        {
            "tobacco_smoking_status": "Current smoker",
            "submitter_donor_id": "DONOR_NULL",
            "program_id": "SYNTHETIC-2"
        },
        {
            "pack_years_smoked": 72,
            "submitter_donor_id": "DONOR_NULL",
            "program_id": "SYNTHETIC-2"
        },
        {   # all fields filled out
            "program_id": "SYNTHETIC-2",
            "submitter_donor_id": "DONOR_ALL_01",
            "tobacco_type": ["Cigar", "Cigarettes", "Roll-ups", "Pipe"],
            "tobacco_smoking_status": "Current reformed smoker for > 15 years",
            "pack_years_smoked": 100
        },
        {  # all fields filled out
            "program_id": "SYNTHETIC-2",
            "submitter_donor_id": "DONOR_ALL_02",
            "tobacco_type": ["Cigar", "Cigarettes", "Roll-ups", "Pipe"],
            "tobacco_smoking_status": "Current reformed smoker for > 15 years",
            "pack_years_smoked": 100
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
            "submitter_donor_id": "DONOR_NULL",
            "program_id": "SYNTHETIC-2"
        },
        {
            "ca125": 109,
            "submitter_donor_id": "DONOR_NULL",
            "program_id": "SYNTHETIC-2",
            "submitter_primary_diagnosis_id": "PRIMARY_DIAGNOSIS_NULL_01"
        },
        {
            "hpv_strain": [
                "HPV52",
                "HPV58",
                "HPV35"
            ],
            "submitter_donor_id": "DONOR_NULL",
            "program_id": "SYNTHETIC-2",
            "submitter_follow_up_id": "FOLLOW_UP_NULL_02"
        },
        {
            "er_status": "Not applicable",
            "her2_ihc_status": "Cannot be determined",
            "her2_ish_status": "Positive",
            "submitter_donor_id": "DONOR_NULL",
            "submitter_specimen_id": "SPECIMEN_NULL_01",
            "program_id": "SYNTHETIC-2"
        },
        {
            "cea": 5,
            "submitter_donor_id": "DONOR_NULL",
            "program_id": "SYNTHETIC-2",
            "submitter_treatment_id": "TREATMENT_NULL_02"
        },
        {   # all fields except for other submitter ids, linked to PD only
            "program_id": "SYNTHETIC-2",
            "submitter_donor_id": "DONOR_ALL_01",
            "submitter_primary_diagnosis_id": "PRIMARY_DIAGNOSIS_ALL_01",
            "test_date": {
                "month_interval": 49,
                "day_interval": 1470
            },
            "psa_level": 265,
            "ca125": 59,
            "cea": 9,
            "er_status": "Positive",
            "er_percent_positive": 89.5,
            "pr_status": "Positive",
            "pr_percent_positive": 51.0,
            "her2_ihc_status": "Negative",
            "her2_ish_status": "Cannot be determined",
            "hpv_ihc_status": "Unknown",
            "hpv_pcr_status": "Positive",
            "hpv_strain": [
                "HPV16",
                "HPV68",
                "HPV31",
                "HPV59"
            ],
        },
        {  # all fields except for other submitter ids, linked to PD only
            "program_id": "SYNTHETIC-2",
            "submitter_donor_id": "DONOR_ALL_02",
            "submitter_treatment_id": "TREATMENT_ALL_02",
            "test_date": {
                "month_interval": 49,
                "day_interval": 1470
            },
            "psa_level": 265,
            "ca125": 59,
            "cea": 9,
            "er_status": "Positive",
            "er_percent_positive": 89.5,
            "pr_status": "Positive",
            "pr_percent_positive": 51.0,
            "her2_ihc_status": "Negative",
            "her2_ish_status": "Cannot be determined",
            "hpv_ihc_status": "Unknown",
            "hpv_pcr_status": "Positive",
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
            "submitter_treatment_id": "TREATMENT_ALL_01",
            "program_id": "SYNTHETIC-2",
            "submitter_donor_id": "DONOR_ALL_01",
            "drug_name": "Cabergoline",
            "drug_reference_identifier": "54746",
            "hormone_drug_dose_units": "g/m2",
            "prescribed_cumulative_drug_dose": 142,
            "actual_cumulative_drug_dose": 81,
            "drug_reference_database": "PubChem"
        },
        {
            "submitter_treatment_id": "TREATMENT_ALL_02",
            "program_id": "SYNTHETIC-2",
            "submitter_donor_id": "DONOR_ALL_02",
            "drug_name": "Cabergoline",
            "drug_reference_identifier": "54746",
            "hormone_drug_dose_units": "g/m2",
            "prescribed_cumulative_drug_dose": 142,
            "actual_cumulative_drug_dose": 81,
            "drug_reference_database": "PubChem"
        },
        {
            "submitter_treatment_id": "TREATMENT_NULL_02",
            "drug_name": "Cabergoline",
            "submitter_donor_id": "DONOR_NULL",
            "program_id": "SYNTHETIC-2"
        },
        {
            "submitter_treatment_id": "TREATMENT_NULL_02",
            "drug_name": "Lutetium Lu 177 Dotatate",
            "drug_reference_identifier": "557845",
            "submitter_donor_id": "DONOR_NULL",
            "program_id": "SYNTHETIC-2"
        },
        {
            "submitter_treatment_id": "TREATMENT_NULL_01",
            "prescribed_cumulative_drug_dose": 106,
            "actual_cumulative_drug_dose": 85,
            "submitter_donor_id": "DONOR_NULL",
            "program_id": "SYNTHETIC-2"
        }
    ]
    return hormone_therapies


def add_immunotherapies():
    immunotherapies = [
        {
            "submitter_treatment_id": "TREATMENT_NULL_02",
            "immunotherapy_type": "Other immunomodulatory substances",
            "submitter_donor_id": "DONOR_NULL",
            "program_id": "SYNTHETIC-2"
        },
        {
            "submitter_treatment_id": "TREATMENT_NULL_02",
            "drug_name": "Nivolumab",
            "drug_reference_identifier": "987654",
            "drug_reference_database": "PubChem",
            "submitter_donor_id": "DONOR_NULL",
            "program_id": "SYNTHETIC-2"
        },
        {
            "submitter_treatment_id": "TREATMENT_NULL_01",
            "immunotherapy_drug_dose_units": "mg/kg",
            "submitter_donor_id": "DONOR_NULL",
            "program_id": "SYNTHETIC-2"
        },
        {   # all fields with valid values
            "submitter_treatment_id": "TREATMENT_ALL_01",
            "program_id": "SYNTHETIC-2",
            "submitter_donor_id": "DONOR_ALL_01",
            "immunotherapy_type": "Other immunomodulatory substances",
            "drug_name": "Braftovi",
            "drug_reference_identifier": "2049112",
            "drug_reference_database": "RxNorm",
            "immunotherapy_drug_dose_units": "ug/m2",
            "prescribed_cumulative_drug_dose": 133,
            "actual_cumulative_drug_dose": 100
        },
        {  # all fields with valid values
            "submitter_treatment_id": "TREATMENT_ALL_02",
            "program_id": "SYNTHETIC-2",
            "submitter_donor_id": "DONOR_ALL_02",
            "immunotherapy_type": "Other immunomodulatory substances",
            "drug_name": "Braftovi",
            "drug_reference_identifier": "2049112",
            "drug_reference_database": "RxNorm",
            "immunotherapy_drug_dose_units": "ug/m2",
            "prescribed_cumulative_drug_dose": 133,
            "actual_cumulative_drug_dose": 100
        }
    ]
    return immunotherapies


def add_radiations():
    radiations = [
        {
            "submitter_treatment_id": "TREATMENT_0026",
            "submitter_primary_diagnosis_id": "PRIMARY_DIAGNOSIS_ALL_01",
            "program_id": "SYNTHETIC-2",
            "submitter_donor_id": "DONOR_ALL_01",
            "radiation_therapy_modality": "Megavoltage radiation therapy using photons (procedure)",
            "radiation_therapy_type": "Internal",
            "radiation_therapy_fractions": "35",
            "radiation_therapy_dosage": "66",
            "anatomical_site_irradiated": "Upper Body",
            "radiation_boost": "No"
        },
        {
            "submitter_treatment_id": "TREATMENT_ALL_02",
            "submitter_primary_diagnosis_id": "PRIMARY_DIAGNOSIS_ALL_02",
            "program_id": "SYNTHETIC-2",
            "submitter_donor_id": "DONOR_ALL_02",
            "radiation_therapy_modality": "Megavoltage radiation therapy using photons (procedure)",
            "radiation_therapy_type": "Internal",
            "radiation_therapy_fractions": "35",
            "radiation_therapy_dosage": "66",
            "anatomical_site_irradiated": "Upper Body",
            "radiation_boost": "No"
        },
        {
            "submitter_treatment_id": "TREATMENT_ALL_01",
            "program_id": "SYNTHETIC-2",
            "submitter_donor_id": "DONOR_ALL_01",
            "radiation_therapy_modality": "Megavoltage radiation therapy using photons (procedure)",
            "radiation_therapy_type": "Internal",
            "radiation_therapy_fractions": "35",
            "radiation_therapy_dosage": "66",
            "anatomical_site_irradiated": "Boost - Area Previously Treated",
            "radiation_boost": "Yes",
            "reference_radiation_treatment_id": "TREATMENT_0026"

        },
        {
            "submitter_treatment_id": "TREATMENT_NULL_02",
            "radiation_therapy_type": "Internal",
            "submitter_donor_id": "DONOR_NULL",
            "program_id": "SYNTHETIC-2"
        },
        {
            "submitter_treatment_id": "TREATMENT_NULL_02",
            "radiation_therapy_modality": "Teleradiotherapy neutrons (procedure)",
            "submitter_donor_id": "DONOR_NULL",
            "program_id": "SYNTHETIC-2"
        },
        {
            "submitter_treatment_id": "TREATMENT_NULL_01",
            "anatomical_site_irradiated": "Right Maxilla",
            "submitter_donor_id": "DONOR_NULL",
            "program_id": "SYNTHETIC-2"
        }
    ]
    return radiations


def add_surgeries():
    surgeries = [
        {
            "submitter_treatment_id": "TREATMENT_ALL_01",
            "program_id": "SYNTHETIC-2",
            "submitter_donor_id": "DONOR_ALL_01",
            "margin_types_involved": ["Proximal margin", "Distal margin"],
            "margin_types_not_involved": ["Common bile duct margin", "Circumferential resection margin"],
            "margin_types_not_assessed": ["Unknown", "Not applicable"],
            "submitter_specimen_id": "SPECIMEN_ALL_01",
            "surgery_type": "Wide Local Excision",
            "surgery_site": "C11",
            "surgery_location": "Metastatic",
            "tumour_length": "5",
            "tumour_width": "7",
            "greatest_dimension_tumour": "10",
            "tumour_focality": "Multifocal",
            "residual_tumour_classification": "R0",
            "lymphovascular_invasion": "Both lymphatic and small vessel and venous (large vessel) invasion",
            "perineural_invasion": "Present"
        },
        {
            "submitter_treatment_id": "TREATMENT_ALL_02",
            "program_id": "SYNTHETIC-2",
            "submitter_donor_id": "DONOR_ALL_02",
            "margin_types_involved": ["Proximal margin", "Distal margin"],
            "margin_types_not_involved": ["Common bile duct margin", "Circumferential resection margin"],
            "margin_types_not_assessed": ["Unknown", "Not applicable"],
            "submitter_specimen_id": "SPECIMEN_ALL_02",
            "surgery_type": "Wide Local Excision",
            "surgery_site": "C11",
            "surgery_location": "Metastatic",
            "tumour_length": "5",
            "tumour_width": "7",
            "greatest_dimension_tumour": "10",
            "tumour_focality": "Multifocal",
            "residual_tumour_classification": "R0",
            "lymphovascular_invasion": "Both lymphatic and small vessel and venous (large vessel) invasion",
            "perineural_invasion": "Present"
        },
        {
            "submitter_treatment_id": "TREATMENT_NULL_02",
            "submitter_specimen_id": "SPECIMEN_NULL_01",
            "surgery_type": "Wide Local Excision",
            "submitter_donor_id": "DONOR_NULL",
            "program_id": "SYNTHETIC-2"
        },
        {
            "submitter_treatment_id": "TREATMENT_NULL_02",
            "submitter_specimen_id": "SPECIMEN_NULL_01",
            "surgery_site": "C11",
            "submitter_donor_id": "DONOR_NULL",
            "program_id": "SYNTHETIC-2"
        },
        {
            "submitter_treatment_id": "TREATMENT_NULL_01",
            "submitter_specimen_id": "SPECIMEN_NULL_01",
            "surgery_location": "Metastatic",
            "submitter_donor_id": "DONOR_NULL",
            "program_id": "SYNTHETIC-2"
        }
    ]
    return surgeries


def add_objects(filename):
    match filename:
        case "Donor.json":
            return add_donors()
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
