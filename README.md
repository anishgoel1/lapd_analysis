# LA Crime Analysis

This project analyzes and visualizes Los Angeles crime data from 2020 to 2023.

## Data Source

The data is sourced from the Los Angeles Open Data portal:
[Crime Data from 2020 to Present](https://data.lacity.org/Public-Safety/Crime-Data-from-2020-to-Present/2nrs-mtv8/about_data)

## Setup

### Installation

1. Clone the repository:
```bash
git clone https://github.com/anishgoel1/lapd_analysis.git
cd lapd_analysis
```

2. Create and activate the conda environment:
```bash
# Create environment from yml file
conda env create -f environment.yml

# Activate the environment
conda activate crime_analysis

# Download required spaCy model
python -m spacy download en_core_web_md
```

## Usage

1. First, clean and prepare the data:
```bash
python data_cleaner.py
```

2. Then generate the crime heatmap:
```bash
python main.py
```