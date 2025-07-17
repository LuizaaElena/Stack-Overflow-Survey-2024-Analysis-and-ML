# 💡 Stack Overflow Developer Survey 2024 – Interactive Analysis & ML Predictions

![Python](https://img.shields.io/badge/Python-3.10-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.25-orange)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Last Commit](https://img.shields.io/github/last-commit/your-username/your-repo-name)


This Streamlit application offers an interactive, visual, and intelligent exploration of the **Stack Overflow Developer Survey 2024** dataset.  
Built as part of a master’s dissertation project, it integrates data analysis and machine learning to extract insights, estimate salaries, and provide career technology recommendations.

---

## 📸 Preview

![Home Page Screenshot](images/Home-page.png)

---

## 🚀 Features

### 📊 Descriptive Analysis

Explore key dimensions such as:
- Demographics (age, country)
- Education and learning methods
- Professional roles and experience
- Technologies used (languages, databases, AI tools)
- Stack Overflow usage patterns
- Job satisfaction and attitudes toward AI

### 💰 Salary Prediction

Estimate your gross annual salary based on:
- Age group, education level, region
- Programming experience & work experience
- Preferred developer role
- Known programming languages

> Uses a trained **CatBoost Regressor** model with real survey data.

### 🤖 Technology Recommendation
###
Receive personalized suggestions of:
- Programming languages
- AI tools 

> Based on your profile and desired professional role. Uses a **multi-label classifier** 

---

## 🛠️ How to Run Locally

### 1. Clone this repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```
### 2. Install required packages

Install all dependencies listed in requirements.txt:
```bash
pip install -r requirements.txt
```

### 3. Launch the Streamlit app

Run the application with: 
```bash
streamlit run Home.py
```

## 📁 Project Structure

├── data/
│   └── variabile_preprocesate.csv         ← Preprocessed survey dataset
├── images/
│   └── Home-page.png                       ← Screenshot used in README
├── models/
│   └── *.pkl                               ← Trained ML models & encoders
├── pages/
│   ├── 1_Descriptive_Analysis.py
│   ├── 2_Salary_Prediction.py
│   └── 3_Technology_Recommendation.py
├── Home.py                                 ← Entry point
├── requirements.txt
├── .gitignore
└── README.md

## 📌 Notes

- All models are trained using the Stack Overflow Survey 2024 dataset.
- The project does not use a database — all data comes from CSV files.
- All computations are done locally.
- Streamlit Cloud can also be used for free deployment.

## 👩🏻‍🎓 Author
Elena-Luiza JALEA
Master’s Dissertation, 2025
Database Support for Business – University of Economic Studies, Bucharest

## 📜 License
This project is for educational and non-commercial purposes.
Original data from: Stack Overflow Survey