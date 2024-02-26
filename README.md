# Marathon of Hope(MoH) Test Synthetic Datasets
This repository includes three datasets (large, medium, small) in `.csv` format with different numbers of donors. Additionally, it contains `genomic.json` files that link samples from the datasets to genomic data in `.bam`, `.cram`, and `.vcf` formats.

### Files:

- **Datasets:**
  - `large_dataset.csv`
  - `medium_dataset.csv`
  - `small_dataset.csv`
  - `genomic.json` inside each `_dataset.csv` folder

- **Scripts:**
  - `CSVConvert.py`: Used to convert the original synthetic data in Katsu to CSV files.
  - `validation_change.py`: Scripts for converting the synthetic data to a format compatible with the `clinical_ETL_code` repository.