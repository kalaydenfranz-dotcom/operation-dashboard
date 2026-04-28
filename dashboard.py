import streamlit as st

import pandas as pd

import plotly.graph_objects as go

import plotly.express as px

from datetime import datetime

import database



def calculate_percentage_change(current, previous):

    """Calculate percentage change between current and previous values"""

    if previous == 0:

        return 0

    change = ((current - previous) / previous) * 100

    return change



def get_header_html(title="AGUS V Operation", subtitle="Real-time Monitoring Dashboard", show_secret=False):

    """Returns the common professional header HTML used across all pages"""

    import base64

    import os

    from datetime import datetime



    def get_base64_of_bin_file(bin_file):

        if not os.path.exists(bin_file):

            return None

        with open(bin_file, "rb") as f:

            data = f.read()

        return base64.b64encode(data).decode()



    # Try different possible paths for the logo

    logo_path = "NPC_LOGO_display.png"

    if not os.path.exists(logo_path):

        logo_path = os.path.join("static", "images", "NPC LOGO.png")

    

    logo_base64 = get_base64_of_bin_file(logo_path)

    

    if logo_base64:

        logo_img_html = f'<img src="data:image/png;base64,{logo_base64}" style="width: 38px; height: 38px; object-fit: contain; filter: drop-shadow(rgba(0, 0, 0, 0.3) 0px 2px 4px); z-index: 2; display: block;">'

    else:

        logo_img_html = '<div style="width: 38px; height: 38px; background: rgba(255,255,255,0.2); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 12px; z-index: 2;">NPC</div>'



    # Get current date and time

    now = datetime.now()

    current_day = now.strftime("%d")

    current_month_year = now.strftime("%b %Y")

    current_weekday = now.strftime("%a")

    current_time = now.strftime("%I:%M %p")

    

    secret_modal_html = ""

    secret_script_html = ""

    

    if show_secret:

        secret_modal_html = f"""

<div id="secretModalOverlay" class="secret-modal-overlay">

    <div class="secret-modal">

        <span class="modal-close" onclick="closeSecretModal()">✕</span>

        <div class="creator-avatar">👨‍💻</div>

        <h2 style="margin-bottom: 10px; background: linear-gradient(to right, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Creator Profile</h2>

        <p style="color: rgba(255, 255, 255, 0.6); font-size: 14px; margin-bottom: 25px;">You've discovered the hidden control center.</p>

        <input type="text" class="modal-input" placeholder="Creator Name" id="creatorName">

        <input type="text" class="modal-input" placeholder="Designation" id="creatorRole">

        <input type="text" class="modal-input" placeholder="GitHub/Portfolio URL" id="creatorLink">

        <button class="save-btn" onclick="saveCreatorProfile()">Initialize Core</button>

    </div>

</div>"""

        

        secret_script_html = ""



    html_parts = [
        '<style>',
        '@keyframes shimmer-effect {',
        '0% { transform: translateX(-100%) rotate(45deg); opacity: 0; }',
        '50% { opacity: 0.5; }',
        '100% { transform: translateX(200%) rotate(45deg); opacity: 0; }',
        '}',
        '@keyframes pulse-effect {',
        '0%, 100% { transform: scale(1); opacity: 1; }',
        '50% { transform: scale(1.1); opacity: 0.8; }',
        '}',
        '@keyframes modalFadeIn {',
        'from { opacity: 0; transform: scale(0.8); }',
        'to { opacity: 1; transform: scale(1); }',
        '}',
        '@keyframes floatAnimation {',
        '0%, 100% { transform: translateY(0px); }',
        '50% { transform: translateY(-10px); }',
        '}',
        '.header-container {',
        'background: linear-gradient(135deg, rgba(102, 126, 234, 0.95) 0%, rgba(118, 75, 162, 0.95) 100%);',
        'padding: 12px 25px;',
        'border-radius: 0 0 20px 20px;',
        'margin-bottom: 25px;',
        'box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);',
        'border: 1px solid rgba(255,255,255,0.2);',
        'border-top: none;',
        'backdrop-filter: blur(10px);',
        'font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;',
        'display: flex;',
        'justify-content: space-between;',
        'position: fixed;',
        'top: 0;',
        'left: 50%;',
        'transform: translateX(-50%);',
        'z-index: 9999;',
        'width: calc(100% - 2rem);',
        'max-width: 1200px;',
        'align-items: center;',
        'color: white;',
        'min-height: 70px;',
        'box-sizing: border-box;',
        '}',
        '.header-left {',
        'display: flex;',
        'align-items: center;',
        'gap: 20px;',
        '}',
        '.header-right {',
        'display: flex;',
        'align-items: center;',
        'gap: 25px;',
        '}',
        '.logo-wrapper {',
        'position: relative;',
        'width: 50px;',
        'height: 50px;',
        'border-radius: 50%;',
        'overflow: hidden;',
        'cursor: pointer;',
        'transition: all 0.3s ease;',
        'box-shadow: 0 4px 12px rgba(0,0,0,0.3);',
        'border: 2px solid rgba(255,255,255,0.3);',
        'display: flex;',
        'align-items: center;',
        'justify-content: center;',
        'background: rgba(255,255,255,0.1);',
        '}',
        '.logo-wrapper:hover {',
        'transform: scale(1.05);',
        'box-shadow: 0 6px 16px rgba(0,0,0,0.4);',
        '}',
        '.shimmer-overlay {',
        'position: absolute;',
        'top: -50%;',
        'left: -50%;',
        'width: 200%;',
        'height: 200%;',
        'background: linear-gradient(45deg, transparent, rgba(255,255,255,0.3), transparent);',
        'animation: shimmer-effect 3s infinite;',
        'pointer-events: none;',
        'z-index: 1;',
        '}',
        '.status-dot {',
        'position: absolute;',
        'bottom: -2px;',
        'right: -2px;',
        'width: 12px;',
        'height: 12px;',
        'background: #00ff88;',
        'border-radius: 50%;',
        'border: 2px solid white;',
        'animation: pulse-effect 2s infinite;',
        'z-index: 3;',
        '}',
        '.date-section {',
        'text-align: center;',
        'background: rgba(255,255,255,0.1);',
        'padding: 8px 16px;',
        'border-radius: 12px;',
        'backdrop-filter: blur(5px);',
        'border: 1px solid rgba(255,255,255,0.2);',
        '}',
        '.time-badge {',
        'background: rgba(255,255,255,0.2);',
        'padding: 6px 12px;',
        'border-radius: 20px;',
        'font-weight: 600;',
        'font-size: 14px;',
        'backdrop-filter: blur(5px);',
        'border: 1px solid rgba(255,255,255,0.3);',
        'display: inline-block;',
        '}',
        '@media (max-width: 768px) {',
        '.header-container {',
        'flex-direction: column;',
        'gap: 15px;',
        'padding: 15px;',
        'width: calc(100% - 1rem);',
        '}',
        '.header-left, .header-right {',
        'width: 100%;',
        'justify-content: center;',
        '}',
        '}',
        '.secret-modal {',
        'display: none;',
        'position: fixed;',
        'z-index: 10000;',
        'left: 0;',
        'top: 0;',
        'width: 100%;',
        'height: 100%;',
        'background-color: rgba(0,0,0,0.8);',
        'animation: modalFadeIn 0.3s ease;',
        '}',
        '.secret-modal-content {',
        'position: relative;',
        'background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);',
        'margin: 10% auto;',
        'padding: 30px;',
        'border-radius: 20px;',
        'width: 80%;',
        'max-width: 500px;',
        'text-align: center;',
        'color: white;',
        'box-shadow: 0 20px 60px rgba(0,0,0,0.5);',
        'animation: floatAnimation 3s ease-in-out infinite;',
        '}',
        '.close-modal {',
        'position: absolute;',
        'right: 20px;',
        'top: 20px;',
        'font-size: 28px;',
        'font-weight: bold;',
        'cursor: pointer;',
        'color: rgba(255,255,255,0.8);',
        'transition: color 0.3s ease;',
        '}',
        '.close-modal:hover {',
        'color: white;',
        '}',
        '</style>',
        f'<div class="header-container">',
        f'<div class="header-left">',
        f'<div style="position: relative;">',
        f'<div class="logo-wrapper" id="logoTrigger">',
        f'<div class="shimmer-overlay"></div>',
        f'{logo_img_html}',
        f'</div>',
        f'<div class="status-dot"></div>',
        f'</div>',
        f'<div>',
        f'<div style="font-size: 24px; font-weight: 700; text-shadow: 0 2px 4px rgba(0,0,0,0.2); line-height: 1.2;">{title}</div>',
        f'<div style="color: rgba(255,255,255,0.8); font-size: 16px; font-weight: 500;">{subtitle}</div>',
        f'</div>',
        f'</div>',
        f'<div class="header-right">',
        f'<div class="date-section">',
        f'<div style="font-size: 22px; font-weight: 700; line-height: 1;">{current_day}</div>',
        f'<div style="font-size: 14px; font-weight: 600; text-transform: uppercase; margin-top: 2px;">{current_month_year}</div>',
        f'</div>',
        f'<div style="text-align: right;">',
        f'<div style="font-size: 16px; font-weight: 500; margin-bottom: 2px; text-transform: uppercase; color: rgba(255,255,255,0.7);">{current_weekday}</div>',
        f'<div class="time-badge"><span>🕐</span> {current_time}</div>',
        f'</div>',
        f'</div>',
        f'</div>',
        f'{secret_script_html}'
    ]
    
    return ''.join(html_parts)



