# 🏠 Funda Price Predictor

Machine Learning project for predicting house prices in the Netherlands using Funda.nl data.

## 📋 Project Overview

This project scrapes real estate listings from Funda.nl, performs feature engineering with external data sources (CBS, NS API), and builds a predictive model to estimate house prices.

**Key Features:**
- Web scraping from Funda.nl
- Geospatial feature engineering (distance to stations, city centers)
- Multiple ML models (Linear Regression, Random Forest, XGBoost)
- Interactive Streamlit dashboard
- Price prediction for new listings

## 🗂️ Project Structure

```
funda-price-predictor/
├── data/
│   ├── raw/                 # Raw scraped data
│   ├── processed/           # Cleaned data
│   └── external/            # CBS, postcode data
├── notebooks/
│   ├── 01_data_collection.ipynb
│   ├── 02_eda.ipynb
│   ├── 03_feature_engineering.ipynb
│   └── 04_modeling.ipynb
├── src/
│   ├── scraper.py          # Funda scraper
│   ├── features.py         # Feature engineering
│   ├── models.py           # ML models
│   └── utils.py            # Helper functions
├── app/
│   └── streamlit_app.py    # Web dashboard
├── requirements.txt
└── README.md
```

## 🚀 Quick Start

### 1. Installation

```bash
git clone https://github.com/yourusername/funda-price-predictor.git
cd funda-price-predictor
pip install -r requirements.txt
```

### 2. Data Collection

```bash
python src/scraper.py --city amsterdam --max-pages 10
```

### 3. Run Analysis

Open Jupyter notebooks in order (01 → 02 → 03 → 04)

### 4. Launch Dashboard

```bash
streamlit run app/streamlit_app.py
```

## 📊 Features Used

**Basic Features:**
- Price (target variable)
- Square meters (m²)
- Number of rooms (kamers)
- Build year (bouwjaar)
- Energy label
- House type (appartement, woning, etc.)

**Engineered Features:**
- Distance to nearest NS station
- Distance to city center
- Postcode-based income level (CBS data)
- Age of the house
- Price per m²

## 🎯 Model Performance

| Model | MAE | RMSE | R² |
|-------|-----|------|-----|
| Linear Regression | TBD | TBD | TBD |
| Random Forest | TBD | TBD | TBD |
| XGBoost | TBD | TBD | TBD |

## 📈 Results

- **Best Model**: [To be determined]
- **Key Insights**: [To be added after analysis]

## 🛠️ Technologies

- **Python 3.9+**
- **Data Collection**: BeautifulSoup, Selenium
- **Data Processing**: Pandas, NumPy
- **ML**: Scikit-learn, XGBoost
- **Visualization**: Matplotlib, Seaborn, Plotly
- **Web App**: Streamlit
- **Geospatial**: Folium, Geopy

## ⚠️ Disclaimer

This project is for educational purposes only. Please respect Funda.nl's terms of service and robots.txt when scraping data.

## 📝 License

MIT License

## 👤 Author

[Your Name]
- LinkedIn: [Your Profile]
- GitHub: [Your Profile]
