import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Saudi Burger & Fried Chicken Dashboard", layout="wide")
st.title("Dashboard: Top Burger & Fried Chicken Restaurants in Saudi Arabia")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("arab_burger_data.csv")
    
    # Rename columns to English
    df = df.rename(columns={
        "سلسلة": "Restaurant",
        "المدينة": "City",
        "عدد الفروع": "Branches",
        "الإيرادات (مليون ريال)": "Revenue",
        "متوسط الإيرادات لكل فرع": "Avg_Revenue_per_Branch",
        "نسبة النمو (%)": "Growth"
    })
    
    # Add Category
    burger_only = ["Burgerizzr", "Johnny Rockets", "Five Guys", "Salt", "Section-B", "Fatburger"]
    chicken_only = ["Al Baik", "KyoChon", "Raising Cane's", "Texas Chicken"]
    both = ["Herfy", "Kudu", "McDonald's", "Burger King", "Hardee's", "KFC"]

    def classify(restaurant):
        if restaurant in burger_only:
            return "Burger"
        elif restaurant in chicken_only:
            return "Chicken"
        elif restaurant in both:
            return "Both"
        else:
            return "Other"

    df["Category"] = df["Restaurant"].apply(classify)
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
category_filter = st.sidebar.multiselect(
    "Select Category:",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

city_filter = st.sidebar.multiselect(
    "Select City:",
    options=df["City"].unique(),
    default=df["City"].unique()
)

filtered_df = df[(df["Category"].isin(category_filter)) & (df["City"].isin(city_filter))]

# Total Revenue by Restaurant
st.subheader("Total Revenue by Restaurant")
revenue_by_restaurant = filtered_df.groupby("Restaurant")["Revenue"].sum().reset_index()
fig1 = px.bar(revenue_by_restaurant.sort_values(by="Revenue"), 
              x="Revenue", y="Restaurant", orientation='h',
              labels={"Revenue": "Revenue (Million SAR)", "Restaurant": "Restaurant"},
              color_discrete_sequence=["orange"])
st.plotly_chart(fig1, use_container_width=True)

# Average Revenue per Branch by Restaurant
st.subheader("Average Revenue per Branch by Restaurant")
avg_rev_branch = filtered_df.groupby("Restaurant")["Avg_Revenue_per_Branch"].mean().reset_index()
fig2 = px.bar(avg_rev_branch.sort_values(by="Avg_Revenue_per_Branch"), 
              x="Avg_Revenue_per_Branch", y="Restaurant", orientation='h',
              labels={"Avg_Revenue_per_Branch": "Avg Revenue per Branch (Million SAR)", "Restaurant": "Restaurant"},
              color_discrete_sequence=["green"])
st.plotly_chart(fig2, use_container_width=True)

# Revenue distribution by Category
st.subheader("Revenue Distribution by Category")
revenue_by_category = filtered_df.groupby("Category")["Revenue"].sum().reset_index()
fig3 = px.pie(revenue_by_category, values='Revenue', names='Category', 
              title='Revenue Distribution by Category')
st.plotly_chart(fig3, use_container_width=True)
