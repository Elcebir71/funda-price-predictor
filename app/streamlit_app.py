"""
Funda House Price Predictor - Streamlit Dashboard

The dashboard intentionally does not use price_per_m2 as an input feature.
That value is derived from the target price and would cause target leakage.
"""

import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

st.set_page_config(
    page_title="Funda Price Predictor",
    page_icon="🏠",
    layout="wide"
)

@st.cache_resource
def load_model():
    return joblib.load('models/best_model_gradient_boosting.pkl')

@st.cache_data
def load_data():
    return pd.read_csv('data/processed/funda_featured.csv')

model = load_model()
df = load_data()

st.sidebar.title("🏠 Funda Price Predictor")
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Navigation",
    ["🏠 Price Predictor", "📊 Data Explorer", "🤖 Model Performance"]
)

if page == "🏠 Price Predictor":
    st.title("🏠 House Price Predictor")
    st.markdown("Enter house details to get a price prediction.")

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

    house_age = 2026 - build_year
    is_new = 1 if house_age < 5 else 0

    energy_map = {
        'A+++': 10, 'A++': 9, 'A+': 8, 'A': 7,
        'B': 6, 'C': 5, 'D': 4, 'E': 3, 'F': 2, 'G': 1
    }
    energy_score = energy_map[energy_label]
    room_area_ratio = rooms / area

    if st.button("🔮 Predict Price", type="primary", use_container_width=True):
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
            'room_area_ratio': room_area_ratio,
            'has_build_year': 1,
            'has_energy_label': 1,
            'has_bedrooms': 1,
            'is_new': is_new,
            **city_encoded
        }])

        try:
            prediction = model.predict(input_data)[0]
            st.success("✅ Prediction Complete!")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("💰 Predicted Price", f"€{prediction:,.0f}")

            with col2:
                st.metric(
                    "📏 Predicted Price per m²",
                    f"€{prediction / area:,.0f}"
                )

            with col3:
                st.metric("📐 Living Area", f"{area} m²")

            with st.expander("📋 Prediction Details"):
                st.write(f"**Location:** {city}")
                st.write(f"**Living Area:** {area} m²")
                st.write(f"**Rooms:** {rooms} ({bedrooms} bedrooms)")
                st.write(f"**Build Year:** {build_year} ({house_age} years old)")
                st.write(f"**Energy Label:** {energy_label}")
                st.write(
                    f"**New Construction:** {'Yes' if is_new else 'No'}"
                )

        except ValueError as exc:
            st.error(
                "The saved model was trained with an older feature set. "
                "Please retrain the models with the current leakage-free "
                "feature pipeline before using the predictor."
            )
            st.caption(f"Model validation message: {exc}")

elif page == "📊 Data Explorer":
    st.title("📊 Data Explorer")

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

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("💰 Price Distribution")
        fig = px.histogram(
            df, x='price', nbins=50,
            title="Price Distribution",
            labels={'price': 'Price (€)', 'count': 'Count'}
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("📏 Area Distribution")
        fig = px.histogram(
            df, x='living_area_m2', nbins=50,
            title="Living Area Distribution",
            labels={'living_area_m2': 'Area (m²)', 'count': 'Count'}
        )
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("🏙️ Average Price by City")
    city_avg = df.groupby('city')['price'].mean().sort_values(ascending=False)
    fig = px.bar(
        x=city_avg.index,
        y=city_avg.values,
        labels={'x': 'City', 'y': 'Average Price (€)'},
        title="Average House Price by City"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📊 Price vs Living Area")
    fig = px.scatter(
        df, x='living_area_m2', y='price', color='city',
        title="Price vs Living Area",
        labels={'living_area_m2': 'Living Area (m²)', 'price': 'Price (€)'},
        hover_data=['rooms', 'city']
    )
    st.plotly_chart(fig, use_container_width=True)

elif page == "🤖 Model Performance":
    st.title("🤖 Model Performance")

    st.warning(
        "⚠️ The previously published 0.990 R² result used "
        "price_per_m2, a target-derived feature. Those metrics are "
        "not presented as valid model performance. Retrain the models "
        "with the current leakage-free feature pipeline."
    )

    comparison_path = 'models/model_comparison.csv'

    try:
        comparison = pd.read_csv(comparison_path)
        st.subheader("Previous Model Comparison")
        st.dataframe(comparison, use_container_width=True)
        st.caption(
            "Historical results only — they must not be interpreted as "
            "leakage-free performance."
        )
    except FileNotFoundError:
        st.info("No model comparison file is available yet.")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Dataset Info")
st.sidebar.markdown(f"- **Listings:** {len(df):,}")
st.sidebar.markdown("- **Cities:** 5")
st.sidebar.markdown("- **Model features:** leakage-free pipeline")
st.sidebar.markdown("- **Target:** House price (€)")
