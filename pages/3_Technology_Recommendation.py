# streamlit_app.py

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
from sklearn.preprocessing import OrdinalEncoder, StandardScaler

st.set_page_config(page_title="AI Technology Recommendation", layout="wide", page_icon="🤖")


@st.cache_resource
def load_models():
    """Load all models and data files"""
    try:
        model_info = None
        try:
            with open("models/model_comparison_results.pkl", "rb") as f:
                model_info = pickle.load(f)
        except FileNotFoundError:
            st.sidebar.warning("Model comparison results not found.")
        
        # Load the best model
        with open("models/recomandare_model_best.pkl", "rb") as f:
            model = pickle.load(f)

        with open("models/recomandare_encoder.pkl", "rb") as f:
            encoder = pickle.load(f)
        
        scaler = None
        try:
            with open("models/recomandare_scaler.pkl", "rb") as f:
                scaler = pickle.load(f)
        except FileNotFoundError:
            pass  # Some models don't need scaling

        with open("models/recomandare_input_cols.pkl", "rb") as f:
            input_cols = pickle.load(f)

        with open("models/recomandare_output_cols.pkl", "rb") as f:
            output_cols = pickle.load(f)

        with open("models/recomandare_dropdown_options.pkl", "rb") as f:
            dropdown_options = pickle.load(f)
        
        return model, encoder, scaler, input_cols, output_cols, dropdown_options, model_info
    
    except FileNotFoundError as e:
        st.error(f"Model file not found: {e}")
        st.info("Make sure all .pkl files are in the current directory")
        st.info("Try running the multi_model_trainer.py script first.")
        st.stop()
    except Exception as e:
        st.error(f"Error loading models: {e}")
        st.error("This might be a scikit-learn version compatibility issue.")
        st.info("Solutions:")
        st.info("1. Run: pip install --upgrade scikit-learn")
        st.info("2. Or retrain the model with multi_model_trainer.py")
        st.stop()

model, encoder, scaler, input_cols, output_cols, dropdown_options, model_info = load_models()


st.title("🤖 Technology Recommendation for IT Career")

with st.sidebar:
    st.header("📊 Model Information")
    
    if model_info:
        st.success(f"**🏆 Active model: Neural Network**")
        st.metric("Jaccard Score", f"{model_info['performance']['Jaccard Score']:.4f}")
        st.metric("F1-Micro Score", f"{model_info['performance']['F1 Micro']:.4f}")
        
        # Show model comparison
        with st.expander("🔍 Model comparison"):
            if 'all_results' in model_info:
                results_df = pd.DataFrame(model_info['all_results'])
                results_df = results_df.sort_values('Jaccard Score', ascending=False)
                st.dataframe(
                    results_df[['Model', 'Jaccard Score', 'F1 Micro']].round(4),
                    use_container_width=True
                )
    else:
        st.info("Model information not available")
    
    st.markdown("---")
    st.markdown("**🎯 How it works:**")
    st.markdown("1. Complete your profile")
    st.markdown("2. AI analyzes the data")
    st.markdown("3. Receive personalized recommendations")


st.markdown("---")
st.subheader("📋 Complete your professional profile")

