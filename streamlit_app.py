import streamlit as st
import pickle
import pandas as pd

# ===== PAGE CONFIG =====
st.set_page_config(page_title="Health Predictor", page_icon="🧬", layout="wide")

# ===== LANGUAGE =====
language = st.selectbox("🌍 Select Language", ["English", "Tamil", "Hindi"])

texts = {
    "English": {
        "title": "Women Health Cycle Predictor",
        "personal": "Personal Details",
        "health": "Health Factors",
        "age": "Age",
        "bmi": "BMI",
        "cycle": "Cycle Length (days)",
        "stress": "Stress Level",
        "sleep": "Sleep Hours",
        "activity": "Activity Level",
        "water": "Water Intake (litres)",
        "pcos": "PCOS History",
        "predict": "Predict Now",
        "regular": "Cycle is Regular",
        "irregular": "Cycle is Irregular",
        "suggest": "Suggestions",
        "result": "Prediction Result",
        "bmi_chart": "BMI Analysis",
        "cycle_chart": "Cycle Analysis",
        "health_chart": "Health Factors"
    },
    "Tamil": {
        "title": "பெண்கள் ஆரோக்கிய சுழற்சி கணிப்பு",
        "personal": "தனிப்பட்ட விவரங்கள்",
        "health": "ஆரோக்கிய விவரங்கள்",
        "age": "வயது",
        "bmi": "உடல் எடை குறியீடு",
        "cycle": "சுழற்சி நாட்கள்",
        "stress": "மன அழுத்தம்",
        "sleep": "தூக்க நேரம்",
        "activity": "செயல்பாடு நிலை",
        "water": "தண்ணீர் உட்கொள்ளல்",
        "pcos": "PCOS வரலாறு",
        "predict": "கணிக்கவும்",
        "regular": "சுழற்சி சாதாரணம்",
        "irregular": "சுழற்சி சீரற்றது",
        "suggest": "பரிந்துரைகள்",
        "result": "முடிவு",
        "bmi_chart": "BMI பகுப்பாய்வு",
        "cycle_chart": "சுழற்சி பகுப்பாய்வு",
        "health_chart": "ஆரோக்கிய நிலை"
    },
    "Hindi": {
        "title": "महिला स्वास्थ्य चक्र भविष्यवाणी",
        "personal": "व्यक्तिगत जानकारी",
        "health": "स्वास्थ्य कारक",
        "age": "आयु",
        "bmi": "बीएमआई",
        "cycle": "चक्र अवधि",
        "stress": "तनाव स्तर",
        "sleep": "नींद के घंटे",
        "activity": "गतिविधि स्तर",
        "water": "पानी सेवन",
        "pcos": "पीसीओएस इतिहास",
        "predict": "पूर्वानुमान",
        "regular": "चक्र सामान्य है",
        "irregular": "चक्र अनियमित है",
        "suggest": "सुझाव",
        "result": "परिणाम",
        "bmi_chart": "बीएमआई विश्लेषण",
        "cycle_chart": "चक्र विश्लेषण",
        "health_chart": "स्वास्थ्य स्थिति"
    }
}

t = texts[language]

# ===== CUSTOM STYLE =====
st.markdown("""
<style>
.main {
    background-color: #0e1117;
}
h1, h2, h3 {
    color: #ff4b4b;
}
.stButton>button {
    background-color: #ff4b4b;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# ===== TITLE =====
st.title(f"🧬 {t['title']}")
st.markdown("---")

# ===== LOAD MODEL =====
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

# ===== INPUTS =====
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"👤 {t['personal']}")
    age = st.number_input(t["age"], 10, 60)
    bmi = st.number_input(t["bmi"], 10.0, 40.0)
    cycle = st.number_input(t["cycle"], 20, 60)

with col2:
    st.subheader(f"💊 {t['health']}")
    stress = st.selectbox(t["stress"], ["Low", "Medium", "High"])
    stress = ["Low", "Medium", "High"].index(stress)

    sleep = st.number_input(t["sleep"], 0, 12)

    activity = st.selectbox(t["activity"], ["Low", "Medium", "High"])
    activity = ["Low", "Medium", "High"].index(activity)

    water = st.number_input(t["water"], 0.0, 5.0)

    pcos = st.selectbox(t["pcos"], ["No", "Yes"])
    pcos = 1 if pcos == "Yes" else 0

st.markdown("---")

# ===== PREDICT =====
if st.button(f"🔍 {t['predict']}"):

    prediction = model.predict([[age, bmi, cycle, stress, sleep, activity, water, pcos]])

    st.subheader(f"📊 {t['result']}")

    if prediction[0] == 0:
        st.success(f"✅ {t['regular']}")
    else:
        st.error(f"❌ {t['irregular']}")
        st.subheader(f"💡 {t['suggest']}")

        if stress == 2:
            st.write("• Reduce stress")
        if sleep < 6:
            st.write("• Improve sleep")
        if water < 2:
            st.write("• Drink more water")
        if activity == 0:
            st.write("• Exercise regularly")
        if pcos == 1:
            st.write("• Consult doctor")

    st.markdown("---")

    # ===== CHARTS =====
    col3, col4 = st.columns(2)

    with col3:
        st.subheader(f"📈 {t['bmi_chart']}")
        bmi_df = pd.DataFrame({
            "Category": ["Underweight", "Normal", "Your BMI"],
            "Value": [18.5, 24.9, bmi]
        })
        st.bar_chart(bmi_df.set_index("Category"))

    with col4:
        st.subheader(f"📅 {t['cycle_chart']}")
        cycle_df = pd.DataFrame({
            "Type": ["Normal", "Your Cycle"],
            "Days": [28, cycle]
        })
        st.bar_chart(cycle_df.set_index("Type"))

    st.subheader(f"⚙️ {t['health_chart']}")
    health_df = pd.DataFrame({
        "Factor": ["Stress", "Sleep", "Activity", "Water"],
        "Value": [stress, sleep, activity, water]
    })
    st.bar_chart(health_df.set_index("Factor"))

# ===== FOOTER =====
st.markdown("---")
st.warning("⚠️ This is not medical advice. Consult a doctor.")