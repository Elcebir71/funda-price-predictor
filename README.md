# 🏠 Funda House Price Predictor

ML-powered house price prediction system for the Netherlands real estate market.

> **Portfolio note:** This project has been updated to prevent target leakage. The previously published 0.990 R² result was produced with a target-derived feature and is therefore treated as a historical result, not as valid final model performance.

## 🎯 Live Demo

🚀 **[Try it live on Streamlit!](https://funda-price-predictor-8jrrmtbezmxhjwbtwczyqg.streamlit.app)**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://funda-price-predictor-8jrrmtbezmxhjwbtwczyqg.streamlit.app)

---

## 📊 Project Overview

An end-to-end machine learning pipeline for predicting house prices in the Netherlands.

### Dataset

- **1,017** real listings
- **5** Dutch cities
- Amsterdam, Utrecht, Rotterdam, Den Haag and Eindhoven
- Target: house price (€)

### Important ML Design Decision

The original version included a target-derived price-per-m² feature:

price_per_m2 = price / living_area_m2

Because price is the target variable, this feature contains information from the answer the model is supposed to predict. Using it creates **target leakage** and can make evaluation metrics look artificially strong.

The current feature pipeline removes this feature from model training and prediction inputs.

This is an intentional part of the project: identifying, explaining and correcting data leakage is an important machine-learning engineering practice.

---

## 🚀 Quick Start

### 1. Clone Repository

~~~bash
git clone https://github.com/Elcebir71/funda-price-predictor.git
cd funda-price-predictor
~~~

### 2. Install Dependencies

~~~bash
pip install -r requirements.txt
~~~

### 3. Rebuild Features

~~~bash
python src/features.py
~~~

### 4. Retrain Models

~~~bash
python src/models.py
~~~

### 5. Run Dashboard

~~~bash
streamlit run app/streamlit_app.py
~~~

Visit: http://localhost:8501

> **Important:** The committed model files and model-comparison CSV were generated before the leakage fix. Retrain the models using the current pipeline before treating new metrics or predictions as valid.

---

## 📈 Features

### 🏠 Price Predictor

Interactive tool to predict house prices based on information available before the target price is known:

- Location (city)
- Living area (m²)
- Number of rooms & bedrooms
- Build year
- Energy label

### 📊 Data Explorer

- Dataset statistics and distributions
- Interactive visualizations
- City-wise price comparisons
- Price vs area analysis

### 🤖 Model Training

The training pipeline compares six regression algorithms:

- Linear Regression
- Ridge
- Random Forest
- XGBoost
- LightGBM
- Gradient Boosting

Evaluation metrics include:

- R²
- MAE
- RMSE
- MAPE
- 5-fold cross-validation R²

---

## 🛠️ Technologies

### Data Collection

- **Web Scraping:** Selenium WebDriver
- **HTML Parsing:** BeautifulSoup4
- **Data Source:** Funda.nl
- **Dataset:** 1,017 listings

### Machine Learning

- **scikit-learn**
- **XGBoost**
- **LightGBM**
- **Pandas**
- **NumPy**
- **Joblib**

### Dashboard

- **Streamlit**
- **Plotly**
- **Streamlit Community Cloud**

---

## 📊 Feature Engineering

The current model uses non-target-derived features such as:

- Living area
- Number of rooms
- Number of bedrooms
- House age
- Energy score
- Room-to-area ratio
- Missing-value indicators
- City one-hot encoding
- New-construction indicator

Target-derived values such as price per m² are excluded from model inputs.

---

## 📁 Project Structure

~~~text
funda-price-predictor/
├── app/
│   └── streamlit_app.py
├── src/
│   ├── scraper.py
│   ├── features.py
│   └── models.py
├── data/
│   ├── raw/
│   │   └── funda_cleaned.csv
│   └── processed/
│       └── funda_featured.csv
├── models/
│   └── *.pkl
├── notebooks/
│   └── 01_eda.ipynb
├── requirements.txt
└── README.md
~~~

---

## 🎯 Pipeline Workflow

~~~mermaid
graph LR
    A[Web Scraping] --> B[Data Cleaning]
    B --> C[Feature Engineering]
    C --> D[Leakage Check]
    D --> E[Model Training]
    E --> F[Model Evaluation]
    F --> G[Streamlit Dashboard]
~~~

1. **Scraping:** Collect listings from Funda.nl
2. **Cleaning:** Handle missing values and prepare the dataset
3. **Feature engineering:** Build model features without target leakage
4. **Leakage check:** Exclude target-derived features
5. **Training:** Compare six regression algorithms
6. **Evaluation:** Use hold-out test data and cross-validation
7. **Dashboard:** Explore the data and generate predictions
8. **Deployment:** Streamlit Community Cloud

---

## 🔬 Data Collection

### Collected Features

- Price (€)
- Living area (m²)
- Number of rooms
- Number of bedrooms
- Build year
- Energy label
- Address
- City
- Scraped timestamp

Example scraping commands:

~~~bash
python src/scraper.py --city amsterdam --max-pages 10
./scrape_overnight.sh
~~~

---

## 🧠 What I Learned

This project demonstrates more than model training:

- Building an end-to-end data pipeline
- Web scraping and data preparation
- Feature engineering
- Regression model comparison
- Cross-validation
- Interactive data visualization
- Streamlit deployment
- **Detecting and correcting target leakage**
- Communicating model limitations honestly

---

## 🔮 Future Improvements

- [ ] Retrain and publish leakage-free benchmark results
- [ ] Add neighborhood-level features
- [ ] Expand to more Dutch cities
- [ ] Add historical price trends
- [ ] Improve hyperparameter tuning
- [ ] Add automated data-quality checks
- [ ] Add model explainability with SHAP
- [ ] Add automated model testing

---

## ⚠️ Disclaimer

This project is for educational and portfolio purposes. Predictions are based on historical listing data and should not be used as the sole basis for real-estate decisions.

---

## 📜 License

MIT License - see LICENSE for details

---

## 👤 Author

**Hakan Sahin**

- 🌐 [Portfolio](https://hakansahin.dev)
- 🐙 [GitHub](https://github.com/Elcebir71)

---

## 🙏 Acknowledgments

- Data source: [Funda.nl](https://www.funda.nl)
- Deployment: [Streamlit Community Cloud](https://streamlit.io/cloud)
- ML Libraries: scikit-learn, XGBoost, LightGBM
