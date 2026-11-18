import sqlite3
import os

def seed_db():
    db_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(db_dir, "company_metrics.db")
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS metrics 
                 (metric_name TEXT, recorded_value TEXT, last_updated TEXT)''')
    c.execute("DELETE FROM metrics")
    
    data = [
        ("Q3 Churn Rate", "7.2%", "2025-10-31"),
        ("SLA Uptime", "99.1%", "2025-10-31"),
        ("Customer Reliability Budget", "$40,000", "2025-10-16"),
        ("Q3 Revenue", "$4.2M", "2025-10-15")
    ]
    
    c.executemany("INSERT INTO metrics VALUES (?,?,?)", data)
    conn.commit()
    conn.close()
    print(f"Database seeded successfully at {db_path}")

if __name__ == "__main__":
    seed_db()