import os
import streamlit as st
import database
import dashboard

# Initialize database for cloud deployment
if os.path.exists('/mount/data'):
    # We're on Streamlit Cloud - initialize database with sample data
    database.initialize_cloud_database()

# Main entry point for Streamlit Cloud deployment
if __name__ == "__main__":
    dashboard.main()
