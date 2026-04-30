import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Admin Dashboard")

# � Login Check
if "logged_in" not in st.session_state:
    st.warning("Please login first")
    st.stop()

# Load data
conn = sqlite3.connect("data_v3.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    enumerator_name TEXT,
    enumerator_phone TEXT,
    district TEXT,
    block TEXT,
    clf_name TEXT,
    survey_date TEXT,
    pre_support_business TEXT,
    pre_revenue REAL,
    reap_support TEXT,
    govt_support TEXT,
    revenue_table TEXT,
    cost_table TEXT,
    staff_salary REAL,
    latest_revenue REAL,
    section_j TEXT,
    section_k TEXT,
    total_revenue REAL,
    total_cost REAL,
    sustainability TEXT
)
""")

conn.commit()

df = pd.read_sql("SELECT * FROM responses", conn)
if df.empty:
    st.warning("No data available yet. Please submit survey first.")
    st.stop()

if df.empty:
    st.info("No survey responses yet.")
    st.stop()

# -------------------
# FILTERS
# -------------------
st.sidebar.header("Filters")

districts = ["All"] + sorted(df["district"].dropna().unique())
selected_district = st.sidebar.selectbox("District", districts)

enumerators = ["All"] + sorted(df["enumerator_name"].dropna().unique())
selected_enum = st.sidebar.selectbox("Enumerator", enumerators)

filtered_df = df.copy()

if selected_district != "All":
    filtered_df = filtered_df[filtered_df["district"] == selected_district]

if selected_enum != "All":
    filtered_df = filtered_df[filtered_df["enumerator_name"] == selected_enum]

# -------------------
# SUMMARY METRICS
# -------------------
st.subheader("Summary")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Surveys", len(filtered_df))
col2.metric("Districts Covered", filtered_df["district"].nunique())
col3.metric("Enumerators", filtered_df["enumerator_name"].nunique())
col4.metric(
    "Sustainable CLFs",
    (filtered_df["sustainability"] == "Sustainable").sum()

)

st.divider()

# -------------------
# CHARTS
# -------------------
col1, col2 = st.columns(2)

# Sustainability Chart
with col1:
    st.subheader("Sustainability Status")

    status_counts = filtered_df["sustainability"].value_counts()

    fig = plt.figure()
    plt.pie(status_counts, labels=status_counts.index, autopct="%1.1f%%")
    st.pyplot(fig)

# Surveys by District
with col2:
    st.subheader("Surveys by District")

    district_counts = filtered_df["district"].value_counts()

    fig2 = plt.figure()
    plt.bar(district_counts.index, district_counts.values)
    plt.xticks(rotation=45)
    st.pyplot(fig2)

st.divider()

# Enumerator performance
st.subheader("Surveys by Enumerator")

enum_counts = filtered_df["enumerator_name"].value_counts()

fig3 = plt.figure()
plt.bar(enum_counts.index, enum_counts.values)
plt.xticks(rotation=45)
st.pyplot(fig3)

st.divider()

# -------------------
# DATA TABLE
# -------------------
st.subheader("Survey Records")

st.dataframe(filtered_df, use_container_width=True)

# -------------------

# DOWNLOAD
# -------------------
st.download_button(
    "Download Filtered Data (Excel)",
    filtered_df.to_csv(index=False),
    "survey_data.csv",
    mime="text/csv"
)
