import streamlit as st
import pandas as pd
import plotly.express as px
from data import generate_sales_data

# Page config
st.set_page_config(page_title="Sales Dashboard", layout="wide", page_icon="📊")

# Load data
df = generate_sales_data()

# Title
st.title("📊 Sales Analytics Dashboard")
st.markdown("Interactive sales insights — filter by region, category, and date.")
st.divider()

# Sidebar filters
st.sidebar.header("🔍 Filters")

regions = ["All"] + sorted(df["region"].unique().tolist())
selected_region = st.sidebar.selectbox("Region", regions)

categories = ["All"] + sorted(df["category"].unique().tolist())
selected_category = st.sidebar.multiselect("Category", categories[1:], default=categories[1:])

min_date = df["date"].min().date()
max_date = df["date"].max().date()
date_range = st.sidebar.date_input("Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)

# Apply filters
filtered = df.copy()
if selected_region != "All":
    filtered = filtered[filtered["region"] == selected_region]
if selected_category:
    filtered = filtered[filtered["category"].isin(selected_category)]
if len(date_range) == 2:
    filtered = filtered[(filtered["date"].dt.date >= date_range[0]) & (filtered["date"].dt.date <= date_range[1])]

# KPI Cards
st.subheader("Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Total Revenue", f"₹{filtered['revenue'].sum():,.0f}")
col2.metric("🛒 Total Orders", f"{len(filtered):,}")
col3.metric("📦 Units Sold", f"{filtered['quantity'].sum():,}")
col4.metric("💵 Avg Order Value", f"₹{filtered['revenue'].mean():,.0f}")

st.divider()

# Charts row 1
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Monthly Revenue Trend")
    monthly = filtered.groupby("month")["revenue"].sum().reset_index()
    fig1 = px.line(monthly, x="month", y="revenue", markers=True,
                   labels={"revenue": "Revenue (₹)", "month": "Month"},
                   color_discrete_sequence=["#1A56A0"])
    fig1.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("🏷️ Revenue by Category")
    cat_rev = filtered.groupby("category")["revenue"].sum().reset_index().sort_values("revenue", ascending=False)
    fig2 = px.bar(cat_rev, x="category", y="revenue",
                  labels={"revenue": "Revenue (₹)", "category": "Category"},
                  color="revenue", color_continuous_scale="Blues")
    st.plotly_chart(fig2, use_container_width=True)

# Charts row 2
col3, col4 = st.columns(2)

with col3:
    st.subheader("🌍 Revenue by Region")
    reg_rev = filtered.groupby("region")["revenue"].sum().reset_index()
    fig3 = px.pie(reg_rev, names="region", values="revenue", hole=0.4,
                  color_discrete_sequence=px.colors.sequential.Blues_r)
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("📦 Top 10 Products")
    top_products = filtered.groupby("product")["revenue"].sum().reset_index().sort_values("revenue", ascending=False).head(10)
    fig4 = px.bar(top_products, x="revenue", y="product", orientation="h",
                  labels={"revenue": "Revenue (₹)", "product": "Product"},
                  color="revenue", color_continuous_scale="Blues")
    fig4.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig4, use_container_width=True)

# Raw data table
st.divider()
st.subheader("📋 Raw Data")
st.dataframe(filtered.sort_values("date", ascending=False).head(100), use_container_width=True)