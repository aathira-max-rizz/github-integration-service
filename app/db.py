import psycopg2

DB_URL = "postgresql://postgres:oscowlaivathsalya@db.biltlkxalucjmijkemjj.supabase.co:5432/postgres"

def get_connection():
    conn = psycopg2.connect(DB_URL)

    # create table automatically
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS github_tokens (
            id SERIAL PRIMARY KEY,
            token TEXT
        );
    """)
    conn.commit()
    cur.close()

    return conn