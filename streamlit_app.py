# Library imports
import streamlit as st
import plotly.express as px
import pandas as pd

# File imports
dim_user = pd.read_pickle("./data/dim_user.pkl")
dim_product = pd.read_pickle("./data/dim_product.pkl")
fact_order = pd.read_pickle("./data/fact_order.pkl")
sql_df1 = pd.read_pickle("./data/sql_df1.pkl")
sql_df2 = pd.read_pickle("./data/sql_df2.pkl")

# Streamlit app title
st.title("Sales insights")

# Answers to the questions
st.header("Answers to the questions")

# Q1
st.subheader("1. Which user spent the most money on products on all Fridays?")
st.dataframe(sql_df1)
# A1
st.write(
    "The user with maximum Friday spend is **User E from Melbourne** with a total spend of **~$874k**."
)

# Q2
st.subheader(
    "2. What are the best 3 products in each location of a user based on quantity?"
)
st.dataframe(sql_df2, height=35 * len(sql_df2) + 38, width=500)
# A2
st.write(
    "Above output captures top 3 best products per user city location based on purchased quantity."
)

# Charts
st.header("Visualizations")

# Chart 1: Total sales over time
date_grouped_df = fact_order.groupby("order_created")["order_total"].sum().reset_index()

fig1 = px.line(
    date_grouped_df.iloc[1:-1],
    x="order_created",
    y="order_total",
    title="SalesTrend Over Time",
)
st.plotly_chart(fig1, use_container_width=True)

# Adding columns for two charts
col1, col2 = st.columns(2)

# Chart 2: Top Spenders
with col1:
    user_grouped_df = (
        fact_order.merge(dim_user, on="user_id")
        .groupby("user_name")["order_total"]
        .sum()
        .reset_index()
        .sort_values("order_total", ascending=False)
        .head()
    )

    fig2 = px.bar(
        user_grouped_df,
        y="user_name",
        x="order_total",
        title="Top Sales By User",
        orientation="h",
        width=1000,
    ).update_yaxes(type="category", categoryorder="max ascending")
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    user_city_sales = (
        fact_order.merge(dim_user, on="user_id")
        .groupby("user_city")["order_total"]
        .sum()
        .reset_index()
    )

    fig3 = px.pie(
        user_city_sales,
        values="order_total",
        names="user_city",
        title="Total Sales By City",
    )
    st.plotly_chart(fig3, use_container_width=True)