def create_metric_card(title, value, change, icon="📊", unit="", show_no_data=False):

    """Create a styled metric card"""

    if show_no_data or change == 0:
        # Show "No previous data" when there's no comparison data
        change_display = "No previous data"
        change_color = "#999"
    else:
        change_color = "green" if change > 0 else "red"
        change_symbol = "↑" if change > 0 else "↓"
        change_display = f"{abs(change):.2f}%{change_symbol}"

    # Use a single line HTML to avoid formatting issues
    html = f'<div class="metric-card"><div style="display:flex;flex-direction:column;align-items:center;text-align:center;width:100%;"><div style="font-size:16px;color:#666;margin-bottom:8px;">{title}</div><div style="font-size:32px;font-weight:bold;color:#333;line-height:1.2;">{value} {unit}</div><div style="font-size:18px;color:{change_color};font-weight:600;margin-top:5px;">{change_display}</div></div></div>'
    
    st.markdown(html, unsafe_allow_html=True)



def create_daily_data_chart(height=None):

    """Create the daily data chart with compact arc area style matching the reference design"""

    df = database.get_daily_data_for_chart(7)

    

    if df.empty:

        return go.Figure()

    

    # Use dynamic height if not provided

    if height is None:

        height = 450  # Default fallback height for full-screen

    

    # Get the latest data for gauge chart

    latest_data = df.iloc[-1] if not df.empty else None

    

    if latest_data is None:

        return go.Figure()

    

    generation_value = float(latest_data['generation'])

    lake_level_value = float(latest_data['lake_level']) if 'lake_level' in latest_data else float(latest_data.get('lake_elevation', 0))

    peak_load_value = float(latest_data['peak_load'])



    # Build smooth arcs for each series, scaled from the latest value.

    # Use a fixed 11-point arc to mimic the reference visual.

    max_value = 3500

    arc_x = list(range(0, 11))

    base_arc = [0, 500, 1000, 1500, 2000, 2500, 3000, 2800, 2200, 1500, 0]



    def build_arc(latest_val: float, baseline_peak: float = 3000.0):

        scale = min(max(latest_val / baseline_peak, 0.0), 1.35)

        return [min(v * scale, max_value) for v in base_arc]



    gen_y = build_arc(generation_value, 3000.0)

    lake_y = build_arc(lake_level_value, 3000.0)

    peak_y = build_arc(peak_load_value, 3000.0)



    fig = go.Figure()



    # Legend order must be: Generation, Lake Level, Peak Load

    fig.add_trace(go.Scatter(

        x=arc_x,

        y=gen_y,

        mode='lines+markers',

        line=dict(color='#e84393', width=3, shape='spline', smoothing=1.1),

        marker=dict(size=6, color='#e84393'),

        fill='tozeroy',

        fillcolor='rgba(232, 67, 147, 0.20)',

        name='Generation (kWh)',

        hovertemplate='<b style="font-size: 16px; font-family: Arial, sans-serif;">Generation: %{y:.0f} kWh</b><extra></extra>'

    ))



    fig.add_trace(go.Scatter(

        x=arc_x,

        y=lake_y,

        mode='lines+markers',

        line=dict(color='#74b9ff', width=3, shape='spline', smoothing=1.1),

        marker=dict(size=6, color='#74b9ff'),

        fill='tozeroy',

        fillcolor='rgba(116, 185, 255, 0.20)',

        name='Lake Level (m)',

        hovertemplate='<b style="font-size: 16px; font-family: Arial, sans-serif;">Lake Level: %{y:.0f} m</b><extra></extra>'

    ))



    fig.add_trace(go.Scatter(

        x=arc_x,

        y=peak_y,

        mode='lines+markers',

        line=dict(color='#2e6bd6', width=3, shape='spline', smoothing=1.1),

        marker=dict(size=6, color='#2e6bd6'),

        fill='tozeroy',

        fillcolor='rgba(46, 107, 214, 0.20)',

        name='Peak Load (kWh)',

        hovertemplate='<b style="font-size: 16px; font-family: Arial, sans-serif;">Peak Load: %{y:.0f} kWh</b><extra></extra>'

    ))

    

    # Update layout to match the gauge design

    fig.update_layout(

        title=dict(

            text='Daily Data Graph',

            x=0.5,

            xanchor='center',

            y=0.97,

            font=dict(size=28, color='#2c3e50', family='Arial, sans-serif')

        ),

        xaxis=dict(

            visible=False,

            showgrid=False,

            zeroline=False,

            fixedrange=True

        ),

        yaxis=dict(

            range=[0, max_value],

            tickmode='array',

            tickvals=[0, 1000, 2000, 3000],

            ticktext=['0', '1000', '2000', '3000+'],

            showgrid=True,

            gridcolor='rgba(0,0,0,0.08)',

            gridwidth=1,

            zeroline=False,

            ticks='outside',

            tickfont=dict(size=22, color='#666', family='Arial, sans-serif'),

            fixedrange=True

        ),

        showlegend=True,

        legend=dict(

            orientation="h",

            yanchor="top",

            y=1.05,

            xanchor="center",

            x=0.5,

            bgcolor='rgba(255,255,255,0.95)',

            bordercolor='rgba(0,0,0,0.15)',

            borderwidth=1,

            font=dict(size=18, color='#2c3e50', family='Arial, sans-serif')

        ),

        height=height,

        margin=dict(l=55, r=25, t=120, b=40),

        paper_bgcolor='rgba(255,255,255,0.98)',

        plot_bgcolor='rgba(255,255,255,0.98)',

        font=dict(family='Arial, sans-serif')

    )

    

    return fig



