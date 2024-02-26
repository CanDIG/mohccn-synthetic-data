# Marathon of Hope(MoH) Test Synthetic Datasets
This repository includes three datasets (large, medium, small) in `.csv` format with different numbers of donors. Additionally, it contains `genomic.json` files that link samples from the datasets to genomic data in `.bam`, `.cram`, and `.vcf` formats, `manifest.yml` and `moh.csv` configured to run through `clinical_ETL_code` repository, `raw_data_indexed.json` and `raw_data_map.json` which are outputs from `clinical_ETL_code`.

### Files:

- **Datasets:**
  - `large_dataset_csv`
  - `medium_dataset_csv`
  - `small_dataset_csv`

- **Scripts:**
  - `CSVConvert.py`: Used to convert the original synthetic data in Katsu to CSV files.
  - `validation_change.py`: Scripts for converting the synthetic data to a format compatible with the `clinical_ETL_code` repository.