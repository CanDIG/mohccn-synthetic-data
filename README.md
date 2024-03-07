# Marathon of Hope(MoH) Test Synthetic Datasets
This repository includes three datasets (large, medium, small) in `.csv` format with different numbers of donors. Additionally, it contains `genomic.json` files that link samples from the datasets to genomic data in `.bam`, `.cram`, and `.vcf` formats, `manifest.yml` and `moh.csv` configured to run through `clinical_ETL_code` repository, `raw_data_indexed.json` and `raw_data_map.json` which are outputs from `clinical_ETL_code`.

### Files:

- **Datasets:**
  - `large_dataset_csv`
  - `medium_dataset_csv`
  - `small_dataset_csv`

- **Scripts:**
  - `json_to_csv.py`: Used to convert the original synthetic data in Katsu to CSV files.
  - `csv_to_ingest.py`: Script for running clinical_etl on a particular dataset to convert into ingestable jsons

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

If you haven't done so already, setup a python virtual environment and run:

```commandline
pip install -r requirements.txt
```

Run the `csv_to_ingest.py` script to convert a particular sized dataset to an ingestable json file

```commandline
python src/csv_to_ingest.py --size m
```

Script uses the config files in the given folder to run `CSVConvert` from `clinical_ETL_code` and will output `raw_data_map.json` to the `medium_dataset_csv` folder. This file can be used for clinical data ingest.

## How to generate genomic json files

TBA
