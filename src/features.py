"""
Feature Engineering for Funda Price Prediction

Adds geospatial and external features to the dataset
"""

import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from datetime import datetime
import time


class FeatureEngineer:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="funda_price_predictor")
        
        # Major city centers in NL (lat, lon)
        self.city_centers = {
            'amsterdam': (52.3676, 4.9041),
            'rotterdam': (51.9244, 4.4777),
            'utrecht': (52.0907, 5.1214),
            'den haag': (52.0705, 4.3007),
            'eindhoven': (51.4416, 5.4697)
        }
        
        # Major NS stations
        self.major_stations = {
            'amsterdam_centraal': (52.3791, 4.9003),
            'utrecht_centraal': (52.0889, 5.1103),
            'rotterdam_centraal': (51.9249, 4.4690),
            'den_haag_centraal': (52.0806, 4.3250),
            'schiphol': (52.3105, 4.7683)
        }
    
    def add_basic_features(self, df):
        """Add basic derived features"""
        df = df.copy()
        
        # Age of the house
        current_year = datetime.now().year
        if 'build_year' in df.columns:
            df['house_age'] = current_year - df['build_year']
            df['house_age'] = df['house_age'].clip(lower=0)  # No negative ages
        
        # Price per m²
        if 'price' in df.columns and 'living_area_m2' in df.columns:
            df['price_per_m2'] = df['price'] / df['living_area_m2']
        
        # Has garden (if plot area > living area)
        if 'plot_area_m2' in df.columns and 'living_area_m2' in df.columns:
            df['has_garden'] = (df['plot_area_m2'] > df['living_area_m2']).astype(int)
        
        # Energy label encoded
        energy_mapping = {
            'A+++++': 7, 'A++++': 6, 'A+++': 5, 'A++': 4, 'A+': 3, 'A': 2,
            'B': 1, 'C': 0, 'D': -1, 'E': -2, 'F': -3, 'G': -4
        }
        if 'energy_label' in df.columns:
            df['energy_score'] = df['energy_label'].map(energy_mapping)
        
        return df
    
    def get_coordinates(self, postcode, city):
        """Get lat/lon from postcode"""
        try:
            location = self.geolocator.geocode(f"{postcode}, {city}, Netherlands")
            if location:
                return location.latitude, location.longitude
        except Exception as e:
            print(f"Geocoding error for {postcode}: {e}")
        return None, None
    
    def add_geospatial_features(self, df, sample_size=None):
        """
        Add distance-based features
        
        Args:
            df: Input DataFrame
            sample_size: If set, only geocode first N rows (for testing)
        """
        df = df.copy()
        
        print("Adding geospatial features...")
        
        # Initialize columns
        df['latitude'] = None
        df['longitude'] = None
        df['distance_to_center'] = None
        df['distance_to_station'] = None
        
        # Limit sample if specified
        if sample_size:
            df_sample = df.head(sample_size)
            indices = df_sample.index
        else:
            df_sample = df
            indices = df.index
        
        for idx in indices:
            postcode = df.loc[idx, 'postcode']
            location_text = df.loc[idx, 'location'] if 'location' in df.columns else 'amsterdam'
            
            if pd.isna(postcode):
                continue
            
            # Get coordinates
            city = self._extract_city(location_text)
            lat, lon = self.get_coordinates(postcode, city)
            
            if lat and lon:
                df.loc[idx, 'latitude'] = lat
                df.loc[idx, 'longitude'] = lon
                
                # Distance to nearest city center
                min_dist_center = self._min_distance((lat, lon), self.city_centers)
                df.loc[idx, 'distance_to_center'] = min_dist_center
                
                # Distance to nearest major station
                min_dist_station = self._min_distance((lat, lon), self.major_stations)
                df.loc[idx, 'distance_to_station'] = min_dist_station
            
            time.sleep(1)  # Respect Nominatim rate limit (1 req/sec)
        
        return df
    
    def _extract_city(self, location_text):
        """Extract city name from location string"""
        # Simple heuristic - take last part after comma
        if isinstance(location_text, str):
            parts = location_text.split(',')
            if len(parts) > 0:
                city = parts[-1].strip().lower()
                return city
        return 'amsterdam'  # default
    
    def _min_distance(self, point, locations_dict):
        """Calculate minimum distance to a set of locations"""
        if not point or None in point:
            return None
        
        distances = []
        for loc_coords in locations_dict.values():
            dist = geodesic(point, loc_coords).kilometers
            distances.append(dist)
        
        return min(distances) if distances else None
    
    def add_categorical_encoding(self, df):
        """One-hot encode categorical variables"""
        df = df.copy()
        
        # Columns to encode
        categorical_cols = ['house_type', 'construction_type']
        
        for col in categorical_cols:
            if col in df.columns:
                # Get top N categories, rest as 'other'
                top_categories = df[col].value_counts().head(5).index
                df[col] = df[col].apply(lambda x: x if x in top_categories else 'other')
                
                # One-hot encode
                dummies = pd.get_dummies(df[col], prefix=col, drop_first=True)
                df = pd.concat([df, dummies], axis=1)
        
        return df
    
    def process_full_pipeline(self, input_file, output_file=None, sample_size=None):
        """
        Run complete feature engineering pipeline
        
        Args:
            input_file: Path to raw CSV
            output_file: Path to save processed CSV
            sample_size: If set, only process first N rows (for testing)
        """
        print(f"Loading data from {input_file}")
        df = pd.read_csv(input_file)
        
        print(f"Initial shape: {df.shape}")
        
        # Step 1: Basic features
        print("\n[1/3] Adding basic features...")
        df = self.add_basic_features(df)
        
        # Step 2: Geospatial features (slow - optional)
        print("\n[2/3] Adding geospatial features...")
        # df = self.add_geospatial_features(df, sample_size=sample_size)
        print("⚠️  Skipping geospatial features (slow). Enable manually if needed.")
        
        # Step 3: Categorical encoding
        print("\n[3/3] Encoding categorical variables...")
        df = self.add_categorical_encoding(df)
        
        print(f"\nFinal shape: {df.shape}")
        print(f"New columns: {list(df.columns)}")
        
        if output_file:
            df.to_csv(output_file, index=False)
            print(f"\n✅ Processed data saved to {output_file}")
        
        return df


def main():
    """Example usage"""
    engineer = FeatureEngineer()
    
    # Process the data
    df = engineer.process_full_pipeline(
        input_file='data/raw/funda_amsterdam_latest.csv',
        output_file='data/processed/funda_processed.csv',
        sample_size=10  # Test with 10 rows first
    )
    
    print("\nSample of processed data:")
    print(df.head())


if __name__ == "__main__":
    main()
