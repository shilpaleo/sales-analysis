# Library imports
import streamlit as st
import plotly.express as px
import pandas as pd

# File imports
dim_user = pd.read_pickle('./data/dim_user.pkl')
dim_product = pd.read_pickle('./data/dim_product.pkl')
fact_order = pd.read_pickle('./data/fact_order.pkl')

# Streamlit app title
st.title('Sales insights dashboard')

# Streamlit app charts
# Chart 1: Total sales over time
date_grouped_df = fact_order.groupby("order_created")["order_total"].sum().reset_index()

fig1 = px.line(
    date_grouped_df.iloc[1:-1],
    x="order_created",
    y="order_total",
    title="Total Sales Over Time",
)
st.plotly_chart(fig1, use_container_width=True)

# Chart 2: Total basket size over time
date_grouped_basket_df = fact_order.groupby("order_created")["basket_size"].sum().reset_index()

fig2 = px.line(
    date_grouped_basket_df.iloc[1:-1],
    x="order_created",
    y="basket_size",
    title="Basket size Over Time",
)
st.plotly_chart(fig2, use_container_width=True)

# Adding columns for two charts
col1, col2 = st.columns(2)

# Chart 3: Total sales by User
with col1:
    user_grouped_df = (
        fact_order.groupby("user_id")["order_total"].sum().reset_index()
        .sort_values("order_total", ascending=False)
        .head()
    )

    fig3 = px.bar(
        user_grouped_df,
        y="user_id",
        x="order_total",
        title="Total Sales By User",
        orientation='h',
    ).update_yaxes(type='category', categoryorder='max ascending')
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    user_city_sales = (
    fact_order.merge(dim_user, on="user_id")
    .groupby("user_city")["order_total"].sum().reset_index()
    )

    fig4 = px.pie(
        user_city_sales,
        values="order_total",
        names="user_city",
        title="Total Sales By City",
    )
    st.plotly_chart(fig4, use_container_width=True)    