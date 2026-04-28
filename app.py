import os
import streamlit as st
import database
import dashboard

# Initialize database for cloud deployment
try:
    if os.path.exists('/mount/data'):
        # We're on Streamlit Cloud - initialize database with sample data
        database.initialize_cloud_database()
        st.sidebar.success("✅ Database initialized for cloud deployment")
except Exception as e:
    st.sidebar.error(f"⚠️ Database initialization: {str(e)}")

# Main entry point for Streamlit Cloud deployment
if __name__ == "__main__":
    dashboard.main()
