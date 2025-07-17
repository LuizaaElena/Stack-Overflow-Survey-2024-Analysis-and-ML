import streamlit as st
import time

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="wide"
)

with st.sidebar:
    st.image("https://cdn.sstatic.net/Sites/stackoverflow/company/img/logos/so/so-logo.png", width=110)
    st.markdown("""
    <div style='text-align:center; font-size:1.1rem; font-weight:600; margin-bottom:0.3em;'>
        Thesis 2025<br>
        <span style="font-weight:400;font-size:0.97em;">Elena-Luiza JALEA</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

# Animated progress bar on loading 
st.markdown("""
<style>
.stProgress > div > div > div > div {
    background-image: linear-gradient(90deg, #f48024 0%, #ffb95b 100%) !important;
    background-color: #f48024 !important;
}
</style>
""", unsafe_allow_html=True)

progress_text = "Loading application..."
my_bar = st.progress(0, text=progress_text)
for pct in range(0, 101, 13):
    time.sleep(0.3)
    my_bar.progress(pct, text=f"{progress_text} {pct}%")
my_bar.empty()

st.markdown("""
<style>        
body { background: #F5F6FA; }
.so-hero {
    background: linear-gradient(90deg, #ffe7bf 0%, #fff7ec 55%, #ffe7bf 100%);
    border-radius: 21px;
    padding: 2.3rem 2.7rem 2.2rem 2.4rem;
    margin-bottom: 2.2rem;
    display: flex; align-items: center; gap: 2.2rem;
    box-shadow: 0 8px 38px #ffe5bb80, 0 2px 12px #eaeaea;
    border: 1.6px solid #ffe5bb;
    position: relative;
    overflow: hidden;
}


.so-logo {
    border-radius: 12px;
    background: #fff;
    box-shadow: 0 3px 16px #ffe0b950;
    border: 2px solid #ffd79a;
    padding: 8px 12px;
}
.so-badge {
    background: #F48024;
    color: white;
    border-radius: 13px;
    padding: 0.23rem 1.05rem;
    font-size: 1.08rem;
    font-weight: 600;
    margin-right: 0.7rem;
    display: inline-flex;
    align-items: center;
    gap: 0.33rem;
    margin-bottom: 0.23rem;
    box-shadow: 0 2px 8px #ffd6a0a0;
}
.so-divider {
    height: 4px;
    width: 65px;
    border: none;
    background: linear-gradient(90deg, #f48024, #ffd6a0 90%);
    margin-top: 0.3rem;
    margin-bottom: 1.2rem;
    border-radius: 4px;
}
.so-btn {
    background: #f48024;
    color: white !important;
    border: none;
    border-radius: 16px;
    padding: 0.58rem 1.2rem;
    font-size: 1.12rem;
    font-weight: 700;
    box-shadow: 0 2px 14px #f480242a;
    cursor: pointer;
    margin-top: 1.1rem;
    transition: background 0.15s, box-shadow 0.17s;
    text-decoration: none;
    display: inline-block;
}
.so-btn:hover {
    background: #d96d00;
    box-shadow: 0 6px 24px #f4802440;
    color: #fff !important;
}
.so-card {
    background: #fff;
    border-radius: 20px;
    box-shadow: 0 2px 18px #ffe9cb80, 0 1px 8px #eee;
    padding: 1.3rem 1.3rem 1.1rem 1.3rem;
    margin-bottom: 2rem;
    min-height: 230px;
    display: flex; flex-direction: column; 
    border: 1px solid #ffe9cb;
    transition: box-shadow 0.20s, transform 0.18s;
    position: relative;
    overflow: hidden;
}
.so-card:hover {
    box-shadow: 0 10px 34px #ffd08088, 0 2px 12px #f4802410;
    transform: translateY(-4px) scale(1.018);
    z-index: 2;
}
.so-card h2 {
    color: #3a4149;
    margin-bottom: 0.55rem;
    display: flex; align-items: center; gap: 0.5rem;
}
.so-card ul {
    margin: 0;
    padding-left: 18px;
    font-size: 1.05rem;
}
.so-instructions {
    background: #fff8ea;
    border-left: 7px solid #f48024;
    border-radius: 14px;
    padding: 1.13rem 1.15rem 0.72rem 1.16rem;
    font-size: 1.15rem;
    margin-bottom: 1.33rem;
    color: #2d2e30;
    box-shadow: 0 1px 7px #f4802412;
    font-weight: 510;
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

st.markdown("""
    <div class="so-hero">
        <img src="https://cdn.sstatic.net/Sites/stackoverflow/company/img/logos/so/so-logo.png" height="85" class="so-logo"/>
        <div>
            <h1 style="margin-bottom: 0.14rem; color: #242729;">Stack Overflow Survey 2024 Analysis</h1>
            <hr class="so-divider">
            <div style="font-size: 1.18rem; margin-bottom: 0.34rem; color: #2c3135;">
                <b>Interactive exploration of data from the global developer community</b>
            </div>
            <div style="color: #444; font-size:1.09rem;">
                <span class="so-badge">👩🏻‍🎓 Elena-Luiza JALEA</span>
                <span class="so-badge">📅 2025</span>
            </div>
            <div style="margin-top:0.55rem; color:#222; font-size:1.07rem;">
                Explore the results of one of the most important surveys in the IT world, through interactive charts, advanced analysis and predictions generated with the help of machine learning.
            </div>
            <a href="https://survey.stackoverflow.co/" target="_blank" class="so-btn">View data source</a>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="so-instructions">
        Select a section to navigate between pages and discover the application's features.<br>
        <span style="color:#F48024; font-weight:600;">Each section can be quickly accessed from the sidebar menu.</span>
    </div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
        <div class="so-card">
        <h2>
            🌐 Descriptive Analysis
        </h2>
        <ul>
            <p>👉🏻 Explore data collected from Stack Overflow 2024 survey</p>
            <p>👉🏻 Discover trends related to career, technologies, education and AI</p>
        </ul>
        <div style="margin-top:0.8rem;">
            <span style="color: #f48024;"><b></b></span>
        </div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="so-card">
        <h2>
            🔎 Technology Recommendation
        </h2>
        <ul>
            <p>👉🏻 Choose what role you want to pursue in IT</p>
            <p>👉🏻 Get personalized recommendations for technologies and AI tools to learn</p>
        </ul>
        <div style="margin-top:0.8rem;">
            <span style="color: #f48024;"><b></b></span>
        </div>
        </div>
    """, unsafe_allow_html=True)


st.markdown("<br>", unsafe_allow_html=True)
col4, col5 = st.columns(2, gap="large")

with col4:
    st.markdown("""
        <div class="so-card">
        <h2>💰 Salary Estimation</h2>
        <ul>
            <p>👉🏻 Complete the form with your personal data and desired role</p>
            <p>👉🏻 Get annual salary prediction based on Stack Overflow 2024 survey data</p>
        </ul>
        </div>
    """, unsafe_allow_html=True)



with col5:
    st.markdown("""
        <div class="so-card">
        <h2>💬 Contact</h2>
        <ul>
            <p>👉🏻 luizajalea@email.com</p>
            <p>👉🏻 Bucharest University of Economic Studies</p>
        </ul>
        </div>
    """, unsafe_allow_html=True)

st.markdown("""
    <div class="so-footer">
    <hr>
    © 2025 Elena-Luiza JALEA · Stack Overflow Survey Thesis · Streamlit powered
            <br>
    <img src="https://upload.wikimedia.org/wikipedia/ro/a/a3/Logo_ASE.png?20140313161351" height="100" style="margin-bottom: -5px; opacity:0.92;" title="Bucharest University of Economic Studies"/>
    </br>
            </div>
""", unsafe_allow_html=True)