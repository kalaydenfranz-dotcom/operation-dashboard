import streamlit as st
import pandas as pd
from datetime import datetime, date
import database

def main():
    # Page configuration
    st.set_page_config(
        page_title="Data Input - Operation Dashboard",
        page_icon="📝",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    # Custom CSS for styling
    st.markdown("""
    <style>
        .main {
            background-color: #f0f2f6;
        }
        .stApp {
            background-color: #f0f2f6;
        }
        .input-card {
            background-color: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .success-message {
            background-color: #d4edda;
            color: #155724;
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #c3e6cb;
            margin-bottom: 20px;
        }
        .error-message {
            background-color: #f8d7da;
            color: #721c24;
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #f5c6cb;
            margin-bottom: 20px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="color: #2c3e50; margin-bottom: 10px;">📝 Data Input Page</h1>
        <p style="color: #7f8c8d;">Enter daily operation data for the tracking system</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📊 View Dashboard", use_container_width=True):
            st.switch_page("main.py")
    
    # Initialize session state for success messages
    if 'success_message' not in st.session_state:
        st.session_state.success_message = None
    if 'error_message' not in st.session_state:
        st.session_state.error_message = None
    
    # Display messages
    if st.session_state.success_message:
        st.markdown(f"""
        <div class="success-message">
            ✅ {st.session_state.success_message}
        </div>
        """, unsafe_allow_html=True)
        st.session_state.success_message = None
    
    if st.session_state.error_message:
        st.markdown(f"""
        <div class="error-message">
            ❌ {st.session_state.error_message}
        </div>
        """, unsafe_allow_html=True)
        st.session_state.error_message = None
    
    # Data Input Form
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    
    st.markdown("### 📅 Enter Daily Data")
    st.markdown("---")
    
    with st.form("data_input_form"):
        # Date selection
        col1, col2 = st.columns(2)
        with col1:
            selected_date = st.date_input(
                "Date",
                value=date.today(),
                max_value=date.today(),
                help="Select the date for this data entry"
            )
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            st.info(f"Current system time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Input fields
        st.markdown("#### 📊 Measurements")
        
        col1, col2 = st.columns(2)
        
        with col1:
            lake_elevation = st.number_input(
                "Lake Elevation",
                min_value=0.0,
                max_value=1000.0,
                value=700.0,
                step=0.01,
                help="Lake elevation in meters"
            )
            
            peak_load = st.number_input(
                "Peak Load",
                min_value=0.0,
                max_value=5000.0,
                value=2500.0,
                step=0.01,
                help="Peak load in MW"
            )
        
        with col2:
            generation = st.number_input(
                "Generation",
                min_value=0.0,
                max_value=2000.0,
                value=500.0,
                step=0.01,
                help="Power generation in MW"
            )
            
            gate_opening = st.number_input(
                "Gate Opening",
                min_value=0.0,
                max_value=10.0,
                value=2.0,
                step=0.01,
                help="Gate opening in meters"
            )
        
        # Form submission
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button(
                "💾 Save Data",
                use_container_width=True,
                type="primary"
            )
        
        if submit_button:
            try:
                # Insert data into database
                database.insert_daily_data(
                    selected_date.strftime('%Y-%m-%d'),
                    lake_elevation,
                    peak_load,
                    generation,
                    gate_opening
                )
                
                st.session_state.success_message = f"Data successfully saved for {selected_date.strftime('%Y-%m-%d')}"
                st.rerun()
                
            except Exception as e:
                st.session_state.error_message = f"Error saving data: {str(e)}"
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Recent Data Display
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    st.markdown("### 📋 Recent Data Entries")
    st.markdown("---")
    
    try:
        # Get recent data
        conn = database.sqlite3.connect('operation_dashboard.db')
        query = '''
            SELECT date, lake_elevation, peak_load, generation, gate_opening, timestamp
            FROM daily_data 
            ORDER BY date DESC, timestamp DESC 
            LIMIT 10
        '''
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if not df.empty:
            # Format the data for display
            display_df = df.copy()
            display_df['date'] = pd.to_datetime(display_df['date']).dt.strftime('%Y-%m-%d')
            display_df['timestamp'] = pd.to_datetime(display_df['timestamp']).dt.strftime('%H:%M:%S')
            display_df.columns = ['Date', 'Lake Elevation', 'Peak Load', 'Generation', 'Gate Opening', 'Time']
            
            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Lake Elevation": st.column_config.NumberColumn(format="%.2f m"),
                    "Peak Load": st.column_config.NumberColumn(format="%.2f MW"),
                    "Generation": st.column_config.NumberColumn(format="%.2f MW"),
                    "Gate Opening": st.column_config.NumberColumn(format="%.2f m")
                }
            )
        else:
            st.info("No data entries found. Start by adding your first entry above!")
            
    except Exception as e:
        st.error(f"Error loading recent data: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick Actions
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    st.markdown("### ⚡ Quick Actions")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.rerun()
    
    with col2:
        if st.button("📊 View Dashboard", use_container_width=True):
            st.switch_page("main.py")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div style="text-align: center; margin-top: 30px; padding: 20px; color: #7f8c8d;">
        <p>💡 <strong>Tip:</strong> This input page is designed for data entry. Use the Dashboard page for viewing analytics.</p>
        <p style="font-size: 12px; margin-top: 10px;">Last updated: {}</p>
    </div>
    """.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