def create_monthly_comparison_chart(height=None):

    """Create the monthly comparison chart with modern design"""

    from datetime import datetime

    

    # Get current month to exclude it from the summary

    current_month_num = datetime.now().month

    current_month_name = datetime.now().strftime('%b')  # 'Apr', 'May', etc.

    

    df = database.get_monthly_data()

    

    # Always override current month with zeros until month ends

    df = df[df['month'] != current_month_name]  # Remove any existing current month data

    

    # Add current month with zero values

    current_month_row = pd.DataFrame({

        'month': [current_month_name],

        'max_lake_elevation': [0],

        'max_peak_load': [None]

    })

    df = pd.concat([df, current_month_row], ignore_index=True)

    

    # Sort months in chronological order

    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    df['month'] = pd.Categorical(df['month'], categories=month_order, ordered=True)

    df = df.sort_values('month')

    

    # Use dynamic height if not provided

    if height is None:

        height = 450  # Default fallback height for full-screen

    

    if df.empty:

        fig = go.Figure()

        fig.update_layout(

            title=dict(

                text="Maximum Peak Load vs Maximum Lake Elevation",

                x=0.5,

                xanchor="center",

                y=0.95,

                yanchor="top",

                font=dict(size=20, color='#2c3e50', family='Arial, sans-serif')

            ),

            height=height,

            margin=dict(l=30, r=30, t=90, b=30),

            paper_bgcolor='rgba(255,255,255,0.98)',

            plot_bgcolor='rgba(248,249,250,0.8)'

        )

        fig.add_annotation(

            text="No monthly summary data",

            x=0.5,

            y=0.5,

            xref="paper",

            yref="paper",

            showarrow=False,

            font=dict(size=12, color="#666")

        )

        return fig

    

    fig = go.Figure()

    

    # Add bars for Maximum Lake Elevation with modern styling

    fig.add_trace(go.Bar(

        x=df['month'],

        y=df['max_lake_elevation'],

        name='Maximum Lake Elevation (m)',

        marker_color='#2ECC71',

        marker_line=dict(width=2, color='white'),

        yaxis='y',

        hovertemplate='<b style="font-size: 16px; font-family: Arial, sans-serif;">Month: %{x}<br>Lake Elevation: %{y:.1f} m</b><extra></extra>'

    ))

    

    # Add line for Maximum Peak Load with wave-like styling like charts 3 and 4

    # Replace None with 0 to show line at zero level (like other charts)

    peak_load_data = df[['month', 'max_peak_load']].copy()

    peak_load_data['max_peak_load'] = peak_load_data['max_peak_load'].fillna(0)

    

    # Always show the line, even if values are zero

    fig.add_trace(go.Scatter(

        x=peak_load_data['month'],

        y=peak_load_data['max_peak_load'],

        mode='lines+markers',

        name='Maximum Peak Load (kWh)',

        line=dict(color='#ff4757', width=4, shape='spline', smoothing=1.3),

        marker=dict(size=8, color='#ff4757', line=dict(width=2, color='white')),

        yaxis='y2',

        hovertemplate='<b style="font-size: 16px; font-family: Arial, sans-serif;">Month: %{x}<br>Peak Load: %{y:.0f} kWh</b><extra></extra>'

    ))

    

    # Add actual data points as markers

    non_null_peak = df[df['max_peak_load'].notna()]

    if not non_null_peak.empty:

        fig.add_trace(go.Scatter(

            x=non_null_peak['month'],

            y=non_null_peak['max_peak_load'],

            mode='markers',

            name='Peak Load Points',

            marker=dict(size=4, color='#ff4757', line=dict(width=1, color='white'), symbol='circle'),

            yaxis='y2',

            hovertemplate='<b style="font-size: 16px; font-family: Arial, sans-serif;">Month: %{x}<br>Peak Load: %{y:.0f} kWh</b><extra></extra>',

            showlegend=False

        ))

    

    fig.update_layout(

        title=dict(

            text="Maximum Peak Load vs Maximum Lake Elevation",

            x=0.5,

            xanchor="center",

            y=0.95,

            yanchor="top",

            font=dict(size=28, color='#2c3e50', family='Arial, sans-serif')

        ),

        xaxis_title=dict(text="Month", font=dict(size=20, color='#2c3e50', family='Arial, sans-serif')),

        yaxis=dict(

            title=dict(text="Maximum Lake Elevation", font=dict(size=20, color="#2ECC71", family='Arial, sans-serif')),

            tickfont=dict(size=22, color="#2ECC71", family='Arial, sans-serif'),

            range=[0, 800],

            tickmode="array",

            tickvals=[0, 200, 400, 600, 800],

            ticktext=["0", "200", "400", "600", "800"],

            autorange=False,

            showgrid=True,

            gridcolor='rgba(0,0,0,0.05)'

        ),

        yaxis2=dict(

            title=dict(text="Maximum Peak Load", font=dict(size=20, color="#ff4757", family='Arial, sans-serif')),

            tickfont=dict(size=22, color="#ff4757", family='Arial, sans-serif'),

            anchor="x",

            overlaying="y",

            side="right",

            range=[0, 4000],

            tickmode="array",

            tickvals=[0, 1000, 2000, 3000, 4000],

            ticktext=["0", "1000", "2000", "3000", "4000"],

            autorange=False,

            scaleratio=1,

            showgrid=True,

            gridcolor='rgba(0,0,0,0.05)'

        ),

        height=height,

        margin=dict(l=30, r=30, t=90, b=30),

        legend=dict(

            orientation="h",

            yanchor="top",

            y=1.05,

            xanchor="center",

            x=0.5,

            bgcolor='rgba(255,255,255,0.98)',

            bordercolor='rgba(44,62,80,0.15)',

            borderwidth=2,

            font=dict(size=11, color='#2c3e50', family='Arial, sans-serif'),

            tracegroupgap=5,

            itemwidth=30,

            itemsizing='constant'

        ),

        paper_bgcolor='rgba(255,255,255,0.98)',

        plot_bgcolor='rgba(248,249,250,0.8)',

        hoverlabel=dict(

            bgcolor="rgba(255,255,255,0.95)",

            bordercolor="rgba(0,0,0,0.1)",

            font=dict(size=12, color='#2c3e50')

        )

    )

    

    return fig



