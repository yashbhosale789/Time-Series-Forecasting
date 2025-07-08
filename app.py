import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# Set page configuration
st.set_page_config(page_title="Sales Forecasting Dashboard", layout="wide", page_icon="📊")

# Custom CSS for professional styling
st.markdown(
    """
    <style>
    .main { background-color: #f8f9fa; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { 
        height: 50px; 
        white-space: nowrap; 
        background-color: #ffffff; 
        border-radius: 4px; 
        color: #333333; 
        font-weight: 500; 
        padding: 0 20px; 
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] { 
        background-color: #007bff; 
        color: white; 
    }
    .stButton>button { 
        background-color: #007bff; 
        color: white; 
        border-radius: 4px; 
        border: none; 
        padding: 10px 20px; 
    }
    .stButton>button:hover { 
        background-color: #0056b3; 
        color: white; 
    }
    .metric-card { 
        background-color: white; 
        padding: 20px; 
        border-radius: 8px; 
        box-shadow: 0 2px 4px rgba(0,0,0,0.1); 
        text-align: center; 
    }
    .metric-card h3 { 
        margin: 0; 
        color: #333333; 
        font-size: 1.2rem; 
    }
    .metric-card p { 
        margin: 5px 0 0; 
        color: #007bff; 
        font-size: 1.5rem; 
        font-weight: bold; 
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and description
st.title("📊 Sales Forecasting Dashboard")
st.markdown("""
This dashboard provides insights into sales forecasts for various products from June 2025 to May 2026. 
Explore MAPE scores to evaluate model performance and view future predictions with interactive visualizations.
""")

# Tabs for navigation
tab1, tab2, tab3 = st.tabs(["Overview", "MAPE Scores", "Future Predictions"])

# Load data
@st.cache_data
def load_data():
    try:
        mape_df = pd.read_csv('mape_scores_monthly.csv')
        future_df = pd.read_csv('future_predictions_monthly.csv')
        return mape_df, future_df
    except FileNotFoundError:
        st.error("Data files not found. Please ensure 'mape_scores_monthly.csv' and 'future_predictions_monthly.csv' are in the same directory as this app.")
        return None, None

mape_df, future_df = load_data()

if mape_df is None or future_df is None:
    st.stop()

# Overview Tab
with tab1:
    st.header("Forecasting Overview")
    st.markdown("This section provides a high-level summary of the forecasting models and their performance.")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            '<div class="metric-card"><h3>Total Products</h3><p>{}</p></div>'.format(len(mape_df)),
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            '<div class="metric-card"><h3>Forecast Horizon</h3><p>12 Months</p></div>',
            unsafe_allow_html=True
        )
    with col3:
        avg_mape = mape_df[['SES', 'DES', 'TES', 'MA', 'ARIMA', 'Auto ARIMA']].mean().mean()
        st.markdown(
            '<div class="metric-card"><h3>Average MAPE</h3><p>{:.2f}%</p></div>'.format(avg_mape),
            unsafe_allow_html=True
        )

    st.subheader("Model Performance Summary")
    model_means = mape_df[['SES', 'DES', 'TES', 'MA', 'ARIMA', 'Auto ARIMA']].mean().reset_index()
    model_means.columns = ['Model', 'Average MAPE']
    fig = px.bar(model_means, x='Model', y='Average MAPE', 
                 title='Average MAPE Across Models', 
                 color='Model', 
                 color_discrete_sequence=px.colors.qualitative.Safe)
    fig.update_layout(showlegend=False, yaxis_title="MAPE (%)", xaxis_title="Model")
    st.plotly_chart(fig, use_container_width=True)

# MAPE Scores Tab
with tab2:
    st.header("Model Performance (MAPE Scores)")
    st.markdown("Review the Mean Absolute Percentage Error (MAPE) for each forecasting model across products.")

    # Product filter
    product_ids = mape_df['Product ID'].dropna().unique()
    selected_product = st.selectbox("Select Product", ["All"] + list(product_ids))

    if selected_product == "All":
        display_df = mape_df
    else:
        display_df = mape_df[mape_df['Product ID'] == selected_product]

    st.dataframe(display_df.style.format({
        'SES': '{:.2f}',
        'DES': '{:.2f}',
        'TES': '{:.2f}',
        'MA': '{:.2f}',
        'ARIMA': '{:.2f}',
        'Auto ARIMA': '{:.2f}'
    }), use_container_width=True)

    # Download button
    csv = display_df.to_csv(index=False)
    st.download_button(
        label="Download MAPE Scores",
        data=csv,
        file_name="mape_scores_filtered.csv",
        mime="text/csv"
    )

    # Visualization
    if selected_product != "All":
        product_mape = display_df[['SES', 'DES', 'TES', 'MA', 'ARIMA', 'Auto ARIMA']].T.reset_index()
        product_mape.columns = ['Model', 'MAPE']
        fig = px.bar(product_mape, x='Model', y='MAPE', 
                     title=f'MAPE Scores for {selected_product}', 
                     color='Model', 
                     color_discrete_sequence=px.colors.qualitative.Safe)
        fig.update_layout(showlegend=False, yaxis_title="MAPE (%)", xaxis_title="Model")
        st.plotly_chart(fig, use_container_width=True)

# Future Predictions Tab
with tab3:
    st.header("Future Sales Predictions")
    st.markdown("Explore forecasted sales from June 2025 to May 2026 for each product.")

    # Product filter
    selected_product = st.selectbox("Select Product", ["All"] + list(future_df['Product ID'].dropna().unique()), key="future_product")

    if selected_product == "All":
        display_df = future_df
    else:
        display_df = future_df[future_df['Product ID'] == selected_product]

    st.dataframe(display_df.style.format({col: '{:.0f}' for col in display_df.columns if col != 'Product ID'}), 
                 use_container_width=True)

    # Download button
    csv = display_df.to_csv(index=False)
    st.download_button(
        label="Download Predictions",
        data=csv,
        file_name="future_predictions_filtered.csv",
        mime="text/csv"
    )

    # Visualization
    if selected_product != "All":
        product_data = display_df.drop(columns=['Product ID']).T.reset_index()
        product_data.columns = ['Month', 'Sales']
        product_data['Month'] = pd.to_datetime(product_data['Month'], format='%b-%Y')
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=product_data['Month'],
            y=product_data['Sales'],
            mode='lines+markers',
            name='Forecasted Sales',
            line=dict(color='#007bff')
        ))
        fig.update_layout(
            title=f'Sales Forecast for {selected_product}',
            xaxis_title='Month',
            yaxis_title='Sales Quantity',
            xaxis=dict(tickformat='%b-%Y', tickangle=45),
            showlegend=True
        )
        st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("**Data Source: Cleaned_Sales_History.xlsx | Forecast Period: Jun 2025 - May 2026**")