import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 🧭 Page Setup
st.set_page_config(
    page_title="AgriInsight",
    page_icon="🌾",
    layout="wide"
)

# 🌐 Language Selection
language = st.sidebar.radio("🌐 Select Language / भाषा चुनें", ["English", "हिन्दी"])

# 🔤 Text Labels
if language == "English":
    title = "🌾 AgriInsight AI – Crop Trend Analysis with Climate Correlation"
    caption = "Powered by data.gov.in datasets (2013–2022)"
    sidebar_header = "🔍 Filters"
    select_state = "Select State"
    select_crop = "Select Crop"
    chart_title = "{} Production vs Rainfall in {} (2013–2022)"
    corr_text = "📈 Correlation between rainfall and production: **{:.2f}**"
    sources_header = "**Data Sources:**"
    chatbot_header = "💬 Ask AgriInsight AI"
    chatbot_placeholder = "Ask a question about rainfall or crop production..."
    chatbot_info = "🤔 Try asking: 'highest production', 'average rainfall', or 'correlation'"
    footer = "Prototype by Ishita Bhatia | Digital Bharat Fellowship 2026 Submission"
else:
    title = "🌾 AgriInsight AI – फसल उत्पादन और वर्षा का विश्लेषण"
    caption = "data.gov.in डेटा (2013–2022) पर आधारित"
    sidebar_header = "🔍 फ़िल्टर"
    select_state = "राज्य चुनें"
    select_crop = "फसल चुनें"
    chart_title = "{} उत्पादन बनाम वर्षा ({}) में (2013–2022)"
    corr_text = "📈 वर्षा और उत्पादन के बीच संबंध: **{:.2f}**"
    sources_header = "**डेटा स्रोत:**"
    chatbot_header = "💬 AgriInsight AI से पूछें"
    chatbot_placeholder = "वर्षा या फसल उत्पादन से जुड़ा प्रश्न पूछें..."
    chatbot_info = "🤔 उदाहरण: 'सबसे अधिक उत्पादन', 'औसत वर्षा', या 'संबंध बताओ'"
    footer = "Ishita Bhatia द्वारा निर्मित | Digital Bharat Fellowship 2026 सबमिशन"

# 🧾 Header
st.title("🌾 AgriInsight")

if language == "English":
    tagline = "#### *Bringing agricultural and climate data together for better insights.*"
else:
    tagline = "#### *कृषि और जलवायु डेटा को एक साथ लाकर बेहतर समझ के लिए।*"

st.markdown(tagline)
st.caption(caption)

# 🗂️ Load Data
@st.cache_data
def load_data():
    crops = pd.read_csv("data/crop_production.csv")
    rain = pd.read_csv("data/rainfall_data.csv")
    return crops, rain

crop_data, rain_data = load_data()

# 🎛️ Sidebar Filters
st.sidebar.header(sidebar_header)
states = sorted(crop_data["State"].unique().tolist())
state = st.sidebar.selectbox(select_state, states)
crops = sorted(crop_data["Crop"].unique().tolist())
crop = st.sidebar.selectbox(select_crop, crops)

# 🔄 Filter and Merge
filtered_crop = crop_data[(crop_data["State"] == state) & (crop_data["Crop"] == crop)]
filtered_rain = rain_data[rain_data["State"] == state]
merged = pd.merge(filtered_crop, filtered_rain, on=["State", "Year"], how="inner")

# 📊 Visualization
if merged.empty:
    st.warning("No matching records found." if language == "English" else "इस चयन के लिए कोई रिकॉर्ड नहीं मिला।")
