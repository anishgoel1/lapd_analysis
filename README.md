# LA Crime Analysis

This project analyzes and visualizes Los Angeles crime data from 2020 to present, creating interactive heatmaps and static visualizations with severity scoring based on NLP analysis.

## Data Source

The crime data is sourced from the Los Angeles Open Data portal:
[Crime Data from 2020 to Present](https://data.lacity.org/Public-Safety/Crime-Data-from-2020-to-Present/2nrs-mtv8/about_data)

## Setup

### Prerequisites
- Anaconda or Miniconda installed on your system
- Git (for cloning the repository)

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

This will:
1. Process the raw crime data into `cleaned_crime_data.pkl`
2. Calculate severity scores using NLP analysis
3. Generate an interactive heatmap (`la_crime_progression_2020_2024.html`)

## Features

- NLP-based severity scoring for crime types (1-5 scale)
- Interactive heatmap visualization
- Year-by-year crime progression (2020-2024)
- Severity-weighted crime density visualization
- Data preprocessing and cleaning

## Project Structure
```
.
├── environment.yml          # Conda environment configuration
├── data_cleaner.py         # Script for data preprocessing
├── main.py                 # Main script for generating heatmaps
├── cleaned_crime_data.pkl  # Processed crime data
└── README.md              # Project documentation
```

## Dependencies

All dependencies are managed through the conda environment:
- Python 3.11
- NumPy 1.24.3
- Pandas
- Folium
- spaCy
- scikit-learn
