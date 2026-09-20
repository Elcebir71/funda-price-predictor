""""
Feature engineering for Funda house price prediction.
"""

import pandas as pd
import numpy as np


def extract_city(address):
    """Extract city from address string."""
    cities = ['Amsterdam', 'Utrecht', 'Rotterdam', 'Eindhoven', 'Haag', 'Hague']

    for city in cities:
        if city.lower() in str(address).lower():
            if city in ['Haag', 'Hague']:
                return 'Den Haag'
            return city
    return 'Other'


def create_features(df):
    """Create model features without using target-derived information."""
    df = df.copy()

    # 1. Extract city from address
    df['city'] = df['address'].apply(extract_city)

    # NOTE:
    # Do NOT create price_per_m2 here. It uses the target (price) and causes
    # target leakage when price is the prediction target.

    # 2. House age
    current_year = 2026
    df['house_age'] = current_year - df['build_year']

    # 3. Is new construction (< 5 years)
    df['is_new'] = (df['house_age'] < 5).astype(int)

    # 4. Has build year info
    df['has_build_year'] = df['build_year'].notna().astype(int)

    # 5. Fill missing build year with median
    df['build_year_filled'] = df['build_year'].fillna(df['build_year'].median())
    df['house_age_filled'] = current_year - df['build_year_filled']

    # 6. Energy label to numeric score
    energy_mapping = {
        'A+++': 10, 'A++': 9, 'A+': 8, 'A': 7,
        'B': 6, 'C': 5, 'D': 4, 'E': 3, 'F': 2, 'G': 1
    }
    df['energy_score'] = df['energy_label'].map(energy_mapping)

    # 7. Has energy label info
    df['has_energy_label'] = df['energy_label'].notna().astype(int)

    # 8. Fill missing energy score with median
    df['energy_score_filled'] = df['energy_score'].fillna(
        df['energy_score'].median()
    )

    # 9. Room to area ratio
    df['room_area_ratio'] = df['rooms'] / df['living_area_m2']

    # 10. Has bedrooms info
    df['has_bedrooms'] = df['bedrooms'].notna().astype(int)

    # 11. Fill missing bedrooms
    df['bedrooms_filled'] = df['bedrooms'].fillna(df['rooms'] - 1)

    # 12. Price category (analysis only; never used as a model feature)
    df['price_category'] = pd.cut(
        df['price'],
        bins=[0, 300000, 500000, 750000, 1000000, np.inf],
        labels=['Budget', 'Mid', 'Upper-Mid', 'Luxury', 'Premium']
    )

    # 13. Area category
    df['area_category'] = pd.cut(
        df['living_area_m2'],
        bins=[0, 60, 90, 120, 150, np.inf],
        labels=['Small', 'Medium', 'Large', 'Very Large', 'Mansion']
    )

    return df


def prepare_for_modeling(df):
    """Prepare features for ML modeling."""
    numeric_features = [
        'living_area_m2',
        'rooms',
        'bedrooms_filled',
        'house_age_filled',
        'energy_score_filled',
        'room_area_ratio',
        'has_build_year',
        'has_energy_label',
        'has_bedrooms',
        'is_new'
    ]

    # One-hot encode city
    df_encoded = pd.get_dummies(df, columns=['city'], drop_first=True)

    city_cols = [col for col in df_encoded.columns if col.startswith('city_')]
    all_features = numeric_features + city_cols

    X = df_encoded[all_features]
    y = df_encoded['price']

    return X, y, all_features


if __name__ == '__main__':
    df = pd.read_csv('data/raw/funda_cleaned.csv')
    print(f'Original data: {df.shape}')

    df_featured = create_features(df)
    print(f'After feature engineering: {df_featured.shape}')

    new_cols = [col for col in df_featured.columns if col not in df.columns]
    print(f'\nNew features created ({len(new_cols)}):')
    for col in new_cols:
        print(f'  - {col}')

    df_featured.to_csv('data/processed/funda_featured.csv', index=False)
    print('\nSaved to: data/processed/funda_featured.csv')

    X, y, features = prepare_for_modeling(df_featured)
    print('\nModel-ready data:')
    print(f'   X shape: {X.shape}')
    print(f'   y shape: {y.shape}')
    print(f'\nFeatures ({len(features)}):')
    for f in features:
        print(f'     - {f}')
