import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import random
import os
import streamlit as st

def get_database_path():
    """Get the appropriate database path for local or cloud deployment"""
    # For Streamlit Cloud, use /mount/data/ which is writable
    if os.path.exists('/mount/data'):
        return '/mount/data/operation_dashboard.db'
    else:
        return 'operation_dashboard.db'

def create_database():
    """Create SQLite database and tables for the operation dashboard"""
    db_path = get_database_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create daily_data table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE NOT NULL,
            lake_elevation REAL,
            peak_load REAL,
            generation REAL,
            gate_opening REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create monthly_summary table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS monthly_summary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            month TEXT NOT NULL,
            year INTEGER NOT NULL,
            max_lake_elevation REAL,
            max_peak_load REAL,
            avg_generation REAL,
            total_generation REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def insert_sample_monthly_summary():
    """Insert removable sample monthly summary rows (Jan/Feb).

    Samples are tagged with year=9999 so they can be deleted safely without touching real data.
    """
    db_path = get_database_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    sample_year = 9999

    cursor.execute(
        "SELECT COUNT(*) FROM monthly_summary WHERE year = ? AND month IN ('Jan', 'Feb')",
        (sample_year,),
    )
    existing = cursor.fetchone()[0]
    if existing >= 2:
        conn.close()
        return

    def rand(a, b):
        return round(random.uniform(a, b), 1)

    samples = [
        ('Jan', sample_year, rand(690, 710), rand(2400, 3100), rand(350, 650), rand(10000, 20000)),
        ('Feb', sample_year, rand(690, 710), rand(2400, 3100), rand(350, 650), rand(10000, 20000)),
    ]

    cursor.executemany(
        '''
        INSERT INTO monthly_summary (month, year, max_lake_elevation, max_peak_load, avg_generation, total_generation)
        VALUES (?, ?, ?, ?, ?, ?)
        ''',
        samples,
    )

    conn.commit()
    conn.close()

def remove_sample_monthly_summary():
    """Remove previously inserted sample monthly summary rows."""
    db_path = get_database_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM monthly_summary WHERE year = 9999")
    conn.commit()
    conn.close()

def upsert_monthly_summary_from_daily_data(year=None):
    """Upsert monthly_summary using aggregated values from daily_data.

    - Computes max_lake_elevation and max_peak_load per month.
    - Writes results into monthly_summary for the selected year.
    - Does not touch removable sample rows (year=9999).
    """
    db_path = get_database_path()
    conn = sqlite3.connect(db_path)

    if year is None:
        year = datetime.now().year

    query = '''
        SELECT
            substr(date, 1, 4) AS year,
            substr(date, 6, 2) AS month_num,
            MAX(lake_elevation) AS max_lake_elevation,
            MAX(peak_load) AS max_peak_load
        FROM daily_data
        WHERE substr(date, 1, 4) = ?
        GROUP BY substr(date, 1, 4), substr(date, 6, 2)
    '''

    df = pd.read_sql_query(query, conn, params=(str(year),))
    if df.empty:
        conn.close()
        return

    month_map = {
        '01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr',
        '05': 'May', '06': 'Jun', '07': 'Jul', '08': 'Aug',
        '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'
    }

    cursor = conn.cursor()
    for _, row in df.iterrows():
        month = month_map.get(str(row['month_num']).zfill(2))
        if not month:
            continue
        cursor.execute(
            "SELECT id FROM monthly_summary WHERE year = ? AND month = ?",
            (int(year), month),
        )
        existing = cursor.fetchone()
        if existing:
            cursor.execute(
                "UPDATE monthly_summary SET max_lake_elevation = ?, max_peak_load = ? WHERE id = ?",
                (row['max_lake_elevation'], row['max_peak_load'], existing[0]),
            )
        else:
            cursor.execute(
                """
                INSERT INTO monthly_summary (month, year, max_lake_elevation, max_peak_load, avg_generation, total_generation)
                VALUES (?, ?, ?, ?, NULL, NULL)
                """,
                (month, int(year), row['max_lake_elevation'], row['max_peak_load']),
            )

    conn.commit()
    conn.close()

