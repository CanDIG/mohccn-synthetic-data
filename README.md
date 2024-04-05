# Marathon of Hope(MoH) Test Synthetic Datasets
This repository includes three datasets (large, medium, small) in `.csv` format with different numbers of donors. Additionally, it contains `genomic.json` files that link samples from the datasets to genomic data in `.bam`, `.cram`, and `.vcf` formats, `manifest.yml` and `moh.csv` configured to run through `clinical_ETL_code` repository, `raw_data_indexed.json` and `raw_data_map.json` which are outputs from `clinical_ETL_code`.

### Files:

- **Datasets:**
  - [`large_dataset_csv`](large_dataset_csv)
  - [`medium_dataset_csv`](medium_dataset_csv)
  - [`small_dataset_csv`](small_dataset_csv)

- **Scripts:**
[/src](/src)
  - `json_to_csv.py`: Used to convert the original synthetic data in Katsu to CSV files.
    - `extra_donors.py`: Adds extra donors to all datasets to test specific scenarios. Imported by `json_to_csv.py`.
    - `post_processing.py`: Edits data to ensure it meets conditional requirements of the model. Imported by `json_to_csv.py`.
  - `csv_to_ingest.py`: Script for running clinical_etl on a particular dataset to convert into ingestable jsons.

## How to generate synthetic data using Mockaroo

See synthetic data folder in katsu: [katsu/chord_metadata_service/mohpackets/data](https://github.com/CanDIG/katsu/tree/develop/chord_metadata_service/mohpackets/data)

## How to convert mockaroo jsons to csv files

Setup a python virtual environment and run:

```commandline
pip install -r requirements.txt
```

Clone the katsu repo and note the path it is cloned to

Run the `json_to_csv.py` script. Can be run with s, m or l specified for small, medium or large dataset conversion. By default, uses the small dataset.

```commandline
python src/json_to_csv.py --size m --input /path/to/katsu/chord_metadata_service/mohpackets/data
```

The script takes the files in the given sized folder, in this case [`katsu/chord_metadata_service/mohpackets/data/medium_dataset/synthetic_data`](mockaroo_data/medium_dataset/synthetic_data) and converts the json files into csv files and stores them in [`medium_dataset_csv/raw_data`](medium_dataset_csv/raw_data). It converts and performs some minor value editing/replacement in order to ensure the data passes validation. 

This should not need to be done unless the mockaroo data is regenerated at some point, such as to change the shape of the data or to incorporate a new data model change.

## How to convert csv files to ingestable clinical json files

If you haven't done so already, set up a python virtual environment and run:

```commandline
pip install -r requirements.txt
```

Run the `csv_to_ingest.py` script to convert a particular sized dataset to an ingestable json file

```commandline
python src/csv_to_ingest.py --size m
```

Script uses the config files in the given folder to run `CSVConvert` from `clinical_ETL_code` and will output `raw_data_map.json` to the `medium_dataset_csv` folder. This file can be used for clinical data ingest.

### Creating a custom dataset

#### Specifying dataset size

##### `--sample`

Specifying the `--sample` argument will sample the specified number of donors, divided approximately equally amongst the 10 programs in the large_dataset. The maximum number for this argument is 4999, as there are 5000 total donors in this dataset.

Output csvs and from the clinical_etl tranformation will be saved in a folder named `custom_dataset_csv-{sample}`.

##### `--donor-number` and `--number-of-programs`

These two arguments must be specified together. `--donors-per-program` specifies the number of donors to choose per program, and `--number-of-programs` determines how many programs to sample from. So the total number of donors in the dataset will be `--donors-per-program` x `--number-of-programs`. The donors are sampled from the large dataset so the maximum for `--donors-per-program` is 500 and the maximum for `--number-of-programs` is 10.

All outputs are saved into a folder called: `custom_dataset_csv-{total_donors}`


#### Specifying a prefix with `--prefix`

The `--prefix` argument can be used to prepend the specified prefix to all csvs in the dataset. When this argument is used, a new folder is created `custom_dataset_csv-{prefix}`, the edited csvs are saved in this folder and the manifest from the source dataset is used for clinical_etl conversion. The outputs from clinical_etl are also saved in this folder.

## How to generate genomic json files

Genomic files were created manually. We may in the future come up with a way of auto-generating these. We are also still working on testing these for functionality.
