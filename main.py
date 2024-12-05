"""
LA Crime Analysis and Visualization
---------------------------------
This module processes LA crime data and generates visualizations showing
crime severity changes between 2020-2023.
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple
import matplotlib.pyplot as plt
import contextily as ctx
from matplotlib.patheffects import withStroke
import spacy
from pathlib import Path


def calculate_severity_scores(crime_descriptions: list[str]) -> Dict[str, int]:
    """
    Calculate severity scores for crime descriptions using NLP.
    
    Args:
        crime_descriptions: List of crime description strings
        
    Returns:
        Dictionary mapping crime descriptions to severity scores (1-5)
    """
    nlp = spacy.load("en_core_web_md")
    
    severity_keywords = {
        5: ["murder", "homicide", "rape", "sexual", "kidnap", "child abuse", "arson"],
        4: ["robbery", "weapon", "assault", "intimate partner", "battery", "shots fired"],
        3: ["burglary", "stolen", "theft", "break"],
        2: ["vandalism", "threat", "trespassing", "forge", "fraud", "shoplifting", "stalking"],
        1: ["disturb", "drunk", "minor", "petty"]
    }

    # Pre-process keywords with spaCy
    severity_vectors = {
        level: [nlp(keyword) for keyword in keywords]
        for level, keywords in severity_keywords.items()
    }

    scores = {}
    for desc in set(crime_descriptions):
        desc_vec = nlp(desc.lower())
        max_score = 1
        max_similarity = 0

        for level, keyword_vectors in severity_vectors.items():
            similarities = [desc_vec.similarity(kw_vec) for kw_vec in keyword_vectors]
            level_max_similarity = max(similarities) if similarities else 0

            if level_max_similarity > max_similarity:
                max_similarity = level_max_similarity
                max_score = level

        scores[desc.lower()] = max_score if max_similarity > 0.3 else 1

    return scores


def get_la_landmarks() -> Dict[str, Tuple[float, float]]:
    """
    Return dictionary of LA landmarks and their coordinates.
    
    Returns:
        Dictionary mapping landmark names to (longitude, latitude) tuples
    """
    return {
        'Venice': (-118.471, 34.002),
        'Beverly Hills': (-118.400, 34.073),
        'Bel Air': (-118.461, 34.082),
        'West Hollywood': (-118.363, 34.090),
        'Downtown': (-118.243, 34.040),
        'Koreatown': (-118.300, 34.062),
        'Echo Park': (-118.260, 34.078),
        'Los Feliz': (-118.292, 34.105),
        'Culver City': (-118.396, 34.021),
        'Century City': (-118.417, 34.053),
        'Brentwood': (-118.476, 34.054),
        'Pacific Palisades': (-118.535, 34.045),
        'Sherman Oaks': (-118.451, 34.149),
        'Studio City': (-118.387, 34.139),
        'North Hollywood': (-118.376, 34.172),
        'Van Nuys': (-118.449, 34.186),
        'Encino': (-118.521, 34.151),
        'Tarzana': (-118.550, 34.168),
        'Woodland Hills': (-118.610, 34.165),
        'Burbank': (-118.309, 34.181),
        'Glendale': (-118.255, 34.142),
        'Marina Del Rey': (-118.451, 33.980),
        'Playa Del Rey': (-118.448, 33.945),
        'El Segundo': (-118.416, 33.919),
        'Pacoima': (-118.410, 34.275),
        'Sunland': (-118.302, 34.257),
        'Sun Valley': (-118.381, 34.217),
        'Granada Hills': (-118.530, 34.293),
        'Chatsworth': (-118.604, 34.257)
    }


def process_crime_data(df: pd.DataFrame, severity_scores: Dict[str, int]) -> pd.DataFrame:
    """
    Process crime data by adding severity scores and calculating grid positions.
    
    Args:
        df: Input DataFrame with crime data
        severity_scores: Dictionary of severity scores for crime descriptions
        
    Returns:
        Processed DataFrame with added columns
    """
    df = df.copy()
    df["severity"] = df["Crm Cd Desc"].str.lower().map(severity_scores)
    df["YEAR"] = pd.to_datetime(df["DATE OCC"]).dt.year
    df = df[df["YEAR"].between(2020, 2023)]

    # Create grid cells for aggregation (approximately 500m grid cells)
    grid_size = 0.005
    df['lat_grid'] = (df['LAT'] / grid_size).round() * grid_size
    df['lon_grid'] = (df['LON'] / grid_size).round() * grid_size
    
    return df


def generate_crime_change_map(data_path: str | Path, output_path: str | Path) -> None:
    """
    Generate and save a map visualization showing crime changes between 2020-2023.
    
    Args:
        data_path: Path to the input pickle file containing crime data
        output_path: Path where the output map image will be saved
    """
    df = pd.read_pickle(data_path)
    
    # Calculate severity scores
    unique_crimes = df["Crm Cd Desc"].unique()
    severity_scores = calculate_severity_scores(unique_crimes)
    
    # Process data
    df = process_crime_data(df, severity_scores)
    
    # Calculate statistics for both years
    df_2020 = df[df["YEAR"] == 2020].groupby(['lat_grid', 'lon_grid'])['severity'].agg(['mean', 'count']).reset_index()
    df_2023 = df[df["YEAR"] == 2023].groupby(['lat_grid', 'lon_grid'])['severity'].agg(['mean', 'count']).reset_index()
    
    # Merge and calculate changes
    df_merged = pd.merge(df_2020, df_2023, on=['lat_grid', 'lon_grid'], suffixes=('_2020', '_2023'), how='outer')
    df_merged = df_merged.fillna(0)
    
    # Calculate percent changes
    df_merged['severity_change'] = ((df_merged['mean_2023'] - df_merged['mean_2020']) / df_merged['mean_2020']) * 100
    df_merged['severity_change'] = df_merged['severity_change'].clip(-100, 100)
    
    df_merged['incident_change'] = ((df_merged['count_2023'] - df_merged['count_2020']) / df_merged['count_2020']) * 100
    df_merged['incident_change'] = df_merged['incident_change'].clip(-100, 100)
    
    # Create visualization
    create_map_visualization(df_merged, output_path)


def create_map_visualization(df_merged: pd.DataFrame, output_path: str | Path) -> None:
    """
    Create and save the map visualization.
    
    Args:
        df_merged: Processed DataFrame with crime change data
        output_path: Path where the output map image will be saved
    """
    base_size = 50
    sizes = base_size * (1 + df_merged['incident_change']/100)
    sizes = sizes.clip(base_size/2, base_size*2)

    plt.figure(figsize=(24, 18))
    ax = plt.gca()
    
    # Create scatter plot
    scatter = ax.scatter(df_merged['lon_grid'], 
                        df_merged['lat_grid'],
                        c=df_merged['severity_change'],
                        s=sizes,
                        cmap='RdYlGn_r',
                        alpha=0.6)
    
    # Add map and landmarks
    ctx.add_basemap(ax, crs='EPSG:4326', source=ctx.providers.OpenStreetMap.Mapnik)
    add_landmarks(ax)
    
    # Configure map properties
    configure_map_properties(ax)
    
    # Add colorbar and legend
    add_colorbar_and_legend(ax, scatter, base_size)
    
    # Save the figure
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()


def add_landmarks(ax: plt.Axes) -> None:
    """Add landmark labels to the map."""
    text_props = {
        'fontsize': 14,
        'fontweight': 'bold',
        'color': 'black',
        'bbox': dict(
            facecolor='white',
            alpha=0.7,
            edgecolor='none',
            pad=0.5,
            boxstyle='round,pad=0.5'
        ),
        'path_effects': [withStroke(linewidth=2, foreground='white')],
        'zorder': 5,
        'ha': 'center',
        'va': 'center'
    }
    
    for name, (lon, lat) in get_la_landmarks().items():
        if plt.xlim()[0] <= lon <= plt.xlim()[1] and plt.ylim()[0] <= lat <= plt.ylim()[1]:
            ax.text(lon, lat, name, **text_props)


def configure_map_properties(ax: plt.Axes) -> None:
    """Configure map axes properties."""
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.set_xticks([])
    ax.set_yticks([])
    plt.xlim(-118.75, -118.15)
    plt.ylim(33.90, 34.35)
    ax.grid(False)


def add_colorbar_and_legend(ax: plt.Axes, scatter: plt.scatter, base_size: int) -> None:
    """Add colorbar and legend to the map."""
    cbar = plt.colorbar(scatter, location='right', pad=0.02)
    cbar.set_label('% Change in Crime Severity', fontsize=18)
    cbar.ax.tick_params(labelsize=16)
    
    legend_elements = [
        plt.scatter([], [], c='gray', alpha=0.6, s=base_size*2, label='-50% or more'),
        plt.scatter([], [], c='gray', alpha=0.6, s=base_size*4, label='No change'),
        plt.scatter([], [], c='gray', alpha=0.6, s=base_size*8, label='+50% or more')
    ]
    
    ax.legend(handles=legend_elements, 
             title='Incident Count Change',
             loc='upper right',
             bbox_to_anchor=(0.98, 0.98),
             title_fontsize=20,
             fontsize=18,
             framealpha=0.8,
             markerscale=1.0)


if __name__ == "__main__":
    generate_crime_change_map("cleaned_crime_data.pkl", "la_crime_change_2020_2023.png")
