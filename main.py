import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Set page config
st.set_page_config(page_title="Indonesia Tourism Destination", layout="wide")

# Helper functions
@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path)
    data.drop_duplicates(inplace=True)
    data.dropna(inplace=True)
    return data

def top_n_tourism(x, y, n=10):
    merged_data = pd.merge(x, y, on='Place_Id', how='inner')

    # Calculate total destinations visited and average rating
    total_destinations_visited = merged_data['Place_Id'].nunique()
    average_rating = merged_data['Place_Ratings'].mean()

    # Get the top 10 most visited destinations
    top_10_destinations = (
        merged_data.groupby('Place_Name')
            .size()
            .reset_index(name='Visit_Count')
            .sort_values(by='Visit_Count', ascending=False)
            .head(n)
        )
    
    return total_destinations_visited, average_rating, top_10_destinations

# Load cleaned data
tourism_rating = load_data('cleaned_data/tourism_rating_clean.csv')
tourism_with_id = load_data('cleaned_data/tourism_with_id_clean.csv')
user = load_data('cleaned_data/user_clean.csv')

col = st.columns((4.5, 2), gap='medium')

with col[0]:
    st.markdown("## Most Visited City")
    most_visited_province = tourism_with_id['City'].value_counts().reset_index()
    most_visited_province.columns = ['City', 'Visit_Count']
    fig = px.bar(most_visited_province, x='Visit_Count', y='City', title='Most Visited City', color='City', orientation='h')
    st.plotly_chart(fig)

with col[1]:
    st.markdown("## Top Tourism Destination")
    top_n = st.selectbox("Select Top N", [5, 10, 15, 20])
    results = top_n_tourism(tourism_rating, tourism_with_id, n=int(top_n))
    total_destinations_visited, average_rating, top_10_destinations = results
    st.dataframe(top_10_destinations,
                 column_order=['Place_Name', 'Visit_Count'],
                 hide_index=True,
                 column_config={
                        'Place_Name': st.column_config.TextColumn(
                            "Places"
                        ),
                        'Visit_Count': st.column_config.ProgressColumn(
                            "Visit Count",
                            format="%f",
                            min_value=0,
                            max_value=top_10_destinations['Visit_Count'].max()
                        )
                 })
    
col = st.columns((3.5, 1.5, 1.5), gap='medium')

with col[0]:
    st.markdown("### Age Distribution")
    age_counts = user['Age'].value_counts().reset_index()
    age_counts.columns = ['Age', 'Count']
    fig = px.bar(age_counts, x='Age', y='Count', title='Group Age Distribution', color='Age')
    st.plotly_chart(fig)

with col[1]:
    st.markdown("### Age Group Distribution")
    group_age_counts = user['Age_group'].value_counts().reset_index()
    group_age_counts.columns = ['Age Group', 'Count']
    fig = px.bar(group_age_counts, x='Age Group', y='Count', title='Age Group Distribution', color='Age Group')
    st.plotly_chart(fig)

with col[2]:
    st.markdown("### Category Distribution")
    category_counts = tourism_with_id['Category'].value_counts().reset_index()
    category_counts.columns = ['Category', 'Count']
    fig = px.pie(category_counts, values='Count', names='Category', title='Category Distribution')
    st.plotly_chart(fig)

st.markdown("# EDA Dashboard")

st.markdown("## Why Yogyakarta is the Most Visited City?")

col = st.columns((1, 1, 1), gap='medium')

with col[0]:
    price_comparison = tourism_with_id.groupby('City')['Price'].mean().reset_index()
    price_comparison.columns = ['City', 'Average Price']
    price_comparison = price_comparison.sort_values(by='Average Price', ascending=False)
    fig = px.bar(price_comparison, x='City', y='Average Price', title='Average Price Comparison', color='City')
    st.plotly_chart(fig)

with col[1]:
    rating_comparison = tourism_with_id.groupby('City')['Rating'].mean().reset_index()
    rating_comparison.columns = ['City', 'Average Rating']
    rating_comparison = rating_comparison.sort_values(by='Average Rating', ascending=False)
    fig = px.bar(rating_comparison, y='City', x='Average Rating', orientation='h', title='Average Rating Comparison', color='City')
    st.plotly_chart(fig)

with col[2]:
    free_places = tourism_with_id.groupby('City')['Place_Status'].value_counts().unstack().reset_index()
    free_places.columns = ['City'] + list(free_places.columns[1:])
    free_places = free_places.sort_values(by=free_places.columns[1], ascending=False)
    fig = px.bar(free_places, x='City', y=free_places.columns[1], title='Free Places Comparison', color='City')
    st.plotly_chart(fig)

st.markdown("## Yogyakarta shows a relatively low figure in the previous chart, so why is it still one of the most visited cities?")

col = st.columns((1, 1), gap='medium')

with col[0]:
    top_visited_category = tourism_with_id['Category'].value_counts().reset_index()
    top_visited_category.columns = ['Category', 'Visit_Count']
    fig = px.pie(top_visited_category, values='Visit_Count', names='Category', title='Top Visited Category')
    st.plotly_chart(fig)

with col[1]:
    yogyakarta_categories = tourism_with_id[tourism_with_id['City'] == 'Yogyakarta']['Category'].value_counts().reset_index()
    yogyakarta_categories.columns = ['Category', 'Count']
    fig = px.bar(yogyakarta_categories, x='Category', y='Count', title='Yogyakarta Categories', color='Category')
    st.plotly_chart(fig)

st.markdown("We can see that Yogyakarta offers a variety of attractions that draw tourists, such as Taman Hiburan, Bahari, and Budaya, while keeping entry fees affordable. This variety makes Yogyakarta a popular destination for tourists.")