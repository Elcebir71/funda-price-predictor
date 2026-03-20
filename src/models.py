"""
ML models for Funda house price prediction
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import warnings
warnings.filterwarnings('ignore')


def evaluate_model(y_true, y_pred, model_name):
    """Calculate evaluation metrics"""
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    
    return {
        'Model': model_name,
        'MAE': f'€{mae:,.0f}',
        'RMSE': f'€{rmse:,.0f}',
        'R²': f'{r2:.3f}',
        'MAPE': f'{mape:.2f}%'
    }


def train_models(X_train, X_test, y_train, y_test):
    """Train and evaluate multiple models"""
    
    models = {
        'Linear Regression': LinearRegression(),
        'Ridge': Ridge(alpha=10),
        'Random Forest': RandomForestRegressor(
            n_estimators=100,
            max_depth=15,
            min_samples_split=5,
            random_state=42,
            n_jobs=-1
        ),
        'XGBoost': XGBRegressor(
            n_estimators=100,
            max_depth=7,
            learning_rate=0.1,
            random_state=42,
            n_jobs=-1
        ),
        'LightGBM': LGBMRegressor(
            n_estimators=100,
            max_depth=7,
            learning_rate=0.1,
            random_state=42,
            n_jobs=-1,
            verbose=-1
        ),
        'Gradient Boosting': GradientBoostingRegressor(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            random_state=42
        )
    }
    
    results = []
    trained_models = {}
    
    print("🤖 Training models...\n")
    
    for name, model in models.items():
        print(f"Training {name}...")
        
        # Train
        model.fit(X_train, y_train)
        
        # Predict
        y_pred = model.predict(X_test)
        
        # Evaluate
        metrics = evaluate_model(y_test, y_pred, name)
        results.append(metrics)
        
        # Cross-validation
        cv_scores = cross_val_score(
            model, X_train, y_train,
            cv=5, scoring='r2', n_jobs=-1
        )
        
        print(f"  ✅ R²: {metrics['R²']} | MAE: {metrics['MAE']} | CV R²: {cv_scores.mean():.3f} (±{cv_scores.std():.3f})")
        
        # Save model
        trained_models[name] = model
    
    # Results dataframe
    results_df = pd.DataFrame(results)
    
    return results_df, trained_models


def get_feature_importance(model, feature_names, top_n=10):
    """Extract feature importance"""
    
    if hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
    elif hasattr(model, 'coef_'):
        importances = np.abs(model.coef_)
    else:
        return None
    
    importance_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': importances
    }).sort_values('Importance', ascending=False).head(top_n)
    
    return importance_df


if __name__ == '__main__':
    print("=" * 60)
    print("🏠 FUNDA HOUSE PRICE PREDICTION - MODEL TRAINING")
    print("=" * 60)
    
    # Load featured data
    print("\n📂 Loading data...")
    df = pd.read_csv('data/processed/funda_featured.csv')
    print(f"   Data shape: {df.shape}")
    
    # Prepare features
    from features import prepare_for_modeling
    X, y, feature_names = prepare_for_modeling(df)
    
    print(f"   Features: {X.shape[1]}")
    print(f"   Samples: {X.shape[0]}")
    
    # Train-test split
    print("\n✂️  Splitting data (80/20)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"   Train: {X_train.shape[0]} samples")
    print(f"   Test: {X_test.shape[0]} samples")
    
    # Train models
    print("\n" + "=" * 60)
    results_df, trained_models = train_models(X_train, X_test, y_train, y_test)
    
    # Display results
    print("\n" + "=" * 60)
    print("📊 MODEL COMPARISON")
    print("=" * 60)
    print(results_df.to_string(index=False))
    
    # Best model
    best_model_name = results_df.loc[results_df['R²'].str.replace('0.', '').astype(float).idxmax(), 'Model']
    best_model = trained_models[best_model_name]
    
    print(f"\n🏆 Best model: {best_model_name}")
    
    # Feature importance (best model)
    print(f"\n📈 Feature Importance ({best_model_name}):")
    importance = get_feature_importance(best_model, feature_names, top_n=10)
    if importance is not None:
        print(importance.to_string(index=False))
    
    # Save best model
    print(f"\n💾 Saving models...")
    joblib.dump(best_model, f'models/best_model_{best_model_name.replace(" ", "_").lower()}.pkl')
    
    # Save all models
    for name, model in trained_models.items():
        filename = f'models/{name.replace(" ", "_").lower()}.pkl'
        joblib.dump(model, filename)
    
    print(f"   ✅ Saved {len(trained_models)} models to models/")
    
    # Save results
    results_df.to_csv('models/model_comparison.csv', index=False)
    print(f"   ✅ Saved comparison to models/model_comparison.csv")
    
    print("\n" + "=" * 60)
    print("✅ MODEL TRAINING COMPLETE!")
    print("=" * 60)