def insert_daily_data(date, lake_elevation, peak_load, generation, gate_opening):
    """Insert daily data into the database"""
    db_path = get_database_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO daily_data (date, lake_elevation, peak_load, generation, gate_opening)
        VALUES (?, ?, ?, ?, ?)
    ''', (date, lake_elevation, peak_load, generation, gate_opening))
    
    conn.commit()
    conn.close()

def insert_monthly_summary(month, year, max_lake_elevation, max_peak_load, avg_generation, total_generation):
    """Insert monthly summary into the database"""
    db_path = get_database_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO monthly_summary (month, year, max_lake_elevation, max_peak_load, avg_generation, total_generation)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (month, year, max_lake_elevation, max_peak_load, avg_generation, total_generation))
    
    conn.commit()
    conn.close()

def get_latest_data():
    """Get the latest daily data"""
    db_path = get_database_path()
    conn = sqlite3.connect(db_path)
    
    query = '''
        SELECT lake_elevation, peak_load, generation, gate_opening, date
        FROM daily_data 
        ORDER BY timestamp DESC, date DESC
        LIMIT 1
    '''
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    if df.empty:
        return None
    return df.iloc[0]

def get_previous_data():
    """Get the previous day's data for comparison"""
    db_path = get_database_path()
    conn = sqlite3.connect(db_path)
    
    query = '''
        SELECT lake_elevation, peak_load, generation, gate_opening, date
        FROM daily_data 
        ORDER BY timestamp DESC, date DESC
        LIMIT 1 OFFSET 1
    '''
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    if df.empty:
        return None
    return df.iloc[0]

def get_monthly_data(year=2025, include_samples=True):
    """Get monthly summary data for a given year.

    If include_samples is True, also includes removable sample rows (year=9999).
    """
    db_path = get_database_path()
    conn = sqlite3.connect(db_path)

    if include_samples:
        query = '''
            SELECT month, max_lake_elevation, max_peak_load
            FROM monthly_summary 
            WHERE year = ? OR year = 9999
        '''
        df = pd.read_sql_query(query, conn, params=(year,))
    else:
        query = '''
            SELECT month, max_lake_elevation, max_peak_load
            FROM monthly_summary 
            WHERE year = ?
        '''
        df = pd.read_sql_query(query, conn, params=(year,))
    conn.close()

    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    if df.empty:
        return pd.DataFrame({
            'month': month_order,
            'max_lake_elevation': [None] * 12,
            'max_peak_load': [None] * 12,
        })

    df['month'] = pd.Categorical(df['month'], categories=month_order, ordered=True)
    df = df.sort_values('month')

    # Ensure all months (Jan-Dec) exist even when data is missing.
    df = df.set_index('month').reindex(month_order).reset_index()
    return df

def get_april_daily_data():
    """Get daily data for April - gets latest entry per day"""
    db_path = get_database_path()
    conn = sqlite3.connect(db_path)
    
    query = '''
        SELECT d1.date, 
               d1.lake_elevation, 
               d1.peak_load, 
               d1.generation,
               d1.gate_opening
        FROM daily_data d1
        INNER JOIN (
            SELECT date, MAX(timestamp) as max_timestamp
            FROM daily_data 
            WHERE date LIKE '%-04-%'
            GROUP BY date
        ) d2 ON d1.date = d2.date AND d1.timestamp = d2.max_timestamp
        WHERE d1.date LIKE '%-04-%'
        ORDER BY d1.date
    '''
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    return df

def get_daily_data_for_chart(days=30):
    """Get daily data for the last N days - gets latest entry per date"""
    db_path = get_database_path()
    conn = sqlite3.connect(db_path)
    
    query = '''
        SELECT d1.date, 
               d1.lake_elevation, 
               d1.peak_load, 
               d1.generation
        FROM daily_data d1
        INNER JOIN (
            SELECT date, MAX(timestamp) as max_timestamp
            FROM daily_data 
            GROUP BY date
            ORDER BY date DESC 
            LIMIT ?
        ) d2 ON d1.date = d2.date AND d1.timestamp = d2.max_timestamp
        ORDER BY d1.date DESC
    '''
    
    df = pd.read_sql_query(query, conn, params=(days,))
    conn.close()
    
    return df.sort_values('date')

def clear_all_data():
    """Clear all existing data from the database"""
    db_path = get_database_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM daily_data')
    cursor.execute('DELETE FROM monthly_summary')
    conn.commit()
    conn.close()

def remove_sample_daily_data():
    """Remove any sample daily data entries."""
    db_path = get_database_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Remove any sample data that might have specific patterns
    cursor.execute("DELETE FROM daily_data WHERE date LIKE '9999-%'")
    cursor.execute("DELETE FROM daily_data WHERE date LIKE '2025-01-%' AND lake_elevation BETWEEN 690 AND 710 AND peak_load BETWEEN 2400 AND 3100")
    conn.commit()
    conn.close()

def initialize_cloud_database():
    """Initialize database with sample data for cloud deployment"""
    # Create database and tables
    create_database()
    
    # Insert sample data for demonstration
    insert_sample_operational_data()
    insert_sample_monthly_summary()

def insert_sample_operational_data():
    """Insert realistic sample operational data for March and April 2025"""
    db_path = get_database_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Sample March 2025 data (realistic operational values)
    march_data = [
        ('2025-03-01', 456.78, 2845.50, 3420.25, 3.45),
        ('2025-03-05', 457.12, 2910.75, 3485.60, 3.52),
        ('2025-03-10', 455.89, 2765.30, 3290.15, 3.38),
        ('2025-03-15', 458.34, 3050.20, 3650.80, 3.67),
        ('2025-03-20', 456.91, 2880.45, 3456.70, 3.48),
        ('2025-03-25', 457.56, 2955.80, 3546.90, 3.58),
        ('2025-03-31', 458.02, 3020.15, 3624.30, 3.63),
    ]
    
    # Sample April 2025 data (current month)
    april_data = [
        ('2025-04-02', 457.23, 2875.60, 3450.75, 3.50),
        ('2025-04-05', 456.87, 2790.35, 3348.40, 3.41),
        ('2025-04-06', 457.45, 2915.20, 3498.25, 3.55),
    ]
    
    # Insert March data
    cursor.executemany('''
        INSERT INTO daily_data (date, lake_elevation, peak_load, generation, gate_opening)
        VALUES (?, ?, ?, ?, ?)
    ''', march_data)
    
    # Insert April data
    cursor.executemany('''
        INSERT INTO daily_data (date, lake_elevation, peak_load, generation, gate_opening)
        VALUES (?, ?, ?, ?, ?)
    ''', april_data)
    
    # Insert monthly summary for March
    cursor.execute('''
        INSERT INTO monthly_summary (month, year, max_lake_elevation, max_peak_load, avg_generation, total_generation)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ('Mar', 2025, 458.34, 3050.20, 3495.28, 108353.60))
    
    conn.commit()
    conn.close()
    print("Sample operational data inserted successfully!")

if __name__ == "__main__":
    create_database()
    print("Database setup completed. Your existing data is preserved!")
