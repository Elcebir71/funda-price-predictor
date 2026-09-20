"""
ML models for Funda house price prediction.
"""

import warnings

import joblib
import numpy as np
import pandas as pd
from lightgbm import LGBMRegressor
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score, train_test_split
from xgboost import XGBRegressor

warnings.filterwarnings("ignore")


def evaluate_model(y_true, y_pred, model_name):
    """Calculate regression evaluation metrics."""
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100

    return {
        "Model": model_name,
        "MAE": f"€{mae:,.0f}",
        "RMSE": f"€{rmse:,.0f}",
        "R²": f"{r2:.3f}",
        "MAPE": f"{mape:.2f}%",
    }


def train_models(X_train, X_test, y_train, y_test):
    """Train and evaluate multiple regression models."""
    models = {
        "Linear Regression": LinearRegression(),
        "Ridge": Ridge(alpha=10),
        "Random Forest": RandomForestRegressor(
            n_estimators=100,
            max_depth=15,
            min_samples_split=5,
            random_state=42,
            n_jobs=-1,
        ),
        "XGBoost": XGBRegressor(
            n_estimators=100,
            max_depth=7,
            learning_rate=0.1,
            random_state=42,
            n_jobs=-1,
        ),
        "LightGBM": LGBMRegressor(
            n_estimators=100,
            max_depth=7,
            learning_rate=0.1,
            random_state=42,
            n_jobs=-1,
            verbose=-1,
        ),
        "Gradient Boosting": GradientBoostingRegressor(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            random_state=42,
        ),
    }

    results = []
    trained_models = {}

    print("🤖 Training leakage-free models...\n")

    for name, model in models.items():
        print(f"Training {name}...")
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        metrics = evaluate_model(y_test, y_pred, name)
        cv_scores = cross_val_score(
            model, X_train, y_train, cv=5, scoring="r2", n_jobs=-1
        )

        metrics["CV R² Mean"] = f"{cv_scores.mean():.3f}"
        metrics["CV R² Std"] = f"{cv_scores.std():.3f}"
        results.append(metrics)
        trained_models[name] = model

        print(
            f"  R²: {metrics['R²']} | MAE: {metrics['MAE']} | "
            f"RMSE: {metrics['RMSE']} | MAPE: {metrics['MAPE']} | "
            f"CV R²: {cv_scores.mean():.3f} ± {cv_scores.std():.3f}"
        )

    return pd.DataFrame(results), trained_models


def get_feature_importance(model, feature_names, top_n=10):
    """Extract model feature importance."""
    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
    elif hasattr(model, "coef_"):
        importances = np.abs(model.coef_)
    else:
        return None

    return (
        pd.DataFrame({"Feature": feature_names, "Importance": importances})
        .sort_values("Importance", ascending=False)
        .head(top_n)
    )


if __name__ == "__main__":
    print("=" * 60)
    print("🏠 FUNDA HOUSE PRICE PREDICTION - MODEL TRAINING")
    print("=" * 60)

    df = pd.read_csv("data/processed/funda_featured.csv")
    from features import prepare_for_modeling

    X, y, feature_names = prepare_for_modeling(df)

    print(f"Samples: {X.shape[0]}")
    print(f"Leakage-free features: {X.shape[1]}")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    results_df, trained_models = train_models(
        X_train, X_test, y_train, y_test
    )

    print("\n" + "=" * 60)
    print("📊 MODEL COMPARISON")
    print("=" * 60)
    print(results_df.to_string(index=False))

    # Select by numeric R² rather than parsing formatted strings.
    r2_values = {
        name: r2_score(y_test, model.predict(X_test))
        for name, model in trained_models.items()
    }
    best_model_name = max(r2_values, key=r2_values.get)
    best_model = trained_models[best_model_name]

    print(f"\nBest model by test R²: {best_model_name}")

    importance = get_feature_importance(best_model, feature_names, top_n=10)
    if importance is not None:
        print("\n📈 Feature Importance:")
        print(importance.to_string(index=False))

    print("\n💾 Saving models...")
    for name, model in trained_models.items():
        filename = f"models/{name.replace(' ', '_').lower()}.pkl"
        joblib.dump(model, filename)

    joblib.dump(
        best_model,
        f"models/best_model_{best_model_name.replace(' ', '_').lower()}.pkl",
    )

    results_df.to_csv("models/model_comparison.csv", index=False)
    print(f"Saved {len(trained_models)} models and model comparison.")