def create_current_month_gate_chart(height=None):

    """Create current month's Gate Opening chart"""

    # Get current month name and year

    current_month = datetime.now().strftime('%B')

    current_year = datetime.now().strftime('%Y')

    current_day = datetime.now().day

    

    # Use dynamic height if not provided

    if height is None:

        height = 500  # Default fallback height for full-screen

    

    # Get days in current month

    import calendar

    days_in_month = calendar.monthrange(int(current_year), datetime.now().month)[1]

    

    # Get daily data for current month

    conn = database.sqlite3.connect('operation_dashboard.db')

    

    query = '''

        SELECT d1.date, 

               d1.gate_opening,

               d1.peak_load

        FROM daily_data d1

        INNER JOIN (

            SELECT date, MAX(timestamp) as max_timestamp

            FROM daily_data 

            WHERE date LIKE ?

            GROUP BY date

        ) d2 ON d1.date = d2.date AND d1.timestamp = d2.max_timestamp

        WHERE d1.date LIKE ?

        ORDER BY d1.date

    '''

    

    current_month_pattern = f'%-{datetime.now().strftime("%m")}-%'

    df = pd.read_sql_query(query, conn, params=(current_month_pattern, current_month_pattern))

    conn.close()

    

    # Create complete month dataframe with all days and interpolate for wave effect

    if df.empty:

        complete_df = pd.DataFrame({

            'day': list(range(1, days_in_month + 1)),

            'gate_opening': [0] * days_in_month

        })

    else:

        # Convert dates to datetime and extract day

        df['date'] = pd.to_datetime(df['date'])

        df['day'] = df['date'].dt.day

        

        # Create complete month dataframe

        complete_df = pd.DataFrame({

            'day': list(range(1, days_in_month + 1)),

            'gate_opening': [0] * days_in_month

        })

        

        # Merge actual data into complete dataframe

        for _, row in df.iterrows():

            idx = row['day'] - 1

            if 0 <= idx < len(complete_df):

                complete_df.iloc[idx, complete_df.columns.get_loc('gate_opening')] = row['gate_opening']

        

        # Interpolate between data points to create smooth wave

        complete_df['gate_opening'] = complete_df['gate_opening'].interpolate(method='cubic')

    

    fig = go.Figure()

    

    # Add Gate Opening line with enhanced visual design (wave only)

    fig.add_trace(go.Scatter(

        x=complete_df['day'],

        y=complete_df['gate_opening'],

        mode='lines',

        name='Gate Opening (m)',

        line=dict(color='#1e88e5', width=4, shape='spline', smoothing=1.3),

        fill='tozeroy',

        fillcolor='rgba(30, 136, 229, 0.15)',

        hovertemplate='<b style="font-size: 16px; font-family: Arial, sans-serif;">Day: %{x}<br>Gate Opening: %{y:.1f} m</b><extra></extra>'

    ))

    

    # Add actual data points as separate markers (only on real data days)

    if not df.empty:

        df['date'] = pd.to_datetime(df['date'])

        df['day'] = df['date'].dt.day

        fig.add_trace(go.Scatter(

            x=df['day'],

            y=df['gate_opening'],

            mode='markers',

            name='Actual Data',

            marker=dict(

                size=4, 

                color='#1e88e5',

                line=dict(width=1, color='white'),

                symbol='circle'

            ),

            hovertemplate='<b style="font-size: 16px; font-family: Arial, sans-serif;">Day: %{x}<br>Gate Opening: %{y:.1f} m</b><extra></extra>',

            showlegend=False

        ))

    

    # Create today arrow only if there's data for today

    today_arrow = []

    if not df.empty:

        df['date'] = pd.to_datetime(df['date'])

        today = datetime.now().date()

        today_data = df[df['date'].dt.date == today]

        

        if not today_data.empty:

            today_arrow = [

                dict(

                    x=current_day,

                    y=0.98,

                    xref='x',

                    yref='paper',

                    text='TODAY',

                    showarrow=True,

                    arrowhead=2,

                    arrowsize=1,

                    arrowwidth=1,

                    arrowcolor='#ff4757',

                    ax=0,

                    ay=-25,

                    font=dict(size=9, color='#ff4757', family='Arial, sans-serif', weight='bold'),

                    bgcolor='rgba(255,255,255,0.9)',

                    bordercolor='#ff4757',

                    borderwidth=1

                )

            ]

    

    fig.update_layout(

        title=dict(

            text=f"{current_month} {current_year}'s Gate Opening",

            x=0.5,

            xanchor="center",

            y=0.95,

            yanchor="top",

            font=dict(size=28, color='#2c3e50', family='Arial, sans-serif')

        ),

        annotations=today_arrow,

        xaxis_title=dict(text="Day", font=dict(size=16, color='#2c3e50', family='Arial, sans-serif')),

        yaxis_title=dict(text="Gate Opening", font=dict(size=16, color='#2c3e50', family='Arial, sans-serif')),

        height=height,

        margin=dict(l=40, r=40, t=120, b=50),

        showlegend=True,

        legend=dict(

            orientation="h",

            yanchor="top",

            y=1.25,

            xanchor="center",

            x=0.5,

            bgcolor='rgba(255,255,255,0.95)',

            bordercolor='rgba(0,0,0,0.1)',

            borderwidth=1,

            font=dict(size=12, color='#2c3e50', family='Arial, sans-serif')

        ),

        xaxis=dict(

            tickmode='array',

            tickvals=list(range(1, days_in_month + 1)),

            ticktext=[str(i) for i in range(1, days_in_month + 1)],

            showgrid=True,

            gridcolor='rgba(0,0,0,0.05)',

            gridwidth=1,

            linecolor='rgba(0,0,0,0.1)',

            linewidth=1,

            tickfont=dict(size=20, color='#666', family='Arial, sans-serif')

        ),

        yaxis=dict(

            showgrid=True,

            gridcolor='rgba(0,0,0,0.05)',

            gridwidth=1,

            linecolor='rgba(0,0,0,0.1)',

            linewidth=1,

            tickfont=dict(size=20, color='#666', family='Arial, sans-serif')

        ),

        plot_bgcolor='rgba(248,249,250,0.8)',

        paper_bgcolor='rgba(255,255,255,0.98)',

        hoverlabel=dict(

            bgcolor="rgba(255,255,255,0.95)",

            bordercolor="rgba(0,0,0,0.1)",

            font=dict(size=12, color='#2c3e50')

        )

    )

    

    return fig



