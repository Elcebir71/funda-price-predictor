"""
Funda House Price Predictor - Streamlit Dashboard
"""

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="Funda Price Predictor",
    page_icon="🏠",
    layout="wide"
)

# Load model and data
@st.cache_resource
def load_model():
    return joblib.load('models/best_model_gradient_boosting.pkl')

@st.cache_data
def load_data():
    return pd.read_csv('data/processed/funda_featured.csv')

model = load_model()
df = load_data()

# Sidebar
st.sidebar.title("🏠 Funda Price Predictor")
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Navigation",
    ["🏠 Price Predictor", "📊 Data Explorer", "🤖 Model Performance"]
)

# Page 1: Price Predictor
if page == "🏠 Price Predictor":
    st.title("🏠 House Price Predictor")
    st.markdown("Enter house details to get instant price prediction")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📍 Location & Size")
        city = st.selectbox(
            "City",
            ["Amsterdam", "Utrecht", "Rotterdam", "Den Haag", "Eindhoven"]
        )
        
        area = st.slider("Living Area (m²)", 20, 300, 100)
        rooms = st.slider("Number of Rooms", 1, 10, 4)
        bedrooms = st.slider("Number of Bedrooms", 1, 8, 2)
    
    with col2:
        st.subheader("🏗️ Building Info")
        build_year = st.slider("Build Year", 1900, 2026, 2000)
        
        energy_label = st.selectbox(
            "Energy Label",
            ["A+++", "A++", "A+", "A", "B", "C", "D", "E", "F", "G"]
        )
    
    # Calculate features
    house_age = 2026 - build_year
    is_new = 1 if house_age < 5 else 0
    
    energy_map = {
        'A+++': 10, 'A++': 9, 'A+': 8, 'A': 7,
        'B': 6, 'C': 5, 'D': 4, 'E': 3, 'F': 2, 'G': 1
    }
    energy_score = energy_map[energy_label]
    
    # Estimate price_per_m2 based on city
    city_price_m2 = {
        'Amsterdam': 6500,
        'Utrecht': 5000,
        'Rotterdam': 4200,
        'Den Haag': 4800,
        'Eindhoven': 3800
    }
    price_per_m2 = city_price_m2[city]
    room_area_ratio = rooms / area
    
    # Predict button
    if st.button("🔮 Predict Price", type="primary", use_container_width=True):
        # Prepare input
        city_encoded = {
            'city_Den Haag': 1 if city == 'Den Haag' else 0,
            'city_Eindhoven': 1 if city == 'Eindhoven' else 0,
            'city_Rotterdam': 1 if city == 'Rotterdam' else 0,
            'city_Utrecht': 1 if city == 'Utrecht' else 0
        }
        
        input_data = pd.DataFrame([{
            'living_area_m2': area,
            'rooms': rooms,
            'bedrooms_filled': bedrooms,
            'house_age_filled': house_age,
            'energy_score_filled': energy_score,
            'price_per_m2': price_per_m2,
            'room_area_ratio': room_area_ratio,
            'has_build_year': 1,
            'has_energy_label': 1,
            'has_bedrooms': 1,
            'is_new': is_new,
            **city_encoded
        }])
        
        # Predict
        prediction = model.predict(input_data)[0]
        
        # Display result
        st.success("✅ Prediction Complete!")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("💰 Predicted Price", f"€{prediction:,.0f}")
        
        with col2:
            low = prediction * 0.92
            high = prediction * 1.08
            st.metric("📉 Price Range", f"€{low:,.0f} - €{high:,.0f}")
        
        with col3:
            st.metric("📏 Price per m²", f"€{prediction/area:,.0f}")
        
        # Show details
        with st.expander("📋 Prediction Details"):
            st.write(f"**Location:** {city}")
            st.write(f"**Living Area:** {area} m²")
            st.write(f"**Rooms:** {rooms} ({bedrooms} bedrooms)")
            st.write(f"**Build Year:** {build_year} ({house_age} years old)")
            st.write(f"**Energy Label:** {energy_label}")
            st.write(f"**New Construction:** {'Yes' if is_new else 'No'}")

# Page 2: Data Explorer
elif page == "📊 Data Explorer":
    st.title("📊 Data Explorer")
    
    # Overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📦 Total Listings", f"{len(df):,}")
    
    with col2:
        st.metric("💰 Average Price", f"€{df['price'].mean():,.0f}")
    
    with col3:
        st.metric("📏 Average Area", f"{df['living_area_m2'].mean():.0f} m²")
    
    with col4:
        st.metric("🏙️ Cities", "5")
    
    st.markdown("---")
    
    # Price distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💰 Price Distribution")
        fig = px.histogram(
            df, x='price',
            nbins=50,
            title="Price Distribution",
            labels={'price': 'Price (€)', 'count': 'Count'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📏 Area Distribution")
        fig = px.histogram(
            df, x='living_area_m2',
            nbins=50,
            title="Living Area Distribution",
            labels={'living_area_m2': 'Area (m²)', 'count': 'Count'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Price by city
    st.subheader("🏙️ Average Price by City")
    city_avg = df.groupby('city')['price'].mean().sort_values(ascending=False)
    fig = px.bar(
        x=city_avg.index,
        y=city_avg.values,
        labels={'x': 'City', 'y': 'Average Price (€)'},
        title="Average House Price by City"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Price vs Area scatter
    st.subheader("📊 Price vs Living Area")
    fig = px.scatter(
        df, x='living_area_m2', y='price',
        color='city',
        title="Price vs Living Area",
        labels={'living_area_m2': 'Living Area (m²)', 'price': 'Price (€)'},
        hover_data=['rooms', 'city']
    )
    st.plotly_chart(fig, use_container_width=True)

# Page 3: Model Performance
elif page == "🤖 Model Performance":
    st.title("🤖 Model Performance")
    
    # Load comparison
    comparison = pd.read_csv('models/model_comparison.csv')
    
    st.subheader("📊 Model Comparison")
    st.dataframe(comparison, use_container_width=True)
    
    st.markdown("---")
    
    # Best model info
    st.success("🏆 Best Model: **Gradient Boosting** with R² = 0.990")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("R² Score", "0.990", "99% accuracy")
        st.metric("MAE", "€15,624", "Average error")
    
    with col2:
        st.metric("MAPE", "2.43%", "Percentage error")
        st.metric("RMSE", "€27,647", "Root MSE")
    
    # Feature importance
    st.subheader("📈 Feature Importance")
    
    importance_data = {
        'Feature': ['Living Area (m²)', 'Price per m²', 'Room/Area Ratio', 
                   'Energy Score', 'House Age', 'City'],
        'Importance': [66.6, 32.9, 0.2, 0.1, 0.1, 0.1]
    }
    
    fig = px.bar(
        importance_data,
        x='Importance',
        y='Feature',
        orientation='h',
        title="Top Features Influencing House Prices"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("💡 **Key Insight:** Living area (m²) is the most important factor, accounting for 66.6% of price variation!")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Dataset Info")
st.sidebar.markdown(f"- **Listings:** 1,017")
st.sidebar.markdown(f"- **Cities:** 5")
st.sidebar.markdown(f"- **Features:** 15")
st.sidebar.markdown(f"- **Model:** Gradient Boosting")
st.sidebar.markdown(f"- **Accuracy:** 99%")

