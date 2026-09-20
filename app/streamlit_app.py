"""Funda House Price Predictor - Streamlit Dashboard.

The dashboard uses the committed leakage-free model artifacts and does not
ship or expose the scraped Funda dataset.
"""

import joblib
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Funda Price Predictor", page_icon="🏠", layout="wide")

@st.cache_resource
def load_model():
    return joblib.load("models/best_model_gradient_boosting.pkl")

@st.cache_data
def load_comparison():
    return pd.read_csv("models/model_comparison.csv")

model = load_model()

st.sidebar.title("🏠 Funda Price Predictor")
st.sidebar.markdown("---")
page = st.sidebar.radio("Navigation", ["🏠 Price Predictor", "🤖 Model Performance"])

if page == "🏠 Price Predictor":
    st.title("🏠 House Price Predictor")
    st.markdown("Enter house details to generate a prediction with the committed leakage-free Gradient Boosting model.")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📍 Location & Size")
        city = st.selectbox("City", ["Amsterdam", "Utrecht", "Rotterdam", "Den Haag", "Eindhoven"])
        area = st.slider("Living Area (m²)", 20, 300, 100)
        rooms = st.slider("Number of Rooms", 1, 10, 4)
        bedrooms = st.slider("Number of Bedrooms", 1, 8, 2)

    with col2:
        st.subheader("🏗️ Building Info")
        build_year = st.slider("Build Year", 1900, 2026, 2000)
        energy_label = st.selectbox("Energy Label", ["A+++", "A++", "A+", "A", "B", "C", "D", "E", "F", "G"])

    house_age = 2026 - build_year
    is_new = 1 if house_age < 5 else 0
    energy_map = {"A+++": 10, "A++": 9, "A+": 8, "A": 7, "B": 6, "C": 5, "D": 4, "E": 3, "F": 2, "G": 1}
    energy_score = energy_map[energy_label]
    room_area_ratio = rooms / area

    if st.button("🔮 Predict Price", type="primary", use_container_width=True):
        city_encoded = {
            "city_Den Haag": 1 if city == "Den Haag" else 0,
            "city_Eindhoven": 1 if city == "Eindhoven" else 0,
            "city_Rotterdam": 1 if city == "Rotterdam" else 0,
            "city_Utrecht": 1 if city == "Utrecht" else 0,
        }
        input_data = pd.DataFrame([{
            "living_area_m2": area,
            "rooms": rooms,
            "bedrooms_filled": bedrooms,
            "house_age_filled": house_age,
            "energy_score_filled": energy_score,
            "room_area_ratio": room_area_ratio,
            "has_build_year": 1,
            "has_energy_label": 1,
            "has_bedrooms": 1,
            "is_new": is_new,
            **city_encoded,
        }])
        try:
            prediction = model.predict(input_data)[0]
            st.success("✅ Prediction Complete!")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("💰 Predicted Price", f"€{prediction:,.0f}")
            with c2:
                st.metric("📏 Predicted Price per m²", f"€{prediction / area:,.0f}")
            with c3:
                st.metric("📐 Living Area", f"{area} m²")
            with st.expander("📋 Prediction Details"):
                st.write(f"**Location:** {city}")
                st.write(f"**Living Area:** {area} m²")
                st.write(f"**Rooms:** {rooms} ({bedrooms} bedrooms)")
                st.write(f"**Build Year:** {build_year} ({house_age} years old)")
                st.write(f"**Energy Label:** {energy_label}")
                st.write(f"**New Construction:** {'Yes' if is_new else 'No'}")
        except ValueError as exc:
            st.error("The saved model does not match the current feature schema. Please use the committed leakage-free model artifact.")
            st.caption(f"Model validation message: {exc}")

elif page == "🤖 Model Performance":
    st.title("🤖 Model Performance")
    st.info("The previously published 0.990 R² result used price_per_m2, a target-derived feature. It is treated as historical and is not used as a valid benchmark.")
    st.subheader("Current Leakage-Free Model Comparison")
    comparison = load_comparison()
    st.dataframe(comparison, use_container_width=True)
    st.caption("Six regression models show similar hold-out performance in the current leakage-free benchmark.")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📦 Portfolio Version")
st.sidebar.markdown("- Leakage-free model inputs")
st.sidebar.markdown("- Scraped dataset not distributed")
st.sidebar.markdown("- Six-model benchmark")
