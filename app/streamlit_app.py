"""
Streamlit Dashboard for Funda Price Predictor

Run with: streamlit run app/streamlit_app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os


# Page config
st.set_page_config(
    page_title="Funda Price Predictor",
    page_icon="🏠",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 0rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)


@st.cache_resource
def load_model():
    """Load trained model"""
    try:
        model_data = joblib.load('models/best_model.pkl')
        return model_data
    except:
        return None


@st.cache_data
def load_data():
    """Load processed data for visualization"""
    try:
        df = pd.read_csv('data/processed/funda_processed.csv')
        return df
    except:
        return None


def predict_price(features, model_data):
    """Make price prediction"""
    model = model_data['model']
    scaler = model_data['scaler']
    feature_names = model_data['feature_names']
    
    # Create DataFrame with correct feature order
    input_df = pd.DataFrame([features], columns=feature_names)
    
    # Fill missing with 0
    input_df = input_df.fillna(0)
    
    # Scale and predict
    input_scaled = scaler.transform(input_df)
    prediction = model.predict(input_scaled)[0]
    
    return prediction


def main():
    # Header
    st.title("🏠 Funda Price Predictor")
    st.markdown("### Predict house prices in the Netherlands using Machine Learning")
    
    # Sidebar
    st.sidebar.header("Navigation")
    page = st.sidebar.radio("Go to", ["🔮 Price Predictor", "📊 Data Explorer", "📈 Model Performance"])
    
    # Load resources
    model_data = load_model()
    df = load_data()
    
    # ============================================
    # PAGE 1: PRICE PREDICTOR
    # ============================================
    if page == "🔮 Price Predictor":
        st.header("Predict House Price")
        
        if model_data is None:
            st.error("❌ Model not found. Please train the model first using `src/models.py`")
            return
        
        # Input form
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Property Details")
            
            living_area = st.number_input(
                "Living Area (m²)", 
                min_value=20, 
                max_value=500, 
                value=100,
                step=5
            )
            
            rooms = st.number_input(
                "Number of Rooms", 
                min_value=1, 
                max_value=15, 
                value=4,
                step=1
            )
            
            bedrooms = st.number_input(
                "Number of Bedrooms", 
                min_value=1, 
                max_value=10, 
                value=3,
                step=1
            )
            
            build_year = st.number_input(
                "Build Year", 
                min_value=1900, 
                max_value=2024, 
                value=1990,
                step=1
            )
        
        with col2:
            st.subheader("Additional Features")
            
            energy_label = st.selectbox(
                "Energy Label",
                ["A+++++", "A++++", "A+++", "A++", "A+", "A", "B", "C", "D", "E", "F", "G"]
            )
            
            plot_area = st.number_input(
                "Plot Area (m²)", 
                min_value=0, 
                max_value=2000, 
                value=120,
                step=10
            )
            
            house_type = st.selectbox(
                "House Type",
                ["Appartement", "Tussenwoning", "Hoekwoning", "Vrijstaande woning", "2-onder-1-kapwoning"]
            )
        
        # Calculate derived features
        current_year = datetime.now().year
        house_age = current_year - build_year
        price_per_m2 = 0  # Will be calculated after prediction
        has_garden = 1 if plot_area > living_area else 0
        
        # Energy score mapping
        energy_mapping = {
            'A+++++': 7, 'A++++': 6, 'A+++': 5, 'A++': 4, 'A+': 3, 'A': 2,
            'B': 1, 'C': 0, 'D': -1, 'E': -2, 'F': -3, 'G': -4
        }
        energy_score = energy_mapping.get(energy_label, 0)
        
        # Prepare features dictionary
        features = {
            'living_area_m2': living_area,
            'plot_area_m2': plot_area,
            'rooms': rooms,
            'bedrooms': bedrooms,
            'build_year': build_year,
            'house_age': house_age,
            'energy_score': energy_score,
            'has_garden': has_garden,
            'price_per_m2': 0,  # Placeholder
        }
        
        # Add dummy columns for one-hot encoded features
        # (This is simplified - in production, handle this properly)
        for fname in model_data['feature_names']:
            if fname not in features:
                features[fname] = 0
        
        # Predict button
        if st.button("🔮 Predict Price", type="primary"):
            with st.spinner("Predicting..."):
                try:
                    prediction = predict_price(features, model_data)
                    
                    # Display result
                    st.success("✅ Prediction Complete!")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Predicted Price", f"€{prediction:,.0f}")
                    
                    with col2:
                        price_per_m2 = prediction / living_area
                        st.metric("Price per m²", f"€{price_per_m2:,.0f}")
                    
                    with col3:
                        # Estimate range (±10%)
                        lower = prediction * 0.9
                        upper = prediction * 1.1
                        st.metric("Estimated Range", f"€{lower:,.0f} - €{upper:,.0f}")
                    
                    # Additional info
                    st.info("""
                    **💡 Note:** This is a machine learning prediction based on historical data. 
                    Actual prices may vary based on location, market conditions, and property condition.
                    """)
                    
                except Exception as e:
                    st.error(f"Error making prediction: {e}")
    
    # ============================================
    # PAGE 2: DATA EXPLORER
    # ============================================
    elif page == "📊 Data Explorer":
        st.header("Data Explorer")
        
        if df is None:
            st.error("❌ Data not found. Please run the scraper first.")
            return
        
        st.write(f"**Total listings:** {len(df)}")
        
        # Summary statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_price = df['price'].mean()
            st.metric("Average Price", f"€{avg_price:,.0f}")
        
        with col2:
            avg_m2 = df['living_area_m2'].mean()
            st.metric("Average Size", f"{avg_m2:.0f} m²")
        
        with col3:
            avg_rooms = df['rooms'].mean()
            st.metric("Average Rooms", f"{avg_rooms:.1f}")
        
        with col4:
            median_year = df['build_year'].median()
            st.metric("Median Build Year", f"{int(median_year)}")
        
        # Visualizations
        st.subheader("Price Distribution")
        
        # Price histogram
        fig = px.histogram(
            df, 
            x='price', 
            nbins=50,
            title='Distribution of House Prices',
            labels={'price': 'Price (€)'}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Price vs Area scatter
        st.subheader("Price vs Living Area")
        fig = px.scatter(
            df, 
            x='living_area_m2', 
            y='price',
            color='rooms',
            title='House Price vs Living Area',
            labels={'living_area_m2': 'Living Area (m²)', 'price': 'Price (€)'}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Data table
        st.subheader("Sample Data")
        st.dataframe(df.head(20))
    
    # ============================================
    # PAGE 3: MODEL PERFORMANCE
    # ============================================
    elif page == "📈 Model Performance":
        st.header("Model Performance")
        
        if model_data is None:
            st.error("❌ Model not found.")
            return
        
        # Display model metrics (if available)
        st.info("Model performance metrics will be displayed here after training.")
        
        # Show feature importance plot if available
        if os.path.exists('data/processed/model_comparison.png'):
            st.subheader("Model Comparison")
            st.image('data/processed/model_comparison.png')
        
        if os.path.exists('data/processed/feature_importance_random_forest.png'):
            st.subheader("Feature Importance")
            st.image('data/processed/feature_importance_random_forest.png')


if __name__ == "__main__":
    main()