else:
    st.subheader(chart_title.format(crop, state))

    fig, ax1 = plt.subplots(figsize=(7, 4))  # Medium-sized chart
    ax2 = ax1.twinx()

    ax1.plot(merged["Year"], merged["Production"], "g-o", label="Production (tonnes)")
    ax2.plot(merged["Year"], merged["Rainfall (mm)"], "b-s", label="Rainfall (mm)")

    ax1.set_xlabel("Year" if language == "English" else "साल")
    ax1.set_ylabel("Production (tonnes)" if language == "English" else "उत्पादन (टन)", color="g")
    ax2.set_ylabel("Rainfall (mm)" if language == "English" else "वर्षा (मि.मी.)", color="b")

    ax1.legend(loc="upper left")
    ax2.legend(loc="upper right")

    st.pyplot(fig)

    # 📈 Correlation Analysis
    corr = merged["Production"].corr(merged["Rainfall (mm)"])
    st.success(corr_text.format(corr))

    # 🌟 Insight Summary
    if corr > 0.5:
        insight = f"🌦️ Higher rainfall generally increased {crop} production in {state}."
    elif corr < -0.5:
        insight = f"🌤️ Higher rainfall seems to decrease {crop} production in {state}."
    else:
        insight = f"☁️ Rainfall had a limited effect on {crop} production in {state}."

    if language == "हिन्दी":
        if corr > 0.5:
            insight = f"🌦️ अधिक वर्षा से {state} में {crop} उत्पादन बढ़ा।"
        elif corr < -0.5:
            insight = f"🌤️ अधिक वर्षा से {state} में {crop} उत्पादन घटा।"
        else:
            insight = f"☁️ वर्षा का {state} में {crop} उत्पादन पर बहुत कम प्रभाव पड़ा।"

    st.info(insight)

    # 📥 Download Report Button
    csv_data = merged.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download Analysis Data" if language == "English" else "⬇️ विश्लेषण डेटा डाउनलोड करें",
        data=csv_data,
        file_name=f"AgriInsight_{state}_{crop}.csv",
        mime="text/csv"
    )

    # 🧾 Data Table
    with st.expander("View Combined Dataset" if language == "English" else "संयुक्त डेटा देखें"):
        st.dataframe(merged)

# 💬 Chatbot Section
st.markdown("---")
st.subheader(chatbot_header)
question = st.text_input(chatbot_placeholder)

if question:
    q = question.lower()
    if "highest production" in q or "सबसे अधिक उत्पादन" in q:
        result = crop_data.groupby(["State", "Crop"])["Production"].max().reset_index()
        st.write("🌾 Highest production values by State and Crop:" if language == "English" else "🌾 राज्य और फसल के अनुसार सबसे अधिक उत्पादन:")
        st.dataframe(result)
    elif "lowest production" in q or "सबसे कम उत्पादन" in q:
        result = crop_data.groupby(["State", "Crop"])["Production"].min().reset_index()
        st.write("🌾 Lowest production values by State and Crop:" if language == "English" else "🌾 राज्य और फसल के अनुसार सबसे कम उत्पादन:")
        st.dataframe(result)
    elif "average rainfall" in q or "औसत वर्षा" in q:
        avg_rain = rain_data.groupby("State")["Rainfall (mm)"].mean().reset_index()
        st.write("☔ Average annual rainfall (2013–2022):" if language == "English" else "☔ औसत वार्षिक वर्षा (2013–2022):")
        st.dataframe(avg_rain)
    elif "correlation" in q or "संबंध" in q:
        merged_data = pd.merge(crop_data, rain_data, on=["State", "Year"], how="inner")
        corr = merged_data["Production"].corr(merged_data["Rainfall (mm)"])
        st.write(f"📈 Overall correlation between rainfall and crop production: **{corr:.2f}**" if language == "English" else f"📈 वर्षा और फसल उत्पादन के बीच कुल संबंध: **{corr:.2f}**")
    else:
        st.info(chatbot_info)

# 📚 Sources + Footer
st.markdown("---")
st.markdown(f"""
{sources_header}  
• Ministry of Agriculture & Farmers Welfare – *State/UT-wise Crop Production Data (2013–2022)*  
• India Meteorological Department (IMD) – *Annual Rainfall Data (2013–2022)*  
Data accessed via [data.gov.in](https://data.gov.in)
""")

st.caption(footer)