def create_current_month_multi_chart(height=None):

    """Create current month's Lake Level, Generation and Peak Load chart with modern design"""

    # Get current month name (April since we're in April)

    from datetime import datetime

    import calendar

    

    # Use dynamic height if not provided

    if height is None:

        height = 500  # Default fallback height for full-screen

    

    # Get current month

    today = datetime.now()

    current_month = today.month

    current_year = today.year

    

    month_name = calendar.month_name[current_month]  # Should be "April"

    

    # Query current month data

    conn = database.sqlite3.connect('operation_dashboard.db')

    current_month_pattern = f'%-{str(current_month).zfill(2)}-%'

    

    query = '''

        SELECT d1.date,

               d1.lake_elevation,

               d1.generation,

               d1.peak_load

        FROM daily_data d1

        INNER JOIN (

            SELECT date, MAX(timestamp) as max_timestamp

            FROM daily_data 

            WHERE date LIKE ?

            GROUP BY date

        ) d2 ON d1.date = d2.date AND d1.timestamp = d2.max_timestamp

        WHERE d1.date LIKE ?

        ORDER BY d1.date

    '''

    

    df = pd.read_sql_query(query, conn, params=(current_month_pattern, current_month_pattern))

    conn.close()

    

    if df.empty:

        fig = go.Figure()

        fig.update_layout(

            title=dict(

                text=f"{month_name} Lake Level, Generation and Peak Load",

                x=0.5,

                xanchor="center",

                y=0.95,

                yanchor="top",

                font=dict(size=20, color='#2c3e50', family='Arial, sans-serif')

            ),

            height=height,

            margin=dict(l=40, r=40, t=120, b=50),

            paper_bgcolor='rgba(255,255,255,0.98)',

            plot_bgcolor='rgba(248,249,250,0.8)'

        )

        fig.add_annotation(

            text=f"No {month_name} data available. Start inputting daily data to see previous month's charts.",

            x=0.5,

            y=0.5,

            xref="paper",

            yref="paper",

            showarrow=False,

            font=dict(size=12, color="#666")

        )

        return fig

    

    fig = go.Figure()

    

    # Convert dates to datetime and format for display

    df['date'] = pd.to_datetime(df['date'])

    df['day'] = df['date'].dt.day

    

    # Get current month and year

    current_month = datetime.now().month

    current_year = datetime.now().year

    

    # Calculate days in current month

    import calendar

    days_in_month = calendar.monthrange(current_year, current_month)[1]

    

    # Create complete dataframe with all days

    complete_days = list(range(1, days_in_month + 1))

    complete_df = pd.DataFrame({'day': complete_days})

    

    # Merge with actual data, filling missing with zeros

    df_merged = complete_df.merge(df, on='day', how='left')

    df_merged['lake_elevation'] = df_merged['lake_elevation'].fillna(0)

    df_merged['peak_load'] = df_merged['peak_load'].fillna(0)

    df_merged['generation'] = df_merged['generation'].fillna(0)

    

    # Format dates as just day numbers like the 3rd chart

    df_merged['day_label'] = df_merged['day'].astype(str)

    

    # Add Lake Elevation with wave-like styling like 3rd chart

    fig.add_trace(go.Scatter(

        x=df_merged['day_label'],

        y=df_merged['lake_elevation'],

        mode='lines',

        name='Lake Elevation (m)',

        line=dict(color='#1e88e5', width=4, shape='spline', smoothing=1.3),

        fill='tozeroy',

        fillcolor='rgba(30, 136, 229, 0.15)',

        hovertemplate='<b style="font-size: 16px; font-family: Arial, sans-serif;">Day: %{x}<br>Lake Elevation: %{y:.1f} m</b><extra></extra>'

    ))

    

    # Add actual data points as markers

    non_zero_elevation = df_merged[df_merged['lake_elevation'] > 0]

    if not non_zero_elevation.empty:

        fig.add_trace(go.Scatter(

            x=non_zero_elevation['day_label'],

            y=non_zero_elevation['lake_elevation'],

            mode='markers',

            name='Lake Elevation Points',

            marker=dict(size=4, color='#1e88e5', line=dict(width=1, color='white'), symbol='circle'),

            hovertemplate='<b style="font-size: 16px; font-family: Arial, sans-serif;">Day: %{x}<br>Lake Elevation: %{y:.1f} m</b><extra></extra>',

            showlegend=False

        ))

    

    # Add Peak Load with wave-like styling like 3rd chart

    fig.add_trace(go.Scatter(

        x=df_merged['day_label'],

        y=df_merged['peak_load'],

        mode='lines',

        name='Peak Load (kWh)',

        line=dict(color='#ff4757', width=4, shape='spline', smoothing=1.3),

        fill='tonexty',

        fillcolor='rgba(255, 71, 87, 0.15)',

        hovertemplate='<b style="font-size: 16px; font-family: Arial, sans-serif;">Day: %{x}<br>Peak Load: %{y:.0f} kWh</b><extra></extra>'

    ))

    

    # Add actual data points as markers

    non_zero_peak = df_merged[df_merged['peak_load'] > 0]

    if not non_zero_peak.empty:

        fig.add_trace(go.Scatter(

            x=non_zero_peak['day_label'],

            y=non_zero_peak['peak_load'],

            mode='markers',

            name='Peak Load Points',

            marker=dict(size=4, color='#ff4757', line=dict(width=1, color='white'), symbol='circle'),

            hovertemplate='<b style="font-size: 16px; font-family: Arial, sans-serif;">Day: %{x}<br>Peak Load: %{y:.0f} kWh</b><extra></extra>',

            showlegend=False

        ))

    

    # Add Daily Generation with wave-like styling like 3rd chart

    fig.add_trace(go.Scatter(

        x=df_merged['day_label'],

        y=df_merged['generation'],

        mode='lines',

        name='Daily Generation (kWh)',

        line=dict(color='#ffa502', width=4, shape='spline', smoothing=1.3),

        fill='tonexty',

        fillcolor='rgba(255, 165, 2, 0.15)',

        hovertemplate='<b style="font-size: 16px; font-family: Arial, sans-serif;">Day: %{x}<br>Generation: %{y:.1f} kWh</b><extra></extra>'

    ))

    

    # Add actual data points as markers

    non_zero_gen = df_merged[df_merged['generation'] > 0]

    if not non_zero_gen.empty:

        fig.add_trace(go.Scatter(

            x=non_zero_gen['day_label'],

            y=non_zero_gen['generation'],

            mode='markers',

            name='Generation Points',

            marker=dict(size=4, color='#ffa502', line=dict(width=1, color='white'), symbol='circle'),

            hovertemplate='<b style="font-size: 16px; font-family: Arial, sans-serif;">Day: %{x}<br>Generation: %{y:.1f} kWh</b><extra></extra>',

            showlegend=False

        ))

    

    fig.update_layout(

        title=dict(

            text=f"{month_name} Lake Level, Generation and Peak Load",

            x=0.5,

            xanchor="center",

            y=0.95,

            yanchor="top",

            font=dict(size=28, color='#2c3e50', family='Arial, sans-serif', weight='bold')

        ),

        xaxis_title=dict(text="Day", font=dict(size=16, color='#2c3e50', family='Arial, sans-serif')),

        yaxis_title=dict(text="Values", font=dict(size=16, color='#2c3e50', family='Arial, sans-serif')),

        height=height,

        margin=dict(l=50, r=50, t=140, b=60),

        showlegend=True,

        legend=dict(

            orientation="h",

            yanchor="top",

            y=1.25,

            xanchor="center",

            x=0.5,

            bgcolor='rgba(255,255,255,0.98)',

            bordercolor='rgba(44,62,80,0.2)',

            borderwidth=2,

            font=dict(size=14, color='#2c3e50', family='Arial, sans-serif', weight='bold'),

            tracegroupgap=8,

            itemwidth=35,

            itemsizing='constant'

        ),

        paper_bgcolor='rgba(248,249,250,0.95)',

        plot_bgcolor='rgba(255,255,255,0.98)',

        xaxis=dict(

            showgrid=True,

            gridcolor='rgba(0,0,0,0.08)',

            gridwidth=1.5,

            linecolor='rgba(0,0,0,0.15)',

            linewidth=2,

            tickmode='array',

            tickvals=list(range(1, days_in_month + 1, 2)),  # Show every 2nd day

            ticktext=[str(i) for i in range(1, days_in_month + 1, 2)],

            tickfont=dict(size=20, color='#2c3e50', family='Arial, sans-serif'),

            tickangle=0  # Make text horizontal (straight)

        ),

        yaxis=dict(

            showgrid=True,

            gridcolor='rgba(0,0,0,0.08)',

            gridwidth=1.5,

            linecolor='rgba(0,0,0,0.15)',

            linewidth=2,

            tickfont=dict(size=20, color='#2c3e50', family='Arial, sans-serif')

        ),

        hoverlabel=dict(

            bgcolor="rgba(255,255,255,0.98)",

            bordercolor="rgba(0,0,0,0.2)",

            font=dict(size=13, color='#2c3e50', family='Arial, sans-serif')

        )

    )

    

    return fig



