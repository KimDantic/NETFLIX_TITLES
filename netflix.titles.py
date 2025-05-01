# streamlit_app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import calendar

# Config
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

# Sidebar
st.sidebar.title("Navigation")
selected_option = st.sidebar.radio(
    "Choose Analysis",
    [
        "Show Raw Data",
        "Top Countries",
        "Titles Per Year",
        "Boxplot by Type",
        "Scatter Plot",
        "Release Year Distribution",
        "Genre Distribution",
        "Monthly Additions",
        "Top Directors",
        "Most Frequent Cast Members",
        "Content Duration (Movies)"
    ]
)

# Display selected visualization
if selected_option == "Show Raw Data":
    st.subheader("📄 Raw Netflix Dataset")
    st.dataframe(df)

elif selected_option == "Top Countries":
    st.subheader("🌍 Top 10 Countries by Number of Titles")
    top_countries = df['country'].value_counts().head(10)
    fig, ax = plt.subplots()
    top_countries.plot(kind='bar', color='tomato', ax=ax)
    ax.set_ylabel("Count")
    st.pyplot(fig)

elif selected_option == "Titles Per Year":
    st.subheader("📅 Titles Added Per Year")
    titles_per_year = df['year_added'].value_counts().sort_index()
    fig, ax = plt.subplots()
    titles_per_year.plot(kind='line', marker='o', ax=ax)
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Titles")
    ax.grid(True)
    st.pyplot(fig)

elif selected_option == "Boxplot by Type":
    st.subheader("🎬 Boxplot: Release Year by Type")
    fig, ax = plt.subplots()
    sns.boxplot(data=df, x='type', y='release_year', ax=ax)
    st.pyplot(fig)

elif selected_option == "Scatter Plot":
    st.subheader("📊 Scatter Plot: Release Year vs Show ID")
    fig, ax = plt.subplots()
    sns.scatterplot(data=df, x='release_year', y='show_id', ax=ax)
    st.pyplot(fig)

elif selected_option == "Release Year Distribution":
    st.subheader("📈 Distribution of Release Years")
    fig, ax = plt.subplots()
    sns.histplot(df['release_year'], kde=True, ax=ax)
    st.pyplot(fig)

elif selected_option == "Genre Distribution":
    st.subheader("🎭 Genre Distribution")
    genre_counts = df['listed_in'].str.split(', ').explode().value_counts().head(20)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=genre_counts.values, y=genre_counts.index, ax=ax)
    ax.set_xlabel('Count')
    ax.set_ylabel('Genre')
    st.pyplot(fig)

elif selected_option == "Monthly Additions":
    st.subheader("🗓️ Additions by Month")
    monthly_trend = df['month_added'].value_counts().sort_index()
    month_names = list(calendar.month_name[1:])
    fig, ax = plt.subplots()
    monthly_trend.plot(kind='bar', color='purple', ax=ax)
    ax.set_xlabel("Month")
    ax.set_ylabel("Number of Titles Added")
    plt.xticks(range(0, 12), month_names, rotation=45)
    st.pyplot(fig)

elif selected_option == "Top Directors":
    st.subheader("🎬 Top 10 Most Frequent Directors")
    top_directors = df['director'].value_counts().head(10)
    fig, ax = plt.subplots()
    top_directors.plot(kind='barh', color='green', ax=ax)
    ax.set_xlabel("Count")
    st.pyplot(fig)

elif selected_option == "Most Frequent Cast Members":
    st.subheader("⭐ Top 10 Cast Members")
    cast_counts = df['cast'].str.split(', ').explode().value_counts().head(10)
    fig, ax = plt.subplots()
    sns.barplot(x=cast_counts.values, y=cast_counts.index, ax=ax, palette='magma')
    ax.set_xlabel("Appearances")
    ax.set_ylabel("Actor/Actress")
    st.pyplot(fig)

elif selected_option == "Content Duration (Movies)":
    st.subheader("⏱️ Movie Duration Distribution")
    movie_df = df[df['type'] == 'Movie'].copy()
    movie_df['duration'] = movie_df['duration'].str.extract('(\d+)').astype(float)
    fig, ax = plt.subplots()
    sns.histplot(movie_df['duration'].dropna(), bins=30, kde=True, ax=ax)
    ax.set_xlabel("Duration (minutes)")
    ax.set_ylabel("Number of Movies")
    st.pyplot(fig)