with st.form("input_form"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**👤 Personal data**")
        age = st.slider("Age", 18, 70, 25)
        years_code = st.number_input("Years of programming experience", 0, 50, 2)
        work_exp = st.number_input("Total professional experience (years)", 0, 50, 1)
    
    with col2:
        st.markdown("**🌍 Location and education**")
        region = st.selectbox("Region", dropdown_options["Region"])
        edlevel = st.selectbox("Educational level", dropdown_options["EdLevel"])
    
    with col3:
        st.markdown("**💼 Work preferences**")
        remote = st.selectbox("Work type", dropdown_options["RemoteWork"])
        mainbranch = st.selectbox("Main activity", dropdown_options["MainBranch_simple"])

    st.markdown("**🧑‍💻 Desired professional role**")
    devtype = st.selectbox("Select the role that interests you:", dropdown_options["DevType"])

    submitted = st.form_submit_button("🚀 Generate Recommendation", use_container_width=True)

st.markdown("""
        <style>
        .tech-container {
            background: linear-gradient(135deg, #f48024 0%, #d96d00 100%);
            padding: 20px;
            border-radius: 15px;
            margin: 10px 0;
            box-shadow: 0 8px 32px rgba(244, 128, 36, 0.37);
        }
        .tech-title {
            color: white;
            font-size: 1.2rem;
            font-weight: bold;
            margin-bottom: 15px;
            text-align: center;
        }
        .tech-badge {
            display: inline-block;
            background: rgba(255, 255, 255, 0.9);
            color: #333;
            padding: 8px 16px;
            margin: 4px 6px 4px 0;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 500;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
        }
        .tech-badge:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
        }
        .lang-container {
            background: linear-gradient(135deg, #f48024 0%, #d96d00 100%);
        }
        .ai-container {
            background: linear-gradient(135deg, #f48024 0%, #d96d00 100%);
        }
        .no-recommendations {
            text-align: center;
            color: white;
            font-style: italic;
            padding: 20px;
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
        with st.spinner("🔄 Analyzing your profile and generating recommendations..."):
            input_dict = {
                "Age": age,
                "YearsCode": years_code,
                "WorkExp": work_exp,
                "Region": region,
                "EdLevel": edlevel,
                "RemoteWork": remote,
                "MainBranch_simple": mainbranch,
            }

            for role in dropdown_options["DevType"]:
                col_name = f"DevType_{role.lower().replace(' ', '_').replace('-', '_').replace('(', '').replace(')', '').replace('.', '')}"
                input_dict[col_name] = 1 if role == devtype else 0

            input_df = pd.DataFrame([input_dict])
            
            categorical_cols = ["Region", "EdLevel", "RemoteWork", "MainBranch_simple"]
            input_df[categorical_cols] = encoder.transform(input_df[categorical_cols])
            
            for col in input_cols:
                if col not in input_df.columns:
                    input_df[col] = 0
            
            input_df = input_df[input_cols]
            
            if scaler is not None and model_info and model_info.get('use_scaled', False):
                input_df = pd.DataFrame(
                    scaler.transform(input_df), 
                    columns=input_df.columns, 
                    index=input_df.index
                )

            y_pred = model.predict(input_df)[0]
            predictions = dict(zip(output_cols, y_pred))
            
            languages_with_scores = []
            ai_tools_with_scores = []
            
            try:
                y_proba_list = model.predict_proba(input_df)
                
                for i, (col, pred) in enumerate(predictions.items()):
                    if pred == 1:  
                        score = 0.5  
                        try:
                            if i < len(y_proba_list):
                                proba_array = y_proba_list[i][0]  
                                if len(proba_array) > 1:
                                    score = proba_array[1]  
                                else:
                                    score = proba_array[0] if proba_array[0] > 0.5 else 1 - proba_array[0]
                        except (IndexError, TypeError):
                            score = 0.7  
                        
                        clean_name = col.replace("Language_", "").replace("AISearchDevHave_", "").replace("_", " ").title()
                        
                        if col.startswith("Language_"):
                            languages_with_scores.append((clean_name, score))
                        elif col.startswith("AISearchDevHave_"):
                            ai_tools_with_scores.append((clean_name, score))
            
            except AttributeError:
                for col, pred in predictions.items():
                    if pred == 1:
                        base_score = 0.6
                        if any(tech in col.lower() for tech in ['python', 'javascript', 'sql', 'html', 'css']):
                            score = base_score + 0.2
                        else:
                            score = base_score
                        
                        clean_name = col.replace("Language_", "").replace("AISearchDevHave_", "").replace("_", " ").title()
                        
                        if col.startswith("Language_"):
                            languages_with_scores.append((clean_name, score))
                        elif col.startswith("AISearchDevHave_"):
                            ai_tools_with_scores.append((clean_name, score))
            
            languages_with_scores.sort(key=lambda x: x[1], reverse=True)
            ai_tools_with_scores.sort(key=lambda x: x[1], reverse=True)
            
            languages = [name for name, score in languages_with_scores]
            ai_tools = [name for name, score in ai_tools_with_scores]

            def normalize_tech_names(lst):
                """Clean and normalize technology names"""
                cleaned = set()
                replacements = {
                    'Javascript': 'JavaScript',
                    'Typescript': 'TypeScript',
                    'Nodejs': 'Node.js',
                    'Reactjs': 'React.js',
                    'Vuejs': 'Vue.js',
                    'Angularjs': 'Angular.js',
                    'Mysql': 'MySQL',
                    'Postgresql': 'PostgreSQL',
                    'Mongodb': 'MongoDB',
                    'Redis': 'Redis',
                    'Html Css': 'HTML/CSS',
                    'Assembly': 'Assembly',
                    'Bash Shell': 'Bash/Shell',
                    'Powershell': 'PowerShell'
                }
                
                for item in lst:
                    clean_item = item.replace("/", " ").replace("_", " ").strip()
                    
                    for old, new in replacements.items():
                        if old.lower() in clean_item.lower():
                            clean_item = new
                            break
                    
                    cleaned.add(clean_item)
                
                return sorted(list(cleaned))

            norm_lang = normalize_tech_names(languages)
            norm_ai = normalize_tech_names(ai_tools)

   
        st.markdown("---")
        st.success("✅ Recommendation generated successfully!")
        
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.markdown(f"### 🎯 Recommendations for: **{devtype}**")
        with col2:
            st.metric("🔧 Technologies", len(norm_lang))
        with col3:
            st.metric("🤖 AI Tools", len(norm_ai))

        col1, col2 = st.columns(2)

        with col1:
            container_class = "tech-container lang-container"
            if norm_lang:
                badges = "".join([f"<span class='tech-badge'>{lang}</span>" for lang in norm_lang])
                st.markdown(f"""
                <div class='{container_class}'>
                    <div class='tech-title'>💻 Programming Languages</div>
                    {badges}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='{container_class}'>
                    <div class='tech-title'>💻 Programming Languages</div>
                    <div class='no-recommendations'>No specific language recommended</div>
                </div>
                """, unsafe_allow_html=True)

        with col2:
            container_class = "tech-container ai-container"
            if norm_ai:
                badges = "".join([f"<span class='tech-badge'>{tool}</span>" for tool in norm_ai])
                st.markdown(f"""
                <div class='{container_class}'>
                    <div class='tech-title'>🤖 AI & Development Tools</div>
                    {badges}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='{container_class}'>
                    <div class='tech-title'>🤖 AI & Development Tools</div>
                    <div class='no-recommendations'>No specific tool recommended</div>
                </div>
                """, unsafe_allow_html=True)

        if norm_lang or norm_ai:
            st.markdown("---")
            
            with st.expander("🎓 Learning suggestions", expanded=True):
                st.markdown("**📚 Recommended learning plan (in AI priority order):**")
                
                if languages_with_scores:
                    st.markdown("**🎯 Programming languages - ordered by relevance to your profile:**")
                    for i, (lang, score) in enumerate(languages_with_scores[:5], 1):
                        confidence_emoji = "🔥" if score > 0.75 else "⭐" if score > 0.65 else "✨"
                        st.markdown(f"{i}. {confidence_emoji} **{lang}** - Relevance: {score:.1%}")
                
                if ai_tools_with_scores:
                    st.markdown("**🤖 AI and development tools - ordered by importance:**")
                    for i, (tool, score) in enumerate(ai_tools_with_scores[:5], 1):
                        confidence_emoji = "🔥" if score > 0.75 else "⭐" if score > 0.65 else "✨"
                        st.markdown(f"{i}. {confidence_emoji} **{tool}** - Relevance: {score:.1%}")
                
                if any(score != 0.5 and score != 0.6 and score != 0.7 and score != 0.8 for _, score in languages_with_scores + ai_tools_with_scores):
                    st.info("💡 **Prioritization explanation:** The order is based on probabilities calculated by the Machine Learning model for your specific profile.")
                else:
                    st.info("💡 **Prioritization explanation:** The order is based on ML model analysis and technology popularity for your role.")

    except KeyError as e:
        st.error(f"❌ Error processing data: Column {e} not found in model.")
        st.info("Check if the model was trained correctly with all necessary columns.")
    except Exception as e:
        st.error(f"❌ Error generating recommendations: {e}")
        st.info("Please try again or contact the administrator.")

st.markdown("---")
col1 = st.columns(1)
st.info(f"🤖 Model: Neural Network")

st.markdown("""
    <div class="so-footer">
    <hr>
    © 2025 Elena-Luiza JALEA · Stack Overflow Survey Thesis · Streamlit powered
            <br>
    <img src="https://upload.wikimedia.org/wikipedia/ro/a/a3/Logo_ASE.png?20140313161351" height="100" style="margin-bottom: -5px; opacity:0.92;" title="Bucharest University of Economic Studies"/>
    </br>
            </div>
""", unsafe_allow_html=True)