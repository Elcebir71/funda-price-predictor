# 🏠 Funda House Price Predictor

ML-powered house price prediction project for the Netherlands real-estate market.

> **Portfolio note:** The project was updated to remove target leakage. The previously published 0.990 R² result used a target-derived feature (price_per_m2) and is therefore treated as a historical result, not as valid final model performance.

## 🎯 Live Demo

🚀 **[Try it live on Streamlit](https://funda-price-predictor-8jrrmtbezmxhjwbtwczyqg.streamlit.app)**

The public demo is intentionally limited to the prediction workflow and model-performance comparison. The scraped Funda dataset is **not distributed in this repository**.

## 📊 Current Leakage-Free Benchmark

The current committed benchmark is based on the leakage-free feature pipeline:

| Model | R² | MAE | RMSE |
|---|---:|---:|---:|
| Linear Regression | 0.800 | €95,015 | €124,693 |
| Ridge | 0.800 | €92,325 | €124,724 |
| Random Forest | 0.790 | €89,336 | €127,736 |
| XGBoost | 0.785 | €89,678 | €129,119 |
| LightGBM | 0.798 | €87,212 | €125,281 |
| Gradient Boosting | 0.788 | €87,964 | €128,110 |

The six models have closely grouped R² values (0.785–0.800) on the current hold-out benchmark. With a dataset of 1,017 listings, these small differences should not be presented as a strong claim that one model is definitively superior.

The benchmark should **not** be compared directly with the historical 0.990 R² result because that result used target-derived information.

## 🧠 ML Design: Preventing Target Leakage

The original pipeline included:

    price_per_m2 = price / living_area_m2

Because price is the target, this feature leaks information from the answer into the model input.

The current pipeline excludes target-derived features and uses information that can be available before the target price is known, including:

- Living area
- Rooms and bedrooms
- House age
- Energy score
- Room-to-area ratio
- Missing-value indicators
- City one-hot encoding
- New-construction indicator

This leakage investigation is an intentional part of the portfolio project: the goal is to demonstrate not only model training, but also validation of the ML methodology.

## 🏗️ Project Architecture

    User inputs
        ↓
    Leakage-free feature construction
        ↓
    Committed Gradient Boosting model
        ↓
    Price prediction

    Training pipeline (local / authorized data only)
        ↓
    Feature engineering
        ↓
    Six-model comparison
        ↓
    Evaluation metrics
        ↓
    Model artifacts

## 🚀 Local Development

Install dependencies:

    pip install -r requirements.txt

Run the dashboard:

    streamlit run app/streamlit_app.py

Check the local Python version:

    python scripts/check_python_version.py

### Training

The training code remains available for reproducibility, but the source dataset is **not committed to the public repository**.

To retrain locally, provide a dataset you are authorized to use at:

    data/raw/funda_cleaned.csv

Then run:

    python src/features.py
    python src/models.py

Do not commit or redistribute scraped Funda data without the necessary permission or rights.

## 🛠️ Technologies

- Python
- Pandas / NumPy
- scikit-learn
- XGBoost
- LightGBM
- Joblib
- Streamlit

## 📁 Repository Structure

    funda-price-predictor/
    ├── app/
    │   └── streamlit_app.py
    ├── scripts/
    │   └── check_python_version.py
    ├── src/
    │   ├── features.py
    │   └── models.py
    ├── models/
    │   ├── best_model_gradient_boosting.pkl
    │   └── model_comparison.csv
    ├── notebooks/
    │   └── 01_eda.ipynb
    ├── requirements.txt
    ├── .gitignore
    └── README.md

The public repository intentionally does not contain the scraped raw or processed Funda datasets.

## 🔬 Evaluation

The training pipeline compares:

- Linear Regression
- Ridge
- Random Forest
- XGBoost
- LightGBM
- Gradient Boosting

Metrics:

- R²
- MAE
- RMSE
- MAPE
- 5-fold cross-validation R²

## 📌 Data and Terms

Funda's current Terms of Use state that, without prior written permission, users may not reproduce, copy, distribute, scrape, data-mine, make available, or otherwise exploit material from the Funda platform. The terms were amended on 6 March 2026.

For that reason, this portfolio repository does not redistribute the scraped Funda dataset and does not include a public scraping workflow.

This is a practical repository-cleanup decision, not a legal opinion. If you intend to collect or redistribute Funda data, obtain appropriate permission or use an authorized data source.

## ⚠️ Disclaimer

This project is for educational and portfolio purposes. Predictions are based on historical model training and should not be used as the sole basis for real-estate decisions.

## 👤 Author

**Hakan Sahin**

- 🌐 [Portfolio](https://hakansahin.dev)
- 🐙 [GitHub](https://github.com/Elcebir71)
