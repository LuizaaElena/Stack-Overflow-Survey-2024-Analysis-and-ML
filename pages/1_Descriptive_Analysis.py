from matplotlib import pyplot as plt
import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
from collections import Counter

st.set_page_config(
    page_title="Descriptive Analysis",
    page_icon="📊",
    layout="wide"
)

# === CSS for font and footer (like Home) ===
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap');
.block-container, .so-footer, h1, h2, h3, h4, h5, h6 {
    font-family: 'Inter', Arial, sans-serif !important;
    letter-spacing: 0.01em;
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

# === SIDEBAR with Home ===
with st.sidebar:
    st.image("https://cdn.sstatic.net/Sites/stackoverflow/company/img/logos/so/so-logo.png", width=110)
    st.markdown("""
    <div style='text-align:center; font-size:1.1rem; font-weight:600; margin-bottom:0.3em;'>
        Thesis 2025<br>
        <span style="font-weight:400;font-size:0.97em;">Elena-Luiza JALEA</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

# === Main tabs ===
st.title("Descriptive Analysis")
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs(["Overview", "Demographic Profile", "Education & Training", "Professional Profile", "Professional Experience", "Technologies Used", "Stack Overflow Usage", "Job Satisfaction & Psychosocial Aspects", "Attitude Towards AI"])


# === TAB 1: Overview ===
with tab1:
    st.markdown("""
    <div style='background:#fff8ea;border-radius:13px;padding:1.2rem 1.4rem 1rem 1.4rem;margin-bottom:1.2rem;
                box-shadow:0 1px 8px #ffd7a04e; border-left:6px solid #f48024;'>
        <h3 style='margin-bottom:0.8rem; color:#f48024;'>General Overview</h3>
        <p style="font-size:1.08rem; line-height:1.55em; margin-bottom:0.7rem; color:#383838;">
            This page offers an interactive and detailed exploration of responses from the <b>Stack Overflow Developer Survey 2024</b>,
            organized into nine thematic sections: demographics, education, professional profile, technologies, Stack Overflow usage, job satisfaction, and attitudes towards AI.
        </p>
        <p style="font-size:1.08rem; line-height:1.55em; margin-bottom:0.7rem; color:#383838;">
            🌍 Demographically, respondents come from a variety of countries, with a high proportion from the USA, Germany, and India, and most fall within the 25–34 age range, typical of the active IT workforce.
        </p>
        <p>
            🎓 From an educational perspective, bachelor's and master's degrees predominate, but alternative training paths are also notable, such as self-taught learning or peer support. This diversity is also reflected in knowledge acquisition methods, where official documentation and platforms like Stack Overflow occupy central positions.
        </p>
        <p>
            💼 The professional profile highlights a concentration on full-stack and back-end developer roles, alongside a preference for remote work and a broad distribution of organization sizes. Annual incomes show an asymmetric distribution, typical of financial data, while the level of job satisfaction is, on average, high. On the other hand, respondents signal various sources of frustration, especially related to technical complexity and "technical debt".     
        </p>
        <p>
            🌐 Stack Overflow usage is frequent, but most interactions are passive, through content consultation, not active participation.    
        </p>
        <p>
            🤖 Regarding AI, there is significant openness toward adopting these technologies, with perceived benefits such as automation, efficiency, and learning support, but also with a dose of caution and uncertainty regarding risks.  
        </p>
        <p style="font-size:1.06rem; color:#383838;">
            <i>Use the tabs above to explore these dimensions in detail.</i>
        </p>
    </div>
    """, unsafe_allow_html=True)


# === DATA ===
try:
    df = pd.read_csv("data/variabile_preprocesate.csv")
except Exception as e:
    st.error("Error loading data: " + str(e))
    df = pd.DataFrame()

# === TAB 2: Demographic Profile ===
with tab2:
    st.markdown("### 🌍 Distribution of respondents by country – Top 20")
    col1, col2 = st.columns([0.8, 2.2])

    with col1:
        with st.expander("🌍 Geographic interpretation"):
            st.markdown("""
            <ul style="font-size:0.92rem; padding-left:1rem; margin-top:0.2rem;">
                <li>At the top positions are <b>United States</b>, <b>Germany</b> and <b>India</b>, which together account for a significant volume of total global respondents.</li>
                <li>The global distribution is diverse, including both European countries (e.g. United Kingdom, Poland, France) and from other continents (e.g. Brazil, Australia, Canada).</li>
                <li>The high visibility of Central and Eastern European countries (e.g. Ukraine, Poland, Czech Republic) highlights active participation of developers from these regions.</li>
            </ul>
            """, unsafe_allow_html=True)


    with col2:
        if not df.empty and "Country" in df.columns:
            top_countries = df[df['Country'] != 'Unknown']['Country'].value_counts().head(20).reset_index()
            top_countries.columns = ["Country", "Count"]
            top_countries["Percent"] = round(100 * top_countries["Count"] / top_countries["Count"].sum(), 1)

            chart = alt.Chart(top_countries).mark_bar(color="#F48024").encode(
                x=alt.X("Country:N", sort="-y", title="Country"),
                y=alt.Y("Count:Q", title="Number of respondents"),
                tooltip=["Country", "Count", "Percent"]
            ).properties(width=750, height=380).configure_axis(
                labelFont="Inter",
                titleFont="Inter",
                labelFontSize=12,
                titleFontSize=13
            )

            st.altair_chart(chart, use_container_width=True)

    st.markdown("### Distribution of respondents by age groups")
    col1, col2 = st.columns([0.8, 2.2])

    with col1:
        with st.expander("🧠 Age interpretation"):
            st.markdown("""
            <ul style="font-size:0.92rem; padding-left:1rem; margin-top:0.2rem;">
                <li>The <b>25–34 years</b> group dominates the sample, indicating the average age of active professionals in technology.</li>
                <li>Followed by respondents aged between <b>35–44 years</b> and <b>18–24 years</b>, highlighting an important presence of both juniors and experienced specialists.</li>
                <li>The reduced proportion of participants over <b>45 years</b> suggests an industry oriented mainly towards younger generations.</li>
                <li>The <b>Under 18</b> and <b>65+</b> categories are marginal, reflecting limited involvement of minors and seniors in the survey.</li>
            </ul>
            """, unsafe_allow_html=True)


    with col2:
        if not df.empty and "Age" in df.columns:
            # Remove missing values and those with "Unknown" label explicitly
            df_age = df[(df["Age"].notna()) & (df["Age"] != "Unknown")].copy()

            # If data is numeric, apply binning
            if pd.api.types.is_numeric_dtype(df_age["Age"]):
                bins = [0, 17, 24, 34, 44, 54, 64, 100]
                labels = ["<18", "18-24", "25-34", "35-44", "45-54", "55-64", "65+"]
                df_age["Age_cat"] = pd.cut(df_age["Age"], bins=bins, labels=labels)
            else:
                df_age["Age_cat"] = df_age["Age"]

            # Count only valid values
            age_counts = df_age["Age_cat"].value_counts().reset_index()
            age_counts.columns = ["AgeGroup", "Count"]
            age_counts["AgeGroup"] = age_counts["AgeGroup"].astype(str)
            age_counts["Percent"] = round(100 * age_counts["Count"] / age_counts["Count"].sum(), 1)

            # Display chart
            chart = alt.Chart(age_counts).mark_bar(color="#F48024").encode(
                y=alt.Y("AgeGroup:N", sort="-x", title="Age"),
                x=alt.X("Count:Q", title="Number of respondents"),
                tooltip=["AgeGroup", "Count", "Percent"]
            ).properties(width=750, height=360).configure_axis(
                labelFont="Inter",
                titleFont="Inter",
                labelFontSize=12,
                titleFontSize=13
            )

            st.altair_chart(chart, use_container_width=True)

# === TAB 3: Education & Training ===
with tab3:
    st.markdown("### 🎓 Distribution by education level")
    col1, col2 = st.columns([0.8, 2.2])

    with col1:
        with st.expander("🎓 Educational level interpretation"):
            st.markdown("""
            <ul style="font-size:0.92rem; padding-left:1rem; margin-top:0.2rem;">
                <li>Most respondents hold a <b>bachelor's degree</b>, followed by those with a <b>master's degree</b>, reflecting a trend towards formal academic training among professionals.</li>
                <li>A considerable part of participants indicate <b>incomplete or alternative</b> educational levels, such as "Some college" or "Secondary school", suggesting diverse entry routes into the industry.</li>
                <li>The percentage of those with primary education or informal education is very low, but present, confirming the progressive accessibility of the IT field.</li>
                <li>The <i>"Something else"</i> category includes atypical responses or those that cannot be classified in standard educational systems.</li>
            </ul>
            """, unsafe_allow_html=True)


    with col2:
        if "EdLevel" in df.columns:
            ed_counts = df[df['EdLevel'] != 'Unknown']['EdLevel'].value_counts().reset_index()
            ed_counts.columns = ["Education", "Count"]
            ed_counts["Percent"] = round(100 * ed_counts["Count"] / ed_counts["Count"].sum(), 1)

            chart = alt.Chart(ed_counts).mark_bar(color="#F48024").encode(
                y=alt.Y("Education:N", sort="-x", title="Educational level"),
                x=alt.X("Count:Q", title="Number of respondents"),
                tooltip=["Education", "Count", "Percent"]
            ).properties(width=750, height=420).configure_axis(
                labelFont="Inter",
                titleFont="Inter"
            )
            st.altair_chart(chart, use_container_width=True)

    # LearnCode
    st.markdown("### 📘 Methods through which respondents learned to code")
    col1, col2 = st.columns([0.8, 2.2])

    with col1:
        with st.expander("📘 Learning methods interpretation"):
            st.markdown("""
            <ul style="font-size:0.92rem; padding-left:1rem; margin-top:0.2rem;">
                <li><b>Self-taught</b> methods are the most frequently used.</li>
                <li><b>Formal education</b> (school, university) continues to play an important role, but is not dominant in developer training.</li>
                <li><b>Practical training at work</b> and colleague support indicate a strong component of collaborative and experiential learning.</li>
                <li><b>Bootcamps</b> and informal support (friends, family) are less frequently mentioned, but reflect accessible alternatives to classical options.</li>
                <li>The diversity of responses shows that the learning process in programming is flexible, personalized and often combined from multiple sources.</li>
            </ul>
            """, unsafe_allow_html=True)


    with col2:
        counter = Counter()
        df['LearnCode'].fillna('').apply(lambda x: counter.update([i.strip() for i in x.split(';') if i.strip()]))
        learn_df = pd.DataFrame(counter.items(), columns=["Method", "Count"]).sort_values(by="Count", ascending=False)
        learn_df["Percent"] = round(100 * learn_df["Count"] / learn_df["Count"].sum(), 1)

        chart = alt.Chart(learn_df).mark_bar(color="#F48024").encode(
            y=alt.Y("Method:N", sort="-x", title="Method"),
            x=alt.X("Count:Q", title="Number of selections"),
            tooltip=["Method", "Count", "Percent"]
        ).properties(width=750, height=420).configure_axis(
            labelFont="Inter",
            titleFont="Inter"
        )
        st.altair_chart(chart, use_container_width=True)

    # LearnCodeOnline
    st.markdown("### 🌐 Online sources used for learning")
    col1, col2 = st.columns([0.8, 2.2])

    with col1:
        with st.expander("🌐 Online sources interpretation"):
            st.markdown("""
            <ul style="font-size:0.92rem; padding-left:1rem; margin-top:0.2rem;">
                <li><b>Technical documentation</b> and <b>Stack Overflow</b> are the most used sources, emphasizing the need for quick access to applicable information.</li>
                <li><b>Written tutorial</b> platforms, <b>blogs</b> and <b>educational video</b> (e.g. YouTube, video courses) are preferred for clarity and accessibility.</li>
                <li>Classical sources, such as <b>books</b>, remain relevant, but less frequent compared to interactive formats.</li>
                <li><b>Artificial intelligence</b> is increasingly mentioned as a support resource in the learning process.</li>
                <li>The variety of options indicates a <b>combined approach</b>: most respondents use multiple types of resources in parallel, depending on needs and personal style.</li>
            </ul>
            """, unsafe_allow_html=True)


    with col2:
        counter = Counter()
        df['LearnCodeOnline'].fillna('').apply(lambda x: counter.update([i.strip() for i in x.split(';') if i.strip()]))
        online_df = pd.DataFrame(counter.items(), columns=["Platform", "Count"]).sort_values(by="Count", ascending=False)
        online_df["Percent"] = round(100 * online_df["Count"] / online_df["Count"].sum(), 1)

        chart = alt.Chart(online_df).mark_bar(color="#F48024").encode(
            y=alt.Y("Platform:N", sort="-x", title="Platform"),
            x=alt.X("Count:Q", title="Number of selections"),
            tooltip=["Platform", "Count", "Percent"]
        ).properties(width=750, height=420).configure_axis(
            labelFont="Inter",
            titleFont="Inter"
        )
        st.altair_chart(chart, use_container_width=True)

    # TechDoc
    st.markdown("### 📚 Types of technical documentation used")
    col1, col2 = st.columns([0.8, 2.2])

    with col1:
        with st.expander("📚 Technical documentation interpretation"):
            st.markdown("""
            <ul style="font-size:0.92rem; padding-left:1rem; margin-top:0.2rem;">
                <li><b>API documentation</b> is the most frequently used, confirming its importance in understanding technical functionalities.</li>
                <li>Official guides and traditional publications occupy leading positions, indicating that formal documentation remains essential.</li>
                <li><b>Knowledge bases provided by official vendors</b> and <b>AI search engines</b> are increasingly popular complementary options.</li>
                <li>The <b>diversity of formats</b> is notable – from classic publications to modern AI tools, showing developers' adaptability to new technologies.</li>
                <li>The "Other" category has a small share, suggesting that most respondents rely on standardized and validated sources.</li>
            </ul>
            """, unsafe_allow_html=True)


    with col2:
        counter = Counter()
        df['TechDoc'].fillna('').apply(lambda x: counter.update([i.strip() for i in x.split(';') if i.strip()]))
        techdoc_df = pd.DataFrame(counter.items(), columns=["DocType", "Count"]).sort_values(by="Count", ascending=False)
        techdoc_df["Percent"] = round(100 * techdoc_df["Count"] / techdoc_df["Count"].sum(), 1)

        chart = alt.Chart(techdoc_df).mark_bar(color="#F48024").encode(
            y=alt.Y("DocType:N", sort="-x", title="Documentation type"),
            x=alt.X("Count:Q", title="Number of selections"),
            tooltip=["DocType", "Count", "Percent"]
        ).properties(width=750, height=420).configure_axis(
            labelFont="Inter",
            titleFont="Inter"
        )
        st.altair_chart(chart, use_container_width=True)

# === TAB 4: Professional Profile ===
with tab4:
    st.markdown("### 💼 Main branch of activity (MainBranch)")
    col1, col2 = st.columns([0.8, 2.2])

    with col1:
        with st.expander("💼 Main activity interpretation"):
            st.markdown("""
            <ul style="font-size:0.92rem; padding-left:1rem; margin-top:0.2rem;">
                <li>Most respondents identify as <b>active professionals</b> in software development.</li>
                <li>A significant category is represented by <b>students and those in professional transition</b>.</li>
            </ul>
            """, unsafe_allow_html=True)

    with col2:
        if "MainBranch" in df.columns:
            counts = df["MainBranch"].value_counts().reset_index()
            counts.columns = ["MainBranch", "Count"]
            counts["Percent"] = round(100 * counts["Count"] / counts["Count"].sum(), 1)

            chart = alt.Chart(counts).mark_bar(color="#F48024").encode(
                y=alt.Y("MainBranch:N", sort="-x", title="Main branch"),
                x=alt.X("Count:Q", title="Number of respondents"),
                tooltip=["MainBranch", "Count", "Percent"]
            ).properties(width=750, height=360).configure_axis(
                labelFont="Inter",
                titleFont="Inter"
            )
            st.altair_chart(chart, use_container_width=True)

    st.markdown("### 🏠 Work arrangement (RemoteWork)")
    col1, col2 = st.columns([0.8, 2.2])

    with col1:
        with st.expander("🏠 Work arrangement interpretation"):
            st.markdown("""
            <ul style="font-size:0.92rem; padding-left:1rem; margin-top:0.2rem;">
                <li><b>Remote work</b> is very widespread – many respondents work completely or partially from home.</li>
                <li>Workplace flexibility is important for developers.</li>
            </ul>
            """, unsafe_allow_html=True)

    with col2:
        if "RemoteWork" in df.columns:
            counts = df["RemoteWork"].value_counts().reset_index()
            counts.columns = ["RemoteWork", "Count"]
            counts["Percent"] = round(100 * counts["Count"] / counts["Count"].sum(), 1)

            chart = alt.Chart(counts).mark_bar(color="#F48024").encode(
                y=alt.Y("RemoteWork:N", sort="-x", title="Work arrangement"),
                x=alt.X("Count:Q", title="Number of respondents"),
                tooltip=["RemoteWork", "Count", "Percent"]
            ).properties(width=750, height=360).configure_axis(
                labelFont="Inter",
                titleFont="Inter"
            )
            st.altair_chart(chart, use_container_width=True)

    st.markdown("### 👥 Employment status (Employment)")
    col1, col2 = st.columns([0.8, 2.2])

    with col1:
        with st.expander("👥 Employment status interpretation"):
            st.markdown("""
            <ul style="font-size:0.92rem; padding-left:1rem; margin-top:0.2rem;">
                <li>Respondents can have <b>multiple forms of employment</b>: full-time, freelancing, part-time etc.</li>
                <li>It is a <b>multi-label</b> variable, reflecting diverse realities.</li>
            </ul>
            """, unsafe_allow_html=True)

    with col2:
        counter = Counter()
        df['Employment'].fillna('').apply(lambda x: counter.update([i.strip() for i in x.split(';') if i.strip()]))
        emp_df = pd.DataFrame(counter.items(), columns=["Employment", "Count"]).sort_values(by="Count", ascending=False)
        emp_df["Percent"] = round(100 * emp_df["Count"] / emp_df["Count"].sum(), 1)

        chart = alt.Chart(emp_df).mark_bar(color="#F48024").encode(
            y=alt.Y("Employment:N", sort="-x", title="Employment status"),
            x=alt.X("Count:Q", title="Number of selections"),
            tooltip=["Employment", "Count", "Percent"]
        ).properties(width=750, height=420).configure_axis(
            labelFont="Inter",
            titleFont="Inter"
        )
        st.altair_chart(chart, use_container_width=True)

    st.markdown("### 🧑‍💻 Top 20 developer types (DevType)")
    col1, col2 = st.columns([0.8, 2.2])

    with col1:
        with st.expander("🧑‍💻 DevType roles interpretation"):
            st.markdown("""
            <ul style="font-size:0.92rem; padding-left:1rem; margin-top:0.2rem;">
                <li>The most frequent roles are <b>full-stack</b> and <b>back-end</b>.</li>
                <li>There is great diversity in development activity.</li>
            </ul>
            """, unsafe_allow_html=True)

    with col2:
        counter = Counter()
        df['DevType'].fillna('').apply(lambda x: counter.update([i.strip() for i in x.split(';') if i.strip()]))
        top20 = counter.most_common(20)
        dev_df = pd.DataFrame(top20, columns=["DevType", "Count"])
        dev_df["Percent"] = round(100 * dev_df["Count"] / dev_df["Count"].sum(), 1)

        chart = alt.Chart(dev_df).mark_bar(color="#F48024").encode(
            y=alt.Y("DevType:N", sort="-x", title="Developer type"),
            x=alt.X("Count:Q", title="Number of selections"),
            tooltip=["DevType", "Count", "Percent"]
        ).properties(width=750, height=420).configure_axis(
            labelFont="Inter",
            titleFont="Inter"
        )
        st.altair_chart(chart, use_container_width=True)

    st.markdown("### 🏢 Organization size (OrgSize_grouped)")
    col1, col2 = st.columns([0.8, 2.2])

    with col1:
        with st.expander("🏢 Organization size interpretation"):
            st.markdown("""
            <ul style="font-size:0.92rem; padding-left:1rem; margin-top:0.2rem;">
                <li>Most work in <b>medium or large companies</b>.</li>
                <li>The share of startups is lower.</li>
            </ul>
            """, unsafe_allow_html=True)

    with col2:
        if "OrgSize_grouped" in df.columns:
            data = df[df["OrgSize_grouped"] != "Unknown"]
            counts = data["OrgSize_grouped"].value_counts().reset_index()
            counts.columns = ["OrgSize", "Count"]
            counts["Percent"] = round(100 * counts["Count"] / counts["Count"].sum(), 1)

            chart = alt.Chart(counts).mark_bar(color="#F48024").encode(
                y=alt.Y("OrgSize:N", sort="-x", title="Company size"),
                x=alt.X("Count:Q", title="Number of respondents"),
                tooltip=["OrgSize", "Count", "Percent"]
            ).properties(width=750, height=400).configure_axis(
                labelFont="Inter",
                titleFont="Inter"
            )
            st.altair_chart(chart, use_container_width=True)

    st.markdown("### 🎯 Type of professional responsibility (ICorPM)")
    col1, col2 = st.columns([0.8, 2.2])

    with col1:
        with st.expander("🎯 Professional responsibility interpretation"):
            st.markdown("""
            <ul style="font-size:0.92rem; padding-left:1rem; margin-top:0.2rem;">
                <li>Most respondents are <b>individual contributors</b>.</li>
                <li>Lower percentage of <b>managers</b> and <b>team leads</b>.</li>
            </ul>
            """, unsafe_allow_html=True)

    with col2:
        if "ICorPM" in df.columns:
            data = df[df["ICorPM"] != "Unknown"]
            counts = data["ICorPM"].value_counts().reset_index()
            counts.columns = ["RoleType", "Count"]
            counts["Percent"] = round(100 * counts["Count"] / counts["Count"].sum(), 1)

            chart = alt.Chart(counts).mark_bar(color="#F48024").encode(
                y=alt.Y("RoleType:N", sort="-x", title="Responsibility"),
                x=alt.X("Count:Q", title="Number of respondents"),
                tooltip=["RoleType", "Count", "Percent"]
            ).properties(width=750, height=400).configure_axis(
                labelFont="Inter",
                titleFont="Inter"
            )
            st.altair_chart(chart, use_container_width=True)

    st.markdown("### 💰 Annual income distribution (USD)")

    col1, col2 = st.columns([0.8, 2.2])

    with col1:
        with st.expander("💰 Gross income distribution interpretation"):
            st.markdown("""
            <ul style="font-size:0.92rem; padding-left:1rem; margin-top:0.2rem;">
                <li>The annual income distribution is <b>strongly right-skewed</b>, typical of self-reported financial data.</li>
                <li>Most respondents fall within the <b>$10,000 – $150,000</b> range, with maximum density between <b>$30,000 and $80,000</b>.</li>
            </ul>
            """, unsafe_allow_html=True)

    with col2:
        if "ConvertedCompYearly" in df.columns:
            # Remove NaN and filter on 1–99 percentile
            comp = df["ConvertedCompYearly"].dropna()
            p1, p99 = np.percentile(comp, [1, 99])
            filtered = comp[(comp >= p1) & (comp <= p99)]
            hist_df = pd.DataFrame({"Salary": filtered})

            chart = alt.Chart(hist_df).mark_bar(color="#F48024").encode(
                x=alt.X("Salary:Q", bin=alt.Bin(maxbins=50), title="Annual income (USD)"),
                y=alt.Y("count():Q", title="Number of respondents"),
                tooltip=["count()"]
            ).properties(width=750, height=400).configure_axis(
                labelFont="Inter",
                titleFont="Inter",
                labelFontSize=12,
                titleFontSize=13
            )

            st.altair_chart(chart, use_container_width=True)


# === TAB 5: Professional Experience ===
with tab5:
    st.markdown("### 🧮 Years of coding experience (YearsCode)")

    col1, col2 = st.columns([0.8, 2.2])

    with col1:
        with st.expander("🧮 Coding experience interpretation"):
            st.markdown("""
            <ul style="font-size:0.92rem; padding-left:1rem; margin-top:0.2rem;">
                <li>Most respondents have between <b>1 and 15 years</b> of programming experience.</li>
                <li><b>50% of respondents</b> fall between <b>6 and 20 years</b>, reflecting a <b>great diversity of profiles</b>.</li>
                <li>The presence of <b>positive outliers</b> (up to 50 years) shows the existence of veteran developers in the sample.</li>
                <li>Very small values (0 years) indicate respondents at the beginning of their journey (e.g. students, beginners).</li>
            </ul>
            """, unsafe_allow_html=True)

    with col2:
        if "YearsCode" in df.columns:
            years_df = df["YearsCode"].dropna()

            viz_option = st.radio(
                "Select analysis type:",
                ["Visual representation", "Descriptive statistics"],
                index=0,
                horizontal=True
            )

            if viz_option == "Visual representation":
                chart = alt.Chart(pd.DataFrame({"YearsCode": years_df})).mark_bar(color="#F48024").encode(
                    x=alt.X("YearsCode:Q", bin=alt.Bin(maxbins=40), title="Years of coding experience"),
                    y=alt.Y("count():Q", title="Number of respondents"),
                    tooltip=["count()"]
                ).properties(width=750, height=400).configure_axis(
                    labelFont="Inter",
                    titleFont="Inter",
                    labelFontSize=12,
                    titleFontSize=13
                )

                st.altair_chart(chart, use_container_width=True)

            else:
                desc = years_df.describe().round(2)
                desc_df = pd.DataFrame(desc)
                desc_df.rename(index={
                    "count": "Number of values",
                    "mean": "Mean",
                    "std": "Standard deviation",
                    "min": "Minimum",
                    "25%": "25th percentile",
                    "50%": "Median",
                    "75%": "75th percentile",
                    "max": "Maximum"
                }, inplace=True)

                desc_df = desc_df.rename(columns={0: "YearsCode"}) if 0 in desc_df.columns else desc_df

                # Convert to styled HTML
                styled_html = desc_df.to_html(
                    classes="styled-table",
                    border=0,
                    justify="center"
                )

                st.markdown("""
                <style>
                .styled-table {
                    font-family: 'Inter', serif;
                    border-collapse: collapse;
                    margin: 0.5rem 0;
                    font-size: 1.03rem;
                    width: 100%;
                }
                .styled-table thead tr {
                    background-color: #f4f4f4;
                    text-align: center;
                    font-weight: bold;
                }
                .styled-table th, .styled-table td {
                    border: 1px solid #ddd;
                    padding: 4px 4px;
                    text-align: center;
                }
                .styled-table tbody tr:nth-child(even) {
                    background-color: #fcfcfc;
                }
                </style>
                """, unsafe_allow_html=True)

                st.markdown(styled_html, unsafe_allow_html=True)

        st.markdown("### 🧑‍💼 Total professional experience (WorkExp)")

    col1, col2 = st.columns([0.8, 2.2])

    with col1:
        with st.expander("🧑‍💼 Professional experience interpretation"):
            st.markdown("""
            <ul style="font-size:0.92rem; padding-left:1rem; margin-top:0.2rem;">
                <li>Most respondents have <b>1–15 years</b> of professional experience in IT, with a local peak recorded at 5 years.</li>
                <li><b>The distribution is asymmetric</b>, with a high concentration around small values and a gradual decrease towards extremes.</li>
                <li><b>The median is smaller than the mean</b>, confirming a <b>long right tail</b> in the distribution.</li>
                <li>Values close to 0 indicate <b>juniors or industry newcomers</b>, while extremes (over 30 years) suggest <b>senior specialists</b>.</li>
            </ul>
            """, unsafe_allow_html=True)

    with col2:
        if "WorkExp" in df.columns:
            workexp_df = df["WorkExp"].dropna()

            viz_option = st.radio(
                "Select analysis type:",
                ["Visual representation", "Descriptive statistics"],
                index=0,
                horizontal=True,
                key="workexp_radio"
            )


            if viz_option == "Visual representation":
                chart = alt.Chart(pd.DataFrame({"WorkExp": workexp_df})).mark_bar(color="#F48024").encode(
                    x=alt.X("WorkExp:Q", bin=alt.Bin(maxbins=40), title="Years of professional experience"),
                    y=alt.Y("count():Q", title="Number of respondents"),
                    tooltip=["count()"]
                ).properties(width=750, height=400).configure_axis(
                    labelFont="Inter",
                    titleFont="Inter",
                    labelFontSize=12,
                    titleFontSize=13
                )

                st.altair_chart(chart, use_container_width=True)

            else:
                desc = workexp_df.describe().round(2)
                desc_df = pd.DataFrame(desc)
                desc_df.rename(index={
                    "count": "Number of values",
                    "mean": "Mean",
                    "std": "Standard deviation",
                    "min": "Minimum",
                    "25%": "25th percentile",
                    "50%": "Median",
                    "75%": "75th percentile",
                    "max": "Maximum"
                }, inplace=True)

                desc_df = desc_df.rename(columns={0: "WorkExp"}) if 0 in desc_df.columns else desc_df

                styled_html = desc_df.to_html(
                    classes="styled-table",
                    border=0,
                    justify="center"
                )

                st.markdown("""
                <style>
                .styled-table {
                    font-family: 'Inter', sans-serif;
                    border-collapse: collapse;
                    margin: 0.5rem 0;
                    font-size: 1.03rem;
                    width: 100%;
                }
                .styled-table thead tr {
                    background-color: #f4f4f4;
                    text-align: center;
                    font-weight: bold;
                }
                .styled-table th, .styled-table td {
                    border: 1px solid #ddd;
                    padding: 8px 12px;
                    text-align: center;
                }
                .styled-table tbody tr:nth-child(even) {
                    background-color: #fcfcfc;
                }
                </style>
                """, unsafe_allow_html=True)

                st.markdown(styled_html, unsafe_allow_html=True)

# === TAB 6: Technologies Used ===
with tab6:
    st.markdown("### 🧑‍💻 Top 20 programming languages used (LanguageHaveWorkedWith)")

    col1, col2 = st.columns([0.8, 2.2])

    with col1:
        with st.expander("🧑‍💻 Programming languages interpretation"):
            st.markdown(f"""
            <ul style="font-size:0.92rem; padding-left:1rem; margin-top:0.2rem;">
                <li>The chart displays <b>the most frequently mentioned 20 languages</b>, out of a total of 49 options available in the survey.</li>
                <li><b>JavaScript, HTML/CSS, Python</b> and <b>SQL</b> are the most popular, reflecting the predominance of web development and data analysis.</li>
                <li>Despite the large number of programming languages available in the survey, preferences are significantly concentrated around the first 10-15, reflecting a market concentrated around mature and well community-supported technologies.</li>
            </ul>
            """, unsafe_allow_html=True)

    with col2:
        from collections import Counter

        df_lang = df["LanguageHaveWorkedWith"].fillna("")
        counter = Counter()
        df_lang.apply(lambda x: counter.update([item.strip() for item in str(x).split(';') if item.strip()]))

        total_options = len(counter)
        top_n = 20
        top_items = counter.most_common(top_n)

        lang_df = pd.DataFrame(top_items, columns=["Language", "Count"])
        total = sum(counter.values())
        lang_df["Percent"] = round(100 * lang_df["Count"] / total, 1)

        chart = alt.Chart(lang_df).mark_bar(color="#F48024").encode(
            y=alt.Y("Language:N", sort="-x", title="Programming language", axis=alt.Axis(labelLimit=0, labelOverlap=False)),
            x=alt.X("Count:Q", title="Number of selections (multi-label)"),
            tooltip=["Language", "Count", "Percent"]
        ).properties(
            width=750,
            height=420,
        ).configure_axis(
            labelFont="Inter",
            titleFont="Inter",
            labelFontSize=12,
            titleFontSize=13
        ).configure_title(
            font="Inter",
            fontSize=14,
            anchor="start"
        )

        st.altair_chart(chart, use_container_width=True)

    st.markdown("### 🗄️ Top 20 databases used (DatabaseHaveWorkedWith)")

    col1, col2 = st.columns([0.8, 2.2])

    with col1:
        with st.expander("🗄️ Databases interpretation"):
            st.markdown(f"""
            <ul style="font-size:0.92rem; padding-left:1rem; margin-top:0.2rem;">
                <li>The chart displays <b>the most frequently mentioned 20 databases</b>, among the 35 options available.</li>
                <li>The top is dominated by <b>MySQL, PostgreSQL and SQLite</b>, reflecting the popularity of these solutions in commercial and open-source applications.</li>
            </ul>
            """, unsafe_allow_html=True)

    with col2:
        from collections import Counter

        df_db = df["DatabaseHaveWorkedWith"].fillna("")
        db_counter = Counter()
        df_db.apply(lambda x: db_counter.update([item.strip() for item in str(x).split(';') if item.strip()]))

        total_options = len(db_counter)
        top_n = 20
        db_top_items = db_counter.most_common(top_n)

        db_df = pd.DataFrame(db_top_items, columns=["Database", "Count"])
        total = sum(db_counter.values())
        db_df["Percent"] = round(100 * db_df["Count"] / total, 1)

        chart = alt.Chart(db_df).mark_bar(color="#F48024").encode(
            y=alt.Y("Database:N", sort="-x", title="Database type", axis=alt.Axis(labelLimit=0, labelOverlap=False)),
            x=alt.X("Count:Q", title="Number of selections (multi-label)"),
            tooltip=["Database", "Count", "Percent"]
        ).properties(
            width=750,
            height=420,
        ).configure_axis(
            labelFont="Inter",
            titleFont="Inter"
        ).configure_title(
            font="Inter",
            fontSize=14,
            anchor="start"
        )

        st.altair_chart(chart, use_container_width=True)

            
# === TAB 7: Stack Overflow Usage ===
with tab7:
    st.markdown("### 🌐 Frequency of Stack Overflow visits (SOVisitFreq)")

    col1, col2 = st.columns([0.8, 2.2])

    with col1:
        with st.expander("🌐 Visit frequency interpretation"):
            st.markdown("""
            <ul style="font-size:0.92rem; padding-left:1rem; margin-top:0.2rem;">
                <li>One third of respondents access the platform a few times per week, this being the most frequent category.</li>
                <li>Two other important segments are represented by those who visit the platform daily or almost daily and those who use it a few times per week.</li>
                <li>The percentage of those who rarely use the platform is <b>relatively low</b>, confirming its high popularity among professionals.</li>
            </ul>
            """, unsafe_allow_html=True)

    with col2:
        if "SOVisitFreq" in df.columns:
            visit_df = df["SOVisitFreq"].dropna()
            visit_df = visit_df[visit_df != "Unknown"]
            vc = visit_df.value_counts()
            total = vc.sum()

            bar_df = pd.DataFrame({
                "SOVisitFreq": vc.index,
                "Count": vc.values,
                "Percent": (vc.values / total * 100).round(2)
            })

            chart = alt.Chart(bar_df).mark_bar(color="#F48024").encode(
                x=alt.X("Count:Q", title="Number of respondents"),
                y=alt.Y("SOVisitFreq:N", sort="-x", title="Visit frequency"),
                tooltip=["SOVisitFreq", "Count", "Percent"]
            ).properties(width=750, height=400).configure_axis(
                labelFont="Inter",
                titleFont="Inter",
                labelFontSize=12,
                titleFontSize=13
            )

            st.altair_chart(chart, use_container_width=True)

    st.markdown("### 👤 Having a Stack Overflow account (SOAccount)")

    col1, col2 = st.columns([0.8, 2.2])

    with col1:
        with st.expander("👤 Stack Overflow account interpretation"):
            st.markdown("""
            <ul style="font-size:0.92rem; padding-left:1rem; margin-top:0.2rem;">
                <li>Most respondents <b>have an account</b> on Stack Overflow.</li>
                <li>This highlights <b>growing interest in active community participation</b>, not just passive content consumption.</li>
                <li>The proportion of those without an account is <b>relatively small</b>, but important for understanding the degree of direct involvement.</li>
            </ul>
            """, unsafe_allow_html=True)

    with col2:
        if "SOAccount" in df.columns:
            account_df = df["SOAccount"].dropna()
            account_df = account_df[account_df != "Unknown"]
            vc = account_df.value_counts()
            total = vc.sum()

            bar_df = pd.DataFrame({
                "SOAccount": vc.index,
                "count": vc.values,
                "percent": (vc.values / total * 100).round(2)
            })

            chart = alt.Chart(bar_df).mark_bar(color="#F48024").encode(
                x=alt.X("count:Q", title="count"),
                y=alt.Y("SOAccount:N", sort="-x", title="SOAccount"),
                tooltip=["SOAccount", "count", "percent"]
            ).properties(width=750, height=400).configure_axis(
                labelFont="Inter",
                titleFont="Inter",
                labelFontSize=12,
                titleFontSize=13
            )

            st.altair_chart(chart, use_container_width=True)

    st.markdown("### 💬 Active participation on Stack Overflow (SOPartFreq)")

    col1, col2 = st.columns([0.8, 2.2])

    with col1:
        with st.expander("💬 Active participation interpretation"):
            st.markdown("""
            <ul style="font-size:0.92rem; padding-left:1rem; margin-top:0.2rem;">
                <li>Most respondents <b>rarely participate</b> actively (e.g. posting questions or answers).</li>
                <li>This highlights that <b>platform usage is predominantly passive</b>.</li>
                <li>However, there is also an <b>actively involved minority</b>, which contributes to community dynamics.</li>
            </ul>
            """, unsafe_allow_html=True)

    with col2:
        if "SOPartFreq" in df.columns:
            part_df = df["SOPartFreq"].dropna()
            part_df = part_df[part_df != "Unknown"]
            vc = part_df.value_counts()
            total = vc.sum()

            bar_df = pd.DataFrame({
                "SOPartFreq": vc.index,
                "count": vc.values,
                "percent": (vc.values / total * 100).round(2)
            })

            chart = alt.Chart(bar_df).mark_bar(color="#F48024").encode(
                x=alt.X("count:Q", title="count"),
                y=alt.Y("SOPartFreq:N", sort="-x", title="SOPartFreq"),
                tooltip=["SOPartFreq", "count", "percent"]
            ).properties(width=750, height=400).configure_axis(
                labelFont="Inter",
                titleFont="Inter",
                labelFontSize=12,
                titleFontSize=13
            )

            st.altair_chart(chart, use_container_width=True)

    st.markdown("### 🛠️ How Stack Overflow is used (SOHow)")

    col1, col2 = st.columns([0.8, 2.2])

    with col1:
        with st.expander("🛠️ Usage method interpretation"):
            st.markdown("""
            <ul style="font-size:0.92rem; padding-left:1rem; margin-top:0.2rem;">
                <li>Stack Overflow is primarily used for <b>quickly finding code solutions</b>, confirming the platform's status as a support tool in solving specific problems at an accelerated pace.</li>
                <li>A large proportion of respondents also use it for <b>general learning</b> or <b>project inspiration</b>.</li>
            </ul>
            """, unsafe_allow_html=True)

    with col2:
        if "SOHow" in df.columns:
            from collections import Counter

            sohow_series = df["SOHow"].fillna('')
            counter = Counter()
            sohow_series.apply(lambda x: counter.update([item.strip() for item in str(x).split(';') if item.strip()]))

            labels, values = zip(*counter.most_common())
            total = sum(values)

            bar_df = pd.DataFrame({
                "SOHow": labels,
                "count": values,
                "percent": [round(v / total * 100, 2) for v in values]
            })

            chart = alt.Chart(bar_df).mark_bar(color="#F48024").encode(
                x=alt.X("count:Q", title="count"),
                y=alt.Y("SOHow:N", sort="-x", title="SOHow"),
                tooltip=["SOHow", "count", "percent"]
            ).properties(width=750, height=400).configure_axis(
                labelFont="Inter",
                titleFont="Inter",
                labelFontSize=12,
                titleFontSize=13
            )

            st.altair_chart(chart, use_container_width=True)

    st.markdown("### 👥 Perception of belonging to the Stack Overflow community (SOComm)")

    col1, col2 = st.columns([0.8, 2.2])

    with col1:
        with st.expander("👥 Community perception interpretation"):
            st.markdown("""
            <ul style="font-size:0.92rem; padding-left:1rem; margin-top:0.2rem;">
                <li>Most respondents feel <b>moderately or well integrated</b> into the Stack Overflow community.</li>
                <li>However, there is a <b>significant percentage</b> that does not identify with the community, signaling a <b>potential for improving inclusion</b>.</li>
                <li>The distribution reflects <b>variety in levels of involvement</b> and familiarity with the platform.</li>
            </ul>
            """, unsafe_allow_html=True)

    with col2:
        if "SOComm" in df.columns:
            comm_df = df["SOComm"].dropna()
            comm_df = comm_df[comm_df != "Unknown"]
            vc = comm_df.value_counts()
            total = vc.sum()

            bar_df = pd.DataFrame({
                "SOComm": vc.index,
                "count": vc.values,
                "percent": (vc.values / total * 100).round(2)
            })

            chart = alt.Chart(bar_df).mark_bar(color="#F48024").encode(
                x=alt.X("count:Q", title="count"),
                y=alt.Y("SOComm:N", sort="-x", title="SOComm"),
                tooltip=["SOComm", "count", "percent"]
            ).properties(width=750, height=400).configure_axis(
                labelFont="Inter",
                titleFont="Inter",
                labelFontSize=12,
                titleFontSize=13
            )

            st.altair_chart(chart, use_container_width=True)

