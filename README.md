# 🏠 Funda House Price Predictor

ML-powered house price prediction system for the Netherlands real estate market.

## 🎯 Live Demo

🚀 **[Try it live on Streamlit!](https://funda-price-predictor-8jrrmtbezmxhjwbtwczyqg.streamlit.app)**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://funda-price-predictor-8jrrmtbezmxhjwbtwczyqg.streamlit.app)

---

## 📊 Project Overview

End-to-end machine learning pipeline that predicts house prices in the Netherlands with **99% accuracy**.

### Key Metrics
- **Dataset:** 1,017 real listings from 5 Dutch cities
- **Accuracy:** R² = 0.990 (99%)
- **Average Error:** €15,624 (2.43% MAPE)
- **Best Model:** Gradient Boosting

### Cities Covered
🏙️ Amsterdam | Utrecht | Rotterdam | Den Haag | Eindhoven

---

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/Elcebir71/funda-price-predictor.git
cd funda-price-predictor
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Dashboard
```bash
streamlit run app/streamlit_app.py
```

Visit: `http://localhost:8501`

---

## 📈 Features

### 🏠 Price Predictor
Interactive tool to predict house prices based on:
- Location (city)
- Living area (m²)
- Number of rooms & bedrooms
- Build year
- Energy label

### 📊 Data Explorer
- Dataset statistics and distributions
- Interactive visualizations
- City-wise price comparisons
- Price vs Area correlations

### 🤖 Model Performance
- Model comparison (6 algorithms)
- Feature importance analysis
- Evaluation metrics (R², MAE, RMSE, MAPE)

---

## 🛠️ Technologies

### Data Collection
- **Web Scraping:** Selenium WebDriver
- **HTML Parsing:** BeautifulSoup4
- **Data Sources:** Funda.nl (1,017 listings)

### Machine Learning
- **scikit-learn:** Model training & evaluation
- **XGBoost:** Gradient boosting
- **LightGBM:** Light gradient boosting
- **Pandas & NumPy:** Data processing

### Dashboard
- **Streamlit:** Web application framework
- **Plotly:** Interactive visualizations
- **Deployment:** Streamlit Community Cloud

---

## 🤖 Model Comparison

| Model | R² Score | MAE | RMSE | MAPE |
|-------|----------|-----|------|------|
| **Gradient Boosting** 🥇 | **0.990** | **€15,624** | €27,647 | 2.43% |
| XGBoost 🥈 | 0.989 | €14,362 | €29,161 | 2.38% |
| Random Forest 🥉 | 0.981 | €16,260 | €38,126 | 2.45% |
| Linear Regression | 0.940 | €47,879 | €68,385 | 9.66% |
| Ridge | 0.928 | €49,682 | €74,752 | 9.69% |
| LightGBM | 0.942 | €24,562 | €66,994 | 3.39% |

---

## 📊 Feature Importance

The model identified these key price drivers:

1. **Living Area (m²)** — 66.6% 🏠
2. **Price per m²** — 32.9% 💰
3. **Room/Area Ratio** — 0.2%
4. **Energy Score** — 0.1%
5. **House Age** — 0.1%

**Key Insight:** Living area is the dominant factor, accounting for **2/3 of price variation**.

---

## 📁 Project Structure
```
funda-price-predictor/
├── app/
│   └── streamlit_app.py         # Streamlit dashboard
├── src/
│   ├── scraper.py               # Web scraping (Selenium)
│   ├── features.py              # Feature engineering
│   └── models.py                # Model training
├── data/
│   ├── raw/
│   │   └── funda_cleaned.csv    # Cleaned scraped data
│   └── processed/
│       └── funda_featured.csv   # Engineered features
├── models/
│   └── *.pkl                    # Trained models
├── notebooks/
│   └── 01_eda.ipynb            # Exploratory analysis
├── requirements.txt             # Python dependencies
└── README.md
```

---

## 🎯 Pipeline Workflow
```mermaid
graph LR
    A[Web Scraping] --> B[Data Cleaning]
    B --> C[Feature Engineering]
    C --> D[Model Training]
    D --> E[Model Evaluation]
    E --> F[Streamlit Dashboard]
    F --> G[Deployment]
```

1. **Scraping:** Selenium extracts 1,017 listings from Funda.nl
2. **Cleaning:** Remove outliers, handle missing values
3. **Features:** Create price_per_m², house_age, energy_score
4. **Training:** Compare 6 ML algorithms
5. **Evaluation:** Best model: Gradient Boosting (R²=0.990)
6. **Dashboard:** Interactive Streamlit app
7. **Deploy:** Live on Streamlit Community Cloud

---

## 🔬 Data Collection

### Scraping Details
```bash
# Scrape Amsterdam (10 pages)
python src/scraper.py --city amsterdam --max-pages 10

# Scrape all cities (overnight batch)
./scrape_overnight.sh
```

**Collected Features:**
- Price (€)
- Living area (m²)
- Number of rooms & bedrooms
- Build year
- Energy label (A+++ to G)
- Address & city
- Scraped timestamp

---

## 📈 Results

### Example Predictions

| City | Area | Rooms | Year | Energy | Predicted Price |
|------|------|-------|------|--------|----------------|
| Amsterdam | 150m² | 5 | 2021 | A+++ | €1,026,302 |
| Utrecht | 100m² | 4 | 2006 | A | €507,657 |
| Rotterdam | 85m² | 3 | 1996 | B | €364,662 |
| Eindhoven | 60m² | 2 | 1976 | D | €219,503 |

**Model Performance:**
- ✅ Accurately predicts prices across all cities
- ✅ Handles new construction vs old buildings
- ✅ Energy label premium correctly valued
- ✅ City-specific pricing captured

---

## 🔮 Future Improvements

- [ ] Add rental price prediction (separate model)
- [ ] Expand to 15+ Dutch cities
- [ ] Real-time Funda API integration
- [ ] Historical price trends
- [ ] Neighborhood-level analysis
- [ ] Investment ROI calculator

---

## ⚠️ Disclaimer

This project is for **educational purposes only**. Predictions are based on historical data and should not be used as the sole basis for real estate decisions. Always consult with real estate professionals.

---

## 📜 License

MIT License - see [LICENSE](LICENSE) for details

---

## 👤 Author

**Hakan Sahin**

- 🌐 Portfolio: [hakansahin.dev](https://hakansahin.dev)
- 💼 LinkedIn: [linkedin.com/in/hakan-sahin](#) <!-- Add your LinkedIn -->
- 🐙 GitHub: [@Elcebir71](https://github.com/Elcebir71)
- 📧 Email: your.email@example.com <!-- Add your email -->

---

## 🙏 Acknowledgments

- Data source: [Funda.nl](https://www.funda.nl)
- Deployment: [Streamlit Community Cloud](https://streamlit.io/cloud)
- ML Libraries: scikit-learn, XGBoost, LightGBM

---

**⭐ If you found this project helpful, please give it a star!**

