import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(page_title="Northwind Business Dashboard", layout="wide")

# -----------------------------
# Custom CSS Styling
# -----------------------------
st.markdown("""
    <style>
        .block-container {
            padding-top: 2rem;
        }
        h1 {
            padding-top: 0.5rem !important;
            margin-bottom: 0.2rem !important;
        }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# Page Title & Subtitle
# -----------------------------
st.markdown("""
    <h1 style='font-size:40px; padding-top:0px;'>📊 Northwind Business Intelligence Dashboard</h1>
    <h4>Business Insights into Revenue, Customers, Products & Shipping</h4>
    <hr style='margin-top: -10px;'>
""", unsafe_allow_html=True)

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data

def load_data():
    df = pd.read_csv("northwind_master_dataset.csv")
    df['OrderMonth'] = pd.to_datetime(df['OrderMonth'], errors='coerce')
    df = df.dropna(subset=['OrderMonth'])
    return df

df = load_data()

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🔎 Filters")
min_date = df['OrderMonth'].min().date()
max_date = df['OrderMonth'].max().date()
date_range = st.sidebar.date_input("Select Order Month Range:", (min_date, max_date))
if isinstance(date_range, tuple) and len(date_range) == 2:
    df = df[(df['OrderMonth'].dt.date >= date_range[0]) & (df['OrderMonth'].dt.date <= date_range[1])]

countries = ['All'] + sorted(df['ShipCountry'].dropna().unique().tolist())
selected_country = st.sidebar.selectbox("Select Country:", countries)
if selected_country != 'All':
    df = df[df['ShipCountry'] == selected_country]

categories = ['All'] + sorted(df['CategoryName'].dropna().unique().tolist())
selected_category = st.sidebar.selectbox("Select Category:", categories)
if selected_category != 'All':
    df = df[df['CategoryName'] == selected_category]

# -----------------------------
# Executive Summary
# -----------------------------
st.subheader("📌 Executive Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"${df['Revenue'].sum():,.2f}")
col2.metric("Avg Order Value", f"${df.groupby('OrderID')['Revenue'].sum().mean():,.2f}")
col3.metric("Orders / Customers", f"{df['OrderID'].nunique():,} / {df['CustomerCompany'].nunique():,}")

ship_perf = df.groupby('ShipperCompany').agg({'Freight':'mean','DeliveryDays':'mean','OrderID':'nunique'}).sort_values('Freight')
shipper = ship_perf.index[0] if not ship_perf.empty else 'N/A'
fastest = ship_perf.sort_values('DeliveryDays').index[0] if not ship_perf.empty else 'N/A'
ontime = len(df[df['ShippedDateMissing']==False])/len(df)*100 if len(df)>0 else 0

st.markdown(f"""
- ✅ **Best Shipper by Cost**: `{shipper}`
- 🚚 **Fastest Shipper**: `{fastest}`
- ⏱️ **Avg Delivery Time**: `{df['DeliveryDays'].mean():.1f}` days
- 📦 **On-time Shipments**: `{ontime:.1f}%`
""")

st.markdown("---")

# -----------------------------
# Monthly Revenue Trend
# -----------------------------
st.subheader("📈 Visual Data Highlights")

monthly_rev = df.groupby(df['OrderMonth'].dt.to_period('M'))['Revenue'].sum().reset_index()
monthly_rev['OrderMonth'] = monthly_rev['OrderMonth'].dt.to_timestamp()
fig1 = px.area(monthly_rev, x='OrderMonth', y='Revenue',
               title='<b>Monthly Revenue Trend</b><br><span style="font-size:12px; font-weight:bold; color:grey">By Order Month</span>',
               color_discrete_sequence=['#4C78A8'])
fig1.update_traces(line=dict(width=4), fillcolor='rgba(76,120,168,0.2)')
if not monthly_rev.empty:
    peak = monthly_rev.loc[monthly_rev['Revenue'].idxmax()]
    fig1.add_annotation(x=peak['OrderMonth'], y=peak['Revenue'], text=f"Peak: ${peak['Revenue']:,.0f}", showarrow=True, arrowhead=1, ax=0, ay=-40, font=dict(color='green'))
fig1.update_layout(yaxis_tickprefix='$', plot_bgcolor='#f0f2f6')
st.plotly_chart(fig1, use_container_width=True)

# -----------------------------
# Top 10 Customers
# -----------------------------
top_customers = df.groupby('CustomerCompany')['Revenue'].sum().nlargest(10).reset_index().sort_values('Revenue')
fig2 = px.bar(top_customers, x='Revenue', y='CustomerCompany', orientation='h', color='Revenue',
              color_continuous_scale='Teal',
              text=[f"${x:,.0f}" for x in top_customers['Revenue']],
              title='<b>Top 10 Customers</b><br><span style="font-size:12px; font-weight:bold; color: grey">By Total Revenue</span>')
fig2.update_layout(xaxis_tickprefix='$', yaxis={'categoryorder':'total ascending'},
                   yaxis_title='Customer Company',
                   coloraxis_colorbar=dict(tickprefix='$', len=1.1, y=0.5), plot_bgcolor='#f0f2f6')
st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# Top 5 Products (Treemap)
# -----------------------------
top_products = (df.groupby(['CategoryName', 'ProductName'])['Revenue'].sum().reset_index()
                  .sort_values(['CategoryName', 'Revenue'], ascending=[True, False])
                  .groupby('CategoryName').head(5))
fig3 = px.treemap(top_products, path=['CategoryName','ProductName'], values='Revenue', color='Revenue',
                  title='<b>Top 5 Products</b><br><span style="font-size:12px; font-weight:bold; color: grey">Revenue Distribution across Categories</span>',
                  color_continuous_scale='Blues')
fig3.update_layout(coloraxis_colorbar=dict(tickprefix='$', len=1.1, y=0.5), plot_bgcolor='#f0f2f6', height=500)
st.plotly_chart(fig3, use_container_width=True)

# -----------------------------
# Global Revenue Distribution
# -----------------------------
country_revenue = df.groupby('ShipCountry')['Revenue'].sum().reset_index()
fig4 = px.choropleth(country_revenue, locations='ShipCountry', locationmode='country names', color='Revenue',
                     title='<b>Global Revenue Distribution</b><br><span style="font-size:12px; font-weight:bold; color: grey">Revenue by Country</span>',
                     color_continuous_scale='Viridis')
fig4.update_layout(coloraxis_colorbar=dict(tickprefix='$', len=1.1, y=0.5), plot_bgcolor='#f0f2f6',
                   dragmode=False, geo=dict(projection_scale=1))
st.plotly_chart(fig4, use_container_width=True)

# -----------------------------
# Freight Cost Distribution
# -----------------------------
fig5 = px.box(df, x='ShipCountry', y='Freight', color='ShipperCompany', notched=True, hover_data=['DeliveryDays'],
              title='<b>Freight Cost Distribution by Country</b><br><span style="font-size:12px; font-weight:bold; color: grey">Best Shipper Federal Shipping</span>',
              color_discrete_sequence=['#1F77B4','#4C5AC5','#2CA02C'])
fig5.update_layout(plot_bgcolor='#f0f2f6')
fig5.add_hline(y=df['Freight'].mean(), line_dash="dot", line_color="red")
st.plotly_chart(fig5, use_container_width=True)

# -----------------------------
# Data Table
# -----------------------------
st.markdown("---")
st.subheader("📄 Filtered Data Table")
st.dataframe(df, use_container_width=True, height=400)

csv = df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download CSV", data=csv, file_name='northwind_filtered_data.csv', mime='text/csv')

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.markdown("Developed by **Mohit Kumar** | Powered by **Streamlit** & **Plotly**")