def main():

    # Initialize session state FIRST - before any other code

    if 'last_data_count' not in st.session_state:

        st.session_state.last_data_count = -1

    

    # Page configuration with proper theme

    st.set_page_config(

        page_title="Operation Dashboard",

        page_icon="⚡",

        layout="wide",

        initial_sidebar_state="collapsed"

    )

    

    # Clean theme configuration

    st.markdown("""

    <style>

        /* Main theme colors */

        .stApp {

            background-color: #f0f2f6;

        }

        

        /* Card backgrounds */

        .css-1d391kg {

            background-color: #f0f2f6;

        }

        .css-1lcbmhc {

            background-color: #ffffff;

        }

        .css-1vq4p4l {

            background-color: #ffffff;

        }

        

        /* Sidebar theme */

        .css-1d391kg .css-17eqqhr {

            background-color: #ffffff;

        }

        .css-1d391kg .css-1lcbmhc {

            color: #262730;

        }

        .css-1d391kg .css-1vq4p4l {

            background-color: #f0f2f6;

            border-color: #dfdfdf;

        }

    </style>

    """, unsafe_allow_html=True)

    

    # Custom CSS for styling and single section layout

    st.markdown("""

    <style>

        .main {

            background-color: #f0f2f6;

            padding-top: 0px !important;

            margin-top: 0px !important;

        }

        .stApp {

            background-color: #f0f2f6;

        }

        .block-container {

            padding-top: 0.5rem !important;

            padding-bottom: 0.5rem !important;

        }

        

        /* Hide header but keep sidebar button */

        .stAppHeader {

            background: transparent !important;

            border: none !important;

            box-shadow: none !important;

            height: 0 !important;

            overflow: visible !important;

        }

        

        .stAppToolbar {

            background: transparent !important;

            height: 0 !important;

            overflow: visible !important;

        }

        

        .stToolbarActions {

            display: none !important;

        }

        

        .stAppDeployButton {

            display: none !important;

        }

        

        /* Position sidebar button separately */

        button[data-testid="stExpandSidebarButton"] {

            position: fixed !important;

            top: 15px !important;

            left: 15px !important;

            z-index: 10002 !important;

            background: rgba(255, 255, 255, 0.9) !important;

            border: 1px solid rgba(0, 0, 0, 0.1) !important;

            border-radius: 8px !important;

            padding: 8px !important;

            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;

        }

        

        /* Increase date font size for better readability at 50% zoom */

        .date-section {

            font-size: 24px !important;

        }

        

        .date-section div:first-child {

            font-size: 28px !important;

            font-weight: 700 !important;

            line-height: 1.2 !important;

        }

        

        .date-section div:last-child {

            font-size: 16px !important;

            font-weight: 600 !important;

            margin-top: 4px !important;

        }

        

        .header-right div[style*="text-align: right"] div:first-child {

            font-size: 16px !important;

            font-weight: 600 !important;

        }

        

        .time-badge {

            font-size: 18px !important;

            font-weight: 600 !important;

        }

        

        /* Auto-refresh functionality */

        .auto-refresh-indicator {

            position: fixed !important;

            bottom: 20px !important;

            right: 20px !important;

            background: rgba(102, 126, 234, 0.9) !important;

            color: white !important;

            padding: 8px 12px !important;

            border-radius: 20px !important;

            font-size: 12px !important;

            font-weight: 500 !important;

            z-index: 9999 !important;

            display: flex !important;

            align-items: center !important;

            gap: 6px !important;

            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2) !important;

            pointer-events: none !important;

            margin: 0 !important;

        }

        

        .auto-refresh-active {

            background: rgba(16, 185, 129, 0.9) !important;

        }

        

        .refresh-spinner {

            width: 12px;

            height: 12px;

            border: 2px solid rgba(255, 255, 255, 0.3);

            border-top: 2px solid white;

            border-radius: 50%;

            animation: spin 1s linear infinite;

        }

        

        @keyframes spin {

            0% { transform: rotate(0deg); }

            100% { transform: rotate(360deg); }

        }

        

                .metric-card {

            background-color: white;

            padding: 25px;

            border-radius: 10px;

            box-shadow: 0 2px 4px rgba(0,0,0,0.1);

            margin-bottom: 15px;

            height: 100%;

            min-height: 140px;

            display: flex;

            align-items: center;

            justify-content: center;

        }

        .dashboard-container {

            background-color: white;

            border-radius: 15px;

            padding: 20px;

            box-shadow: 0 4px 6px rgba(0,0,0,0.1);

            margin-bottom: 20px;

        }

        .chart-container {

            background-color: white;

            border-radius: 10px;

            padding: 20px;

            box-shadow: 0 2px 4px rgba(0,0,0,0.1);

            margin-bottom: 20px;

        }

        /* Reduce spacing between elements */

        .element-container {

            margin-bottom: 0.5rem !important;

        }

        /* Make charts more compact */

        .js-plotly-plot .plotly {

            margin: 0 auto;

        }

        

        /* Print Styles - Landscape Mode */

        @media print {

            @page {

                size: A4 landscape;

                margin: 0.4in;

            }

            

            * {

                -webkit-print-color-adjust: exact !important;

                print-color-adjust: exact !important;

                box-sizing: border-box !important;

            }

            

            html, body {

                background-color: white !important;

                margin: 0 !important;

                padding: 0 !important;

                width: 100% !important;

                height: 100% !important;

                overflow: visible !important;

            }

            

            .main {

                background-color: white !important;

                padding: 0.5rem !important;

                max-width: 100% !important;

                width: 100% !important;

                overflow: visible !important;

            }

            

            .stApp {

                background-color: white !important;

                padding: 0 !important;

                width: 100% !important;

                overflow: visible !important;

            }

            

            .dashboard-container {

                background-color: white !important;

                box-shadow: none !important;

                border: none !important;

                padding: 15px !important;

                margin: 0 !important;

                page-break-inside: avoid;

                width: 100% !important;

                max-width: 100% !important;

                overflow: visible !important;

            }

            

            /* Force proper column layout in print */

            .stColumns {

                display: flex !important;

                flex-direction: row !important;

                width: 100% !important;

                gap: 15px !important;

                margin-bottom: 15px !important;

                page-break-inside: avoid;

                overflow: visible !important;

            }

            

            .stColumns > div {

                flex: 1 !important;

                min-width: 0 !important;

                padding: 5px !important;

                overflow: visible !important;

            }

            

            .chart-container {

                background-color: white !important;

                box-shadow: none !important;

                border: 1px solid #ddd !important;

                page-break-inside: avoid;

                margin-bottom: 15px !important;

                padding: 10px !important;

                width: 100% !important;

                overflow: visible !important;

                height: auto !important;

            }

            

            .metric-card {

                background-color: white !important;

                box-shadow: none !important;

                border: 1px solid #ddd !important;

                page-break-inside: avoid;

                margin-bottom: 10px !important;

                padding: 10px !important;

                width: 100% !important;

                height: auto !important;

                overflow: visible !important;

            }

            

            /* Hide streamlit elements when printing */

            .stDeployButton,

            .stMainMenu,

            .stSidebar,

            .stAlert,

            button:not(.print-button),

            .streamlit-container .element-container:has(button),

            footer,

            .element-container:has(.print-button) {

                display: none !important;

            }

            

            /* Ensure charts are properly sized and not cut */

            .js-plotly-plot {

                page-break-inside: avoid;

                width: 100% !important;

                height: 220px !important;

                min-height: 220px !important;

                overflow: visible !important;

            }

            

            .js-plotly-plot .plotly {

                width: 100% !important;

                height: 220px !important;

                min-height: 220px !important;

                overflow: visible !important;

            }

            

            .js-plotly-plot svg {

                width: 100% !important;

                height: 100% !important;

                overflow: visible !important;

            }

            

            /* Force proper spacing and prevent cutting */

            .element-container {

                margin-bottom: 5px !important;

                padding: 0 !important;

                overflow: visible !important;

                page-break-inside: avoid;

            }

            

            /* Text sizing for print */

            h1, h2, h3 {

                font-size: 16px !important;

                margin: 5px 0 !important;

                line-height: 1.2 !important;

            }

            

            .metric-card div {

                font-size: 11px !important;

                line-height: 1.2 !important;

            }

            

            .metric-card div[style*="font-size: 24px"] {

                font-size: 18px !important;

                line-height: 1.2 !important;

            }

            

            .metric-card div[style*="font-size: 30px"] {

                font-size: 22px !important;

                line-height: 1.2 !important;

            }

            

            /* Ensure no content is cut */

            * {

                overflow: visible !important;

            }

        }

        

        /* Print button styling */

        .print-button {

            background-color: #007bff;

            color: white;

            border: none;

            padding: 8px 16px;

            border-radius: 4px;

            cursor: pointer;

            font-size: 14px;

            margin: 10px 0;

        }

        

        .print-button:hover {

            background-color: #0056b3;

        }

        

        /* Enhanced logo animations */

        @keyframes shimmer {

            0% {

                transform: translateX(-100%) rotate(45deg);

                opacity: 0;

            }

            50% {

                opacity: 1;

            }

            100% {

                transform: translateX(200%) rotate(45deg);

                opacity: 0;

            }

        }

        

        @keyframes pulse {

            0%, 100% {

                transform: scale(1);

                opacity: 1;

            }

            50% {

                transform: scale(1.05);

                opacity: 0.8;

            }

        }

        

        .logo-container {

            position: relative;

            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);

        }

        

        .logo-container:hover {

            transform: translateY(-3px) scale(1.02);

        }

        

        .status-indicator {

            animation: pulse 2s infinite;

        }

        

        /* Responsive logo sizing */

        @media (max-width: 768px) {

            .logo-container img {

                width: 30px !important;

                height: 30px !important;

            }

            .logo-container > div:first-child {

                width: 40px !important;

                height: 40px !important;

            }

        }

        

        @media (max-width: 480px) {

            .logo-container img {

                width: 25px !important;

                height: 25px !important;

            }

            .logo-container > div:first-child {

                width: 35px !important;

                height: 35px !important;

            }

        }

        

        /* CSS-only hover effects for logo */

        .logo-container > div:first-child {

            transform: translateY(-1px);

            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);

        }

        

        .logo-container:hover > div:first-child {

            transform: translateY(-3px) scale(1.05);

            box-shadow: 0 12px 40px rgba(0,0,0,0.25), 0 4px 12px rgba(0,0,0,0.15) !important;

            background: linear-gradient(145deg, rgba(255,255,255,0.35), rgba(255,255,255,0.15)) !important;

        }

    </style>

    """, unsafe_allow_html=True)



    # Combined Header HTML and JavaScript in ONE st.markdown call to ensure same DOM context

    header_html = get_header_html(show_secret=True)

    

    # Display the original header without modal functionality

    st.markdown(header_html, unsafe_allow_html=True)

    

    # Check for data_check parameter for simple auto-refresh

    query_params = st.query_params

    if 'data_check' in query_params:

        # Return simple data count for change detection

        try:

            conn = database.sqlite3.connect('operation_dashboard.db')

            count = pd.read_sql_query("SELECT COUNT(*) as count FROM daily_data", conn).iloc[0]['count']

            conn.close()

            

            # Return minimal HTML with data count

            st.markdown(f'<div data-count="{count}" style="display:none;">{count}</div>', unsafe_allow_html=True)

            return

        except Exception as e:

            print(f"Error in data_check: {e}")

            st.markdown('<div data-count="0" style="display:none;">0</div>', unsafe_allow_html=True)

            return

    

    # Check for refresh_check parameter for simple auto-refresh

    if 'refresh_check' in query_params:

        # Return simple data count for change detection

        try:

            conn = database.sqlite3.connect('operation_dashboard.db')

            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM daily_data")

            count = cursor.fetchone()[0]

            conn.close()

            

            print(f"DEBUG: Data count for refresh_check: {count}")

            

            # Return just the count as plain text

            return str(count)

        except Exception as e:

            print(f"DEBUG: Error getting data count: {e}")

            return "0"

    

        

    # Auto-refresh for main dashboard only
    # Simple auto-refresh without UI indicator
    st.markdown('<meta http-equiv="refresh" content="30">', unsafe_allow_html=True)



    # Get current data count for debugging

    try:

        conn = database.sqlite3.connect('operation_dashboard.db')

        current_count = pd.read_sql_query("SELECT COUNT(*) as count FROM daily_data", conn).iloc[0]['count']

        conn.close()

        

        print(f"Current data count: {current_count}")

        

    except Exception as e:

        print(f"Data count check error: {e}")

        current_count = 0

    

    # Get data - ensure fresh data fetch

    try:

        # Force fresh data fetch

        conn = database.sqlite3.connect('operation_dashboard.db')

        latest_query = '''

            SELECT lake_elevation, peak_load, generation, gate_opening, date

            FROM daily_data 

            ORDER BY timestamp DESC, date DESC

            LIMIT 1

        '''

        latest_df = pd.read_sql_query(latest_query, conn)

        conn.close()

        

        if not latest_df.empty:

            latest_data = latest_df.iloc[0]

        else:

            latest_data = None

    except Exception as e:

        print(f"Error fetching latest data: {e}")

        latest_data = database.get_latest_data()

    

    previous_data = database.get_previous_data()



    # Keep monthly_summary in sync with daily_data (real-time monthly max values)

    try:

        database.upsert_monthly_summary_from_daily_data()

    except Exception as e:

        print(f"Monthly summary update error: {e}")



    if latest_data is None:

        st.error("No data available. Please run the database setup first.")

        return

    

    # Calculate percentage changes

    if previous_data is not None:

        lake_change = calculate_percentage_change(latest_data['lake_elevation'], previous_data['lake_elevation'])

        load_change = calculate_percentage_change(latest_data['peak_load'], previous_data['peak_load'])

        gate_change = calculate_percentage_change(latest_data['gate_opening'], previous_data['gate_opening'])

        generation_change = calculate_percentage_change(latest_data['generation'], previous_data['generation'])

        no_previous_data = False

    else:

        lake_change = load_change = gate_change = generation_change = 0

        no_previous_data = True

    

        

    # Main content layout

    # Row 1: Daily Data Graph + Monthly Comparison (side-by-side)

    st.markdown("""

    <style>

    .daily-data-card {

        background: #f3f4f6;

        border-radius: 16px;

        padding: 14px 14px 6px 14px;

        border: 1px solid rgba(0,0,0,0.08);

        width: 100%;

        margin: 0;

    }

    </style>

    """, unsafe_allow_html=True)



    left_chart_col, right_chart_col = st.columns(2)



    with left_chart_col:

        daily_chart = create_daily_data_chart()

        st.plotly_chart(daily_chart, use_container_width=True, config={'displayModeBar': False}, key="daily_data_graph")



    with right_chart_col:

        fig_monthly = create_monthly_comparison_chart()

        st.plotly_chart(fig_monthly, use_container_width=True, config={'displayModeBar': False}, key="monthly_chart")

    

    # Centered Real-time Metrics between top and bottom charts

    

    # Create full-width columns for metrics to match chart width

    col1, col2, col3, col4 = st.columns(4)

    

    if latest_data is None:

        # Show placeholder cards when no data

        with col1:

            st.markdown("""

            <div class="metric-card">

                <div style="display: flex; flex-direction: column; align-items: center; text-align: center; width: 100%;">

                    <div style="font-size: 16px; color: #666; margin-bottom: 8px;">Daily Lake Elevation</div>

                    <div style="font-size: 32px; font-weight: bold; color: #999; line-height: 1.2;">--</div>

                    <div style="font-size: 18px; color: #999; margin-top: 5px;">

                        No data

                    </div>

                </div>

            </div>

            """, unsafe_allow_html=True)

        

        with col2:

            st.markdown("""

            <div class="metric-card">

                <div style="display: flex; flex-direction: column; align-items: center; text-align: center; width: 100%;">

                    <div style="font-size: 16px; color: #666; margin-bottom: 8px;">Daily Peak Load</div>

                    <div style="font-size: 32px; font-weight: bold; color: #999; line-height: 1.2;">--</div>

                    <div style="font-size: 18px; color: #999; margin-top: 5px;">

                        No data

                    </div>

                </div>

            </div>

            """, unsafe_allow_html=True)

        

        with col3:

            st.markdown("""

            <div class="metric-card">

                <div style="display: flex; flex-direction: column; align-items: center; text-align: center; width: 100%;">

                    <div style="font-size: 16px; color: #666; margin-bottom: 8px;">Daily Gate Opening</div>

                    <div style="font-size: 32px; font-weight: bold; color: #999; line-height: 1.2;">--</div>

                    <div style="font-size: 18px; color: #999; margin-top: 5px;">

                        No data

                    </div>

                </div>

            </div>

            """, unsafe_allow_html=True)

        

        with col4:

            st.markdown("""

            <div class="metric-card">

                <div style="display: flex; flex-direction: column; align-items: center; text-align: center; width: 100%;">

                    <div style="font-size: 16px; color: #666; margin-bottom: 8px;">Daily Generation</div>

                    <div style="font-size: 32px; font-weight: bold; color: #999; line-height: 1.2;">--</div>

                    <div style="font-size: 18px; color: #999; margin-top: 5px;">

                        No data

                    </div>

                </div>

            </div>

            """, unsafe_allow_html=True)

    else:

        # Show actual data when available

        with col1:

            create_metric_card(

                "Daily Lake Elevation",

                f"{latest_data['lake_elevation']:.2f}",

                lake_change,

                "💧",

                "m",

                show_no_data=no_previous_data

            )

        

        with col2:

            create_metric_card(

                "Daily Peak Load",

                f"{latest_data['peak_load']:.2f}",

                load_change,

                "⚡",

                "kWh",

                show_no_data=no_previous_data

            )

        

        with col3:

            create_metric_card(

                "Daily Gate Opening",

                f"{latest_data['gate_opening']:.2f}",

                gate_change,

                "🚪",

                "m",

                show_no_data=no_previous_data

            )

        

        with col4:

            create_metric_card(

                "Daily Generation",

                f"{latest_data['generation']:.2f}",

                generation_change,

                "⚙️",

                "kWh",

                show_no_data=no_previous_data

            )

    

    # Row 3: Current Month Gate Opening + Multi Chart

    col1, col2 = st.columns(2)

    

    with col1:

        fig_current_gate = create_current_month_gate_chart()

        st.plotly_chart(fig_current_gate, use_container_width=True, config={'displayModeBar': False}, key="current_month_gate_chart")

    

    with col2:

        fig_current_month_multi = create_current_month_multi_chart()

        st.plotly_chart(fig_current_month_multi, use_container_width=True, config={'displayModeBar': False}, key="current_month_multi_chart")

    

    # Footer - Navigation buttons removed as sidebar menu is now available



if __name__ == "__main__":

    main()

