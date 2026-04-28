import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random
import base64
import os

# Sample data functions - no database needed
def get_latest_data():
    return {
        'lake_elevation': 456.78,
        'peak_load': 2845.50,
        'generation': 3420.25,
        'gate_opening': 3.45,
        'date': '2025-04-28'
    }

def get_previous_data():
    return {
        'lake_elevation': 455.89,
        'peak_load': 2765.30,
        'generation': 3290.15,
        'gate_opening': 3.38,
        'date': '2025-04-27'
    }

def get_monthly_data(year=2025, include_samples=True):
    return pd.DataFrame({
        'month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        'max_lake_elevation': [456.5, 457.2, 456.8, 457.1, 456.9, 457.3, 456.7, 457.0, 456.6, 457.4, 456.8, 457.2],
        'max_peak_load': [2800, 2900, 2850, 2950, 2820, 2980, 2790, 2920, 2810, 2960, 2830, 2940]
    })

def get_april_daily_data():
    dates = ['2025-04-01', '2025-04-05', '2025-04-10', '2025-04-15', '2025-04-20', '2025-04-25']
    data = []
    for date in dates:
        data.append({
            'date': date,
            'lake_elevation': 456 + random.uniform(-1, 1),
            'peak_load': 2850 + random.uniform(-100, 100),
            'generation': 3400 + random.uniform(-100, 100),
            'gate_opening': 3.5 + random.uniform(-0.2, 0.2)
        })
    return pd.DataFrame(data)

def get_daily_data_for_chart(days=30):
    data = []
    for i in range(days):
        date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        data.append({
            'date': date,
            'lake_elevation': 456 + random.uniform(-1, 1),
            'peak_load': 2850 + random.uniform(-100, 100),
            'generation': 3400 + random.uniform(-100, 100)
        })
    df = pd.DataFrame(data)
    return df.sort_values('date')

def calculate_percentage_change(current, previous):
    if previous == 0:
        return 0
    change = ((current - previous) / previous) * 100
    return change

def get_header_html(title="AGUS V Operation", subtitle="Real-time Monitoring Dashboard"):
    def get_base64_of_bin_file(bin_file):
        if not os.path.exists(bin_file):
            return None
        with open(bin_file, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()

    logo_base64 = get_base64_of_bin_file("NPC_LOGO_display.png")
    logo_html = f'<img src="data:image/png;base64,{logo_base64}" style="height:60px; margin-right:20px;">' if logo_base64 else ''
    
    current_time = datetime.now().strftime("%B %d, %Y %I:%M %p")
    
    header_html = f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 20px; border-radius: 10px; margin-bottom: 20px; 
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <div style="display: flex; align-items: center;">
                {logo_html}
                <div>
                    <h1 style="color: white; margin: 0; font-size: 28px; font-weight: bold;">{title}</h1>
                    <p style="color: rgba(255,255,255,0.9); margin: 5px 0 0 0; font-size: 16px;">{subtitle}</p>
                </div>
            </div>
            <div style="text-align: right;">
                <p style="color: white; margin: 0; font-size: 14px;">{current_time}</p>
                <p style="color: rgba(255,255,255,0.8); margin: 0; font-size: 12px;">Live Monitoring</p>
            </div>
        </div>
    </div>
    """
    return header_html

def create_daily_chart():
    df = get_daily_data_for_chart(30)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['date'], 
        y=df['lake_elevation'],
        mode='lines+markers',
        name='Lake Elevation (m)',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=6)
    ))
    
    fig.add_trace(go.Scatter(
        x=df['date'], 
        y=df['peak_load']/10,
        mode='lines+markers',
        name='Peak Load (MW/10)',
        line=dict(color='#ff7f0e', width=3),
        marker=dict(size=6)
    ))
    
    fig.add_trace(go.Scatter(
        x=df['date'], 
        y=df['generation']/10,
        mode='lines+markers',
        name='Generation (MW/10)',
        line=dict(color='#2ca02c', width=3),
        marker=dict(size=6)
    ))
    
    fig.update_layout(
        title="Daily Operations - Last 30 Days",
        xaxis_title="Date",
        yaxis_title="Values",
        hovermode='x unified',
        template='plotly_white',
        height=400,
        margin=dict(l=50, r=20, t=80, b=30),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11)
        )
    )
    
    return fig

def create_monthly_chart():
    df = get_monthly_data()
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df['month'],
        y=df['max_lake_elevation'],
        name='Lake Elevation (m)',
        marker_color='#1f77b4',
        opacity=0.8
    ))
    
    fig.add_trace(go.Bar(
        x=df['month'],
        y=df['max_peak_load']/100,
        name='Peak Load (MW/100)',
        marker_color='#ff7f0e',
        opacity=0.8
    ))
    
    fig.update_layout(
        title="Monthly Comparison - 2025",
        xaxis_title="Month",
        yaxis_title="Values",
        barmode='group',
        template='plotly_white',
        height=400,
        margin=dict(l=25, r=25, t=80, b=25),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.15,
            xanchor="right",
            x=1,
            font=dict(size=10)
        )
    )
    
    return fig

def main():
    st.set_page_config(
        page_title="Operation Dashboard",
        page_icon="⚡",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.markdown(get_header_html(), unsafe_allow_html=True)
    
    # Get data
    latest_data = get_latest_data()
    previous_data = get_previous_data()
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        lake_change = calculate_percentage_change(latest_data['lake_elevation'], previous_data['lake_elevation'])
        st.metric(
            "Lake Elevation", 
            f"{latest_data['lake_elevation']:.2f} m",
            f"{lake_change:+.2f}%" if lake_change != 0 else "No change"
        )
    
    with col2:
        load_change = calculate_percentage_change(latest_data['peak_load'], previous_data['peak_load'])
        st.metric(
            "Peak Load", 
            f"{latest_data['peak_load']:.2f} MW",
            f"{load_change:+.2f}%" if load_change != 0 else "No change"
        )
    
    with col3:
        gen_change = calculate_percentage_change(latest_data['generation'], previous_data['generation'])
        st.metric(
            "Power Generation", 
            f"{latest_data['generation']:.2f} MW",
            f"{gen_change:+.2f}%" if gen_change != 0 else "No change"
        )
    
    with col4:
        gate_change = calculate_percentage_change(latest_data['gate_opening'], previous_data['gate_opening'])
        st.metric(
            "Gate Opening", 
            f"{latest_data['gate_opening']:.2f} m",
            f"{gate_change:+.2f}%" if gate_change != 0 else "No change"
        )
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        fig_daily = create_daily_chart()
        st.plotly_chart(fig_daily, use_container_width=True, config={'displayModeBar': False})
    
    with col2:
        fig_monthly = create_monthly_chart()
        st.plotly_chart(fig_monthly, use_container_width=True, config={'displayModeBar': False})
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666; padding: 20px;'>"
        "🚀 Operation Dashboard - Real-time Monitoring System<br>"
        "<small>Sample Data for Demonstration | Streamlit Cloud Deployment</small>"
        "</div>", 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
