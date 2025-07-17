import streamlit as st
import joblib, numpy as np, pandas as pd
from catboost import CatBoostRegressor, Pool
from pathlib import Path


st.set_page_config(page_title="IT Salary Prediction", layout="wide", page_icon="💰")

@st.cache_resource
def load_salary_model():
    """Load salary prediction model and metadata"""
    MODEL_PATH = Path("models/best_salary_model_catboost.pkl")
    META_PATH  = Path("models/model_metadata_catboost.pkl")

    if not MODEL_PATH.exists() or not META_PATH.exists():
        st.error("🔴 Cannot find .pkl files in models/ folder. Check location!")
        st.stop()

    model: CatBoostRegressor = joblib.load(MODEL_PATH)
    meta  = joblib.load(META_PATH)
    
    return model, meta

model, meta = load_salary_model()

feature_columns      = meta["feature_columns"]
numeric_features     = meta["numeric_features"]
categorical_features = meta["categorical_features"]


EDLEVELS = [
    "Primary/elementary school",
    "Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)",
    "Some college/university study without earning a degree",
    "Associate degree (A.A., A.S., etc.)",
    "Bachelor's degree (B.A., B.S., B.Eng., etc.)",
    "Master's degree (M.A., M.S., M.Eng., MBA, etc.)",
    "Professional degree (JD, MD, Ph.D, Ed.D, etc.)",
    "Something else",
]
AGES = [
    "Under 18 years old", "18-24 years old", "25-34 years old",
    "35-44 years old", "45-54 years old", "55-64 years old",
    "65 years or older", "Unknown",
]
REGIONS = [
    'Northern America', 'Western Europe', 'Eastern Europe', 'Northern Europe',
    'Southern Europe', 'Southern Asia', 'South-eastern Asia', 'Eastern Asia',
    'Central Asia', 'South America', 'Central America', 'Caribbean',
    'Northern Africa', 'Western Africa', 'Middle Africa', 'Eastern Africa',
    'Southern Africa', 'Australia and New Zealand', 'Melanesia', 'Polynesia',
    'Other',
]

LANGUAGE_COLS = [c for c in feature_columns if c.startswith("Language_")]
DEVTYPE_COLS  = [c for c in feature_columns if c.startswith("DevType_")]

LANGUAGE_LABELS = {c: c.replace("Language_", "").replace("_", " ") for c in LANGUAGE_COLS}
DEVTYPE_LABELS  = {c: c.replace("DevType_", "").replace("_", " ") for c in DEVTYPE_COLS}

VALID_DEVTYPE_LABELS = [
    label.title()
    for label in DEVTYPE_LABELS.values()
    if "student" not in label.lower() and "other" not in label.lower()
]

ED_MAP = {
    "Primary/elementary school": 0,
    "Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)": 1,
    "Some college/university study without earning a degree": 2,
    "Associate degree (A.A., A.S., etc.)": 3,
    "Bachelor's degree (B.A., B.S., B.Eng., etc.)": 4,
    "Master's degree (M.A., M.S., M.Eng., MBA, etc.)": 5,
    "Professional degree (JD, MD, Ph.D, Ed.D, etc.)": 6,
    "Something else": 7,
}


st.title("💰 Salary Prediction for IT Career")

with st.sidebar:
    st.header("📊 Model Information")
    
    st.success("**🏆 Active model:** CatBoost Regressor")
    st.metric("MAE (Test)", f"${meta['test_mae']:,.0f}")
    st.metric("RMSE (Test)", f"${meta['test_rmse']:,.0f}")
    
    with st.expander("🎯 What do MAE and RMSE mean?"):
        st.markdown("""
        **📏 MAE (Mean Absolute Error)**
        - Average absolute error in dollars
        - How much the prediction deviates, on average, from the real salary
        - **Example:** MAE = $5,000 means that, on average, the prediction can be +- 5,000 dollars different from the real salary.
                            
        **📊 RMSE (Root Mean Squared Error)**
        - Root mean squared error (more sensitive to large errors)
        - Penalizes very wrong predictions more
        - **Example:** RMSE = $8,000 means there are some predictions with larger errors
        
        **🔍 How to interpret:**
        - The smaller the values, the more accurate the model
        - MAE gives you an idea about the "typical" error
        - RMSE shows you if there are very wrong predictions
        
        """)

    st.markdown("---")
    st.markdown("**🎯 How it works:**")
    st.markdown("1. Complete your profile")
    st.markdown("2. AI analyzes the data")
    st.markdown("3. Receive salary estimate")

