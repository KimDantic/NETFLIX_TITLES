# streamlit_app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import calendar

# Page config
st.set_page_config(page_title="Netflix Titles Analysis", layout="wide")
st.title("📺 Netflix Titles Data Analysis")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv('netflix_titles.csv')
    df = df.dropna(subset=['show_id', 'type'])
    df['country'].fillna("Unknown", inplace=True)
    df['cast'].fillna("Not Available", inplace=True)
    df['director'].fillna("Not Available", inplace=True)
    df['date_added'].fillna("Unknown", inplace=True)
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    df = df.drop_duplicates()
    df['year_added'] = df['date_added'].dt.year
    df['month_added'] = df['date_added'].dt.month
    return df

df = load_data()

# Show raw data
if st.checkbox("Show Raw Data"):
    st.dataframe(df)

# Top 10 Countries by Number of Titles
st.subheader("🌍 Top 10 Countries by Number of Titles")
top_countries = df['country'].value_counts().head(10)
fig, ax = plt.subplots()
top_countries.plot(kind='bar', color='tomato', ax=ax)
ax.set_ylabel("Count")
st.pyplot(fig)

# Titles Added per Year
st.subheader("📅 Netflix Titles Added Per Year")
titles_per_year = df['year_added'].value_counts().sort_index()
fig, ax = plt.subplots()
titles_per_year.plot(kind='line', marker='o', ax=ax)
ax.set_xlabel("Year")
ax.set_ylabel("Number of Titles")
ax.grid(True)
st.pyplot(fig)

# Boxplot of Release Year by Type
st.subheader("🎬 Boxplot: Release Year by Type (Movie/TV Show)")
fig, ax = plt.subplots()
sns.boxplot(data=df, x='type', y='release_year', ax=ax)
st.pyplot(fig)

# Scatter Plot: Release Year vs Show ID
st.subheader("📊 Scatter Plot: Release Year vs Show ID")
fig, ax = plt.subplots()
sns.scatterplot(data=df, x='release_year', y='show_id', ax=ax)
st.pyplot(fig)

# Histogram: Distribution of Release Year
st.subheader("📈 Distribution of Release Years")
fig, ax = plt.subplots()
sns.histplot(df['release_year'], kde=True, ax=ax)
st.pyplot(fig)

# Genre Distribution
st.subheader("🎭 Genre Distribution")
genre_counts = df['listed_in'].str.split(', ').explode().value_counts().head(20)
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=genre_counts.values, y=genre_counts.index, ax=ax)
ax.set_xlabel('Count')
ax.set_ylabel('Genre')
st.pyplot(fig)

# Monthly Additions
st.subheader("🗓️ Netflix Additions by Month")
monthly_trend = df['month_added'].value_counts().sort_index()
month_names = list(calendar.month_name[1:])
fig, ax = plt.subplots()
monthly_trend.plot(kind='bar', color='purple', ax=ax)
ax.set_xlabel("Month")
ax.set_ylabel("Number of Titles Added")
plt.xticks(range(0, 12), month_names, rotation=45)
st.pyplot(fig)
