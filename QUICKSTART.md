# 🚀 Quick Start Guide

Follow these steps to get your Funda Price Predictor up and running.

## Step 1: Setup Environment

**Check Python version first:**
```bash
python --version
# Should be Python 3.10 or higher
# If not: brew install python@3.11 (Mac) or download from python.org

# Or use the checker script:
python check_python_version.py
```

```bash
# Create project directory
mkdir funda-price-predictor
cd funda-price-predictor

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Collect Data

```bash
# Create necessary directories
mkdir -p data/raw data/processed models

# Scrape Funda listings (start small for testing)
python src/scraper.py --city amsterdam --max-pages 5 --delay 3

# This will create: data/raw/funda_amsterdam_TIMESTAMP.csv
```

**Important Notes:**
- Start with `--max-pages 5` to collect ~50 listings
- Use `--delay 3` to be respectful to Funda's servers
- Check robots.txt and terms of service before scraping

## Step 3: Explore the Data

Open Jupyter notebook:
```bash
jupyter notebook notebooks/02_eda.ipynb
```

Or create your own quick exploration:
```python
import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('data/raw/funda_amsterdam_LATEST.csv')

# Basic info
print(df.info())
print(df.describe())

# Quick plot
df['price'].hist(bins=30)
plt.xlabel('Price (€)')
plt.ylabel('Count')
plt.title('Distribution of House Prices')
plt.show()
```

## Step 4: Feature Engineering

```bash
# Process the raw data
python src/features.py
```

This will:
- Add derived features (house_age, price_per_m2, etc.)
- Encode categorical variables
- Save to: `data/processed/funda_processed.csv`

**Note:** Geospatial features are disabled by default (slow). Enable manually in the code if needed.

## Step 5: Train Models

```bash
# Train all models and evaluate
python src/models.py
```

This will:
- Train 6 different models (Linear, Ridge, Lasso, Random Forest, Gradient Boosting, XGBoost)
- Evaluate performance
- Save plots to `data/processed/`
- Save best model to `models/best_model.pkl`

## Step 6: Launch Dashboard

```bash
# Run Streamlit app
streamlit run app/streamlit_app.py
```

The dashboard will open in your browser at `http://localhost:8501`

## 📊 Using the Dashboard

**Three main pages:**

1. **🔮 Price Predictor**
   - Enter house details (m², rooms, build year, etc.)
   - Get instant price prediction
   - See estimated price range

2. **📊 Data Explorer**
   - View dataset statistics
   - Interactive charts
   - Explore price distributions

3. **📈 Model Performance**
   - See model comparison
   - View feature importance
   - Understand what drives prices

## 🎯 Next Steps

Once you have the basic version working:

1. **Collect More Data**
   - Scrape more pages: `--max-pages 50`
   - Add more cities: utrecht, rotterdam, den-haag

2. **Add Geospatial Features**
   - Enable geocoding in `src/features.py`
   - Add distance to stations, city centers

3. **Tune Models**
   - Hyperparameter optimization
   - Try different features
   - Cross-validation

4. **Improve Dashboard**
   - Add map visualization (Folium)
   - Compare multiple predictions
   - Export predictions to CSV

5. **Deploy Online**
   - Deploy to Streamlit Cloud (free)
   - Share with others
   - Add to your portfolio

## 🐛 Troubleshooting

**Scraper not working?**
- Check your internet connection
- Funda might have changed their HTML structure
- Use `--delay 5` for slower, more reliable scraping

**Model accuracy poor?**
- Need more data (aim for 200+ listings)
- Add more features (location, distance features)
- Try different hyperparameters

**Dashboard not loading model?**
- Make sure you ran `src/models.py` first
- Check that `models/best_model.pkl` exists

## 📚 Resources

- [Scikit-learn Documentation](https://scikit-learn.org/)
- [XGBoost Guide](https://xgboost.readthedocs.io/)
- [Streamlit Docs](https://docs.streamlit.io/)
- [Funda.nl](https://www.funda.nl/)

## ⚠️ Legal Notice

This project is for educational purposes only. Always:
- Respect robots.txt
- Follow Funda's terms of service
- Don't overload their servers
- Use reasonable delays between requests

Good luck with your project! 🚀