with st.sidebar:
    st.image("https://cdn.sstatic.net/Sites/stackoverflow/company/img/logos/so/so-logo.png", width=110)
    st.markdown("""
    <div style='text-align:center; font-size:1.1rem; font-weight:600; margin-bottom:0.3em;'>
        Thesis 2025<br>
        <span style="font-weight:400;font-size:0.97em;">Elena-Luiza JALEA</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")


st.markdown("---")
st.subheader("📋 Complete your professional profile")

with st.form("salary_form"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**👤 Personal data**")
        age = st.selectbox("Age group", AGES)
        years_code = st.number_input("Years of coding experience", 0, 60, 5, step=1)
        work_exp = st.number_input("Years of professional experience", 0, 60, 3, step=1)
    
    with col2:
        st.markdown("**🌍 Location and education**")
        region = st.selectbox("Geographic region", REGIONS)
        ed = st.selectbox("Education level", EDLEVELS)
    
    with col3:
        st.markdown("**💼 Work preferences**")
        dev_sel = st.selectbox("Desired role", VALID_DEVTYPE_LABELS)

    st.markdown("**🧑‍💻 Known programming languages**")
    langs_sel = st.multiselect("Select the languages you know:", LANGUAGE_LABELS.values())

    submitted = st.form_submit_button("💰 Estimate Salary", use_container_width=True)


def build_row() -> pd.DataFrame:
    row = pd.Series(0.0, index=feature_columns, dtype=float)

    row["EdLevel"] = ed
    row["Age"]     = age
    row["Region"]  = region

    row["YearsCode"] = years_code
    row["WorkExp"]   = work_exp

    for col, label in LANGUAGE_LABELS.items():
        if label.title() in langs_sel:
            row[col] = 1

    for col, label in DEVTYPE_LABELS.items():
        row[col] = 1 if label.title() == dev_sel else 0

    row["languages_count"]  = row[LANGUAGE_COLS].sum()
    row["years_prof_ratio"] = work_exp / max(years_code, 1e-6)
    row["coding_gap_years"] = max(years_code - work_exp, 0)
    row["EdLevel_ord"]      = ED_MAP.get(ed, 7)

    return row.to_frame().T

st.markdown("""
<style>
.salary-container {
    background: linear-gradient(135deg, #f48024 0%, #d96d00 100%);
    padding: 30px;
    border-radius: 15px;
    margin: 20px 0;
    box-shadow: 0 8px 32px rgba(244, 128, 36, 0.37);
    text-align: center;
}
.salary-title {
    color: white;
    font-size: 1.5rem;
    font-weight: bold;
    margin-bottom: 20px;
}
.salary-amount {
    color: white;
    font-size: 3rem;
    font-weight: bold;
    margin: 10px 0;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}
.salary-subtitle {
    color: rgba(255, 255, 255, 0.9);
    font-size: 1.1rem;
    margin-bottom: 15px;
}
.so-footer {
    margin-top: 2.4rem;
    background: none;
    color: #888;
    font-size: 1.03rem;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)


if submitted:
    try:
        with st.spinner("🔄 Analyzing your profile and calculating salary estimate..."):
            new_df = build_row()
            cat_runtime = categorical_features + ["EdLevel"]
            cat_idx = [new_df.columns.get_loc(c) for c in cat_runtime if c in new_df.columns]

            pred_log = model.predict(Pool(new_df, cat_features=cat_idx))[0]
            salary = np.expm1(pred_log)


        st.markdown("---")
        st.success("✅ Salary estimate generated successfully!")
        
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.markdown(f"### 💰 Estimate for: **{dev_sel}**")
        with col2:
            st.metric("🔧 Languages", len(langs_sel))
        with col3:
            st.metric("📅 Experience", f"{years_code} years")

        st.markdown(f"""
        <div class='salary-container'>
            <div class='salary-title'>💸 Annual Salary Estimate</div>
            <div class='salary-amount'>{salary:,.0f} $</div>
            <div class='salary-subtitle'>Estimated annual gross salary</div>

        </div>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Error generating estimate: {e}")
        st.info("Please try again or contact the administrator.")


st.markdown("---")
st.info("🤖 Model: CatBoost Regressor")

st.markdown("""
    <div class="so-footer">
    <hr>
    © 2025 Elena-Luiza JALEA · Stack Overflow Survey Thesis · Streamlit powered
            <br>
    <img src="https://upload.wikimedia.org/wikipedia/ro/a/a3/Logo_ASE.png?20140313161351" height="100" style="margin-bottom: -5px; opacity:0.92;" title="Bucharest University of Economic Studies"/>
    </br>
            </div>
""", unsafe_allow_html=True)