"""
Feature engineering for Funda house price prediction
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import re


def extract_city(address):
    """Extract city from address string"""
    cities = ['Amsterdam', 'Utrecht', 'Rotterdam', 'Eindhoven', 'Haag', 'Hague']
    
    for city in cities:
        if city.lower() in address.lower():
            if city in ['Haag', 'Hague']:
                return 'Den Haag'
            return city
    return 'Other'


def create_features(df):
    """
    Create engineered features
    
    Args:
        df: Raw dataframe
        
    Returns:
        df: Dataframe with new features
    """
    
    df = df.copy()
    
    # 1. Extract city from address
    df['city'] = df['address'].apply(extract_city)
    
    # 2. Price per m²
    df['price_per_m2'] = df['price'] / df['living_area_m2']
    
    # 3. House age (current year - build year)
    current_year = 2026
    df['house_age'] = current_year - df['build_year']
    
    # 4. Is new construction (< 5 years)
    df['is_new'] = (df['house_age'] < 5).astype(int)
    
    # 5. Has build year info
    df['has_build_year'] = df['build_year'].notna().astype(int)
    
    # 6. Fill missing build_year with median
    df['build_year_filled'] = df['build_year'].fillna(df['build_year'].median())
    df['house_age_filled'] = current_year - df['build_year_filled']
    
    # 7. Energy label to numeric score
    energy_mapping = {
        'A+++': 10, 'A++': 9, 'A+': 8, 'A': 7,
        'B': 6, 'C': 5, 'D': 4, 'E': 3, 'F': 2, 'G': 1
    }
    df['energy_score'] = df['energy_label'].map(energy_mapping)
    
    # 8. Has energy label info
    df['has_energy_label'] = df['energy_label'].notna().astype(int)
    
    # 9. Fill missing energy score with median
    df['energy_score_filled'] = df['energy_score'].fillna(df['energy_score'].median())
    
    # 10. Room to area ratio
    df['room_area_ratio'] = df['rooms'] / df['living_area_m2']
    
    # 11. Has bedrooms info
    df['has_bedrooms'] = df['bedrooms'].notna().astype(int)
    
    # 12. Fill missing bedrooms (assume rooms - 1)
    df['bedrooms_filled'] = df['bedrooms'].fillna(df['rooms'] - 1)
    
    # 13. Price category (for analysis)
    df['price_category'] = pd.cut(
        df['price'],
        bins=[0, 300000, 500000, 750000, 1000000, np.inf],
        labels=['Budget', 'Mid', 'Upper-Mid', 'Luxury', 'Premium']
    )
    
    # 14. Area category
    df['area_category'] = pd.cut(
        df['living_area_m2'],
        bins=[0, 60, 90, 120, 150, np.inf],
        labels=['Small', 'Medium', 'Large', 'Very Large', 'Mansion']
    )
    
    return df


def prepare_for_modeling(df):
    """
    Prepare features for ML modeling
    
    Args:
        df: Dataframe with engineered features
        
    Returns:
        X: Feature matrix
        y: Target variable
        feature_names: List of feature names
    """
    
    # Define features to use
    numeric_features = [
        'living_area_m2',
        'rooms',
        'bedrooms_filled',
        'house_age_filled',
        'energy_score_filled',
        'price_per_m2',
        'room_area_ratio',
        'has_build_year',
        'has_energy_label',
        'has_bedrooms',
        'is_new'
    ]
    
    categorical_features = ['city']
    
    # One-hot encode city
    df_encoded = pd.get_dummies(df, columns=['city'], drop_first=True)
    
    # Get all feature columns
    city_cols = [col for col in df_encoded.columns if col.startswith('city_')]
    all_features = numeric_features + city_cols
    
    X = df_encoded[all_features]
    y = df_encoded['price']
    
    return X, y, all_features


if __name__ == '__main__':
    # Load data
    df = pd.read_csv('data/raw/funda_cleaned.csv')
    print(f"Original data: {df.shape}")
    
    # Create features
    df_featured = create_features(df)
    print(f"After feature engineering: {df_featured.shape}")
    
    # Show new columns
    new_cols = [col for col in df_featured.columns if col not in df.columns]
    print(f"\nNew features created ({len(new_cols)}):")
    for col in new_cols:
        print(f"  - {col}")
    
    # Save
    df_featured.to_csv('data/processed/funda_featured.csv', index=False)
    print(f"\n✅ Saved to: data/processed/funda_featured.csv")
    
    # Prepare for modeling
    X, y, features = prepare_for_modeling(df_featured)
    print(f"\n📊 Model-ready data:")
    print(f"   X shape: {X.shape}")
    print(f"   y shape: {y.shape}")
    print(f"\n   Features ({len(features)}):")
    for f in features:
        print(f"     - {f}")
