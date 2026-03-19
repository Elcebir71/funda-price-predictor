"""
Machine Learning Models for House Price Prediction
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import xgboost as xgb
import joblib
import matplotlib.pyplot as plt
import seaborn as sns


class HousePriceModels:
    def __init__(self):
        self.models = {}
        self.scaler = StandardScaler()
        self.feature_names = None
        self.results = {}
    
    def prepare_data(self, df, target_col='price'):
        """
        Prepare data for modeling
        
        Args:
            df: Input DataFrame
            target_col: Target variable column name
            
        Returns:
            X, y, feature_names
        """
        # Drop non-numeric and non-feature columns
        cols_to_drop = [
            'url', 'scraped_at', 'address', 'location', 'postcode',
            'description', 'house_type', 'construction_type', 'energy_label',
            target_col
        ]
        
        # Keep only columns that exist
        cols_to_drop = [col for col in cols_to_drop if col in df.columns]
        
        # Features
        X = df.drop(columns=cols_to_drop, errors='ignore')
        
        # Target
        y = df[target_col]
        
        # Remove rows with missing target
        mask = ~y.isna()
        X = X[mask]
        y = y[mask]
        
        # Fill missing features with median
        X = X.fillna(X.median())
        
        self.feature_names = X.columns.tolist()
        
        print(f"Features: {len(self.feature_names)}")
        print(f"Samples: {len(X)}")
        print(f"Target range: {y.min():.0f} - {y.max():.0f}")
        
        return X, y
    
    def train_test_split_data(self, X, y, test_size=0.2, random_state=42):
        """Split data into train and test sets"""
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        return X_train_scaled, X_test_scaled, y_train, y_test
    
    def train_linear_models(self, X_train, y_train):
        """Train linear regression models"""
        print("\n[1/4] Training Linear Models...")
        
        # Linear Regression
        lr = LinearRegression()
        lr.fit(X_train, y_train)
        self.models['linear_regression'] = lr
        
        # Ridge
        ridge = Ridge(alpha=1.0)
        ridge.fit(X_train, y_train)
        self.models['ridge'] = ridge
        
        # Lasso
        lasso = Lasso(alpha=1000)
        lasso.fit(X_train, y_train)
        self.models['lasso'] = lasso
        
        print("✅ Linear models trained")
    
    def train_random_forest(self, X_train, y_train):
        """Train Random Forest"""
        print("\n[2/4] Training Random Forest...")
        
        rf = RandomForestRegressor(
            n_estimators=100,
            max_depth=15,
            min_samples_split=5,
            random_state=42,
            n_jobs=-1
        )
        rf.fit(X_train, y_train)
        self.models['random_forest'] = rf
        
        print("✅ Random Forest trained")
    
    def train_gradient_boosting(self, X_train, y_train):
        """Train Gradient Boosting"""
        print("\n[3/4] Training Gradient Boosting...")
        
        gb = GradientBoostingRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        )
        gb.fit(X_train, y_train)
        self.models['gradient_boosting'] = gb
        
        print("✅ Gradient Boosting trained")
    
    def train_xgboost(self, X_train, y_train):
        """Train XGBoost"""
        print("\n[4/4] Training XGBoost...")
        
        xgb_model = xgb.XGBRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42,
            n_jobs=-1
        )
        xgb_model.fit(X_train, y_train)
        self.models['xgboost'] = xgb_model
        
        print("✅ XGBoost trained")
    
    def evaluate_models(self, X_test, y_test):
        """Evaluate all trained models"""
        print("\n" + "="*60)
        print("MODEL EVALUATION")
        print("="*60)
        
        results = []
        
        for name, model in self.models.items():
            y_pred = model.predict(X_test)
            
            mae = mean_absolute_error(y_test, y_pred)
            rmse = np.sqrt(mean_squared_error(y_test, y_pred))
            r2 = r2_score(y_test, y_pred)
            
            results.append({
                'Model': name,
                'MAE': mae,
                'RMSE': rmse,
                'R²': r2
            })
            
            print(f"\n{name.upper()}")
            print(f"  MAE:  €{mae:,.0f}")
            print(f"  RMSE: €{rmse:,.0f}")
            print(f"  R²:   {r2:.4f}")
        
        self.results = pd.DataFrame(results)
        return self.results
    
    def plot_results(self):
        """Plot model comparison"""
        if self.results.empty:
            print("No results to plot. Run evaluate_models first.")
            return
        
        fig, axes = plt.subplots(1, 3, figsize=(15, 4))
        
        # MAE
        axes[0].barh(self.results['Model'], self.results['MAE'])
        axes[0].set_xlabel('MAE (€)')
        axes[0].set_title('Mean Absolute Error')
        
        # RMSE
        axes[1].barh(self.results['Model'], self.results['RMSE'])
        axes[1].set_xlabel('RMSE (€)')
        axes[1].set_title('Root Mean Squared Error')
        
        # R²
        axes[2].barh(self.results['Model'], self.results['R²'])
        axes[2].set_xlabel('R² Score')
        axes[2].set_title('R² Score')
        axes[2].set_xlim([0, 1])
        
        plt.tight_layout()
        plt.savefig('data/processed/model_comparison.png', dpi=300, bbox_inches='tight')
        print("\n✅ Plot saved to data/processed/model_comparison.png")
        plt.show()
    
    def feature_importance(self, model_name='random_forest', top_n=15):
        """Plot feature importance for tree-based models"""
        if model_name not in self.models:
            print(f"Model {model_name} not found.")
            return
        
        model = self.models[model_name]
        
        if not hasattr(model, 'feature_importances_'):
            print(f"Model {model_name} does not have feature_importances_")
            return
        
        importances = model.feature_importances_
        indices = np.argsort(importances)[::-1][:top_n]
        
        plt.figure(figsize=(10, 6))
        plt.barh(range(top_n), importances[indices])
        plt.yticks(range(top_n), [self.feature_names[i] for i in indices])
        plt.xlabel('Importance')
        plt.title(f'Top {top_n} Features - {model_name}')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.savefig(f'data/processed/feature_importance_{model_name}.png', dpi=300)
        print(f"\n✅ Feature importance saved")
        plt.show()
    
    def save_best_model(self, model_name, filepath='models/best_model.pkl'):
        """Save trained model to disk"""
        if model_name not in self.models:
            print(f"Model {model_name} not found.")
            return
        
        import os
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Save model and scaler
        joblib.dump({
            'model': self.models[model_name],
            'scaler': self.scaler,
            'feature_names': self.feature_names
        }, filepath)
        
        print(f"✅ Model saved to {filepath}")
    
    def predict(self, X_new, model_name='xgboost'):
        """Make predictions on new data"""
        if model_name not in self.models:
            print(f"Model {model_name} not found.")
            return None
        
        X_scaled = self.scaler.transform(X_new)
        predictions = self.models[model_name].predict(X_scaled)
        
        return predictions


def main():
    """Example usage"""
    # Load processed data
    df = pd.read_csv('data/processed/funda_processed.csv')
    
    # Initialize model trainer
    trainer = HousePriceModels()
    
    # Prepare data
    X, y = trainer.prepare_data(df)
    X_train, X_test, y_train, y_test = trainer.train_test_split_data(X, y)
    
    # Train all models
    trainer.train_linear_models(X_train, y_train)
    trainer.train_random_forest(X_train, y_train)
    trainer.train_gradient_boosting(X_train, y_train)
    trainer.train_xgboost(X_train, y_train)
    
    # Evaluate
    results = trainer.evaluate_models(X_test, y_test)
    print("\n" + "="*60)
    print(results.to_string(index=False))
    print("="*60)
    
    # Plot results
    trainer.plot_results()
    
    # Feature importance
    trainer.feature_importance('random_forest')
    
    # Save best model
    best_model = results.loc[results['R²'].idxmax(), 'Model']
    print(f"\n🏆 Best model: {best_model}")
    trainer.save_best_model(best_model)


if __name__ == "__main__":
    main()
