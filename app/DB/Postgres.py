import psycopg2
from Constants.config import DB_CONFIG

def get_connection():
    """
    Returns a new PostgreSQL connection.
    Use cursor() on the returned connection.
    """
    return psycopg2.connect(
        host=DB_CONFIG["host"],
        database=DB_CONFIG["database"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        port=DB_CONFIG["port"]
    )


def fetch_all(query: str, params=None):
    """
    Utility function to fetch all rows.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def execute(query: str, params=None):
    """
    Utility function for INSERT / UPDATE / DELETE.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()
    cur.close()
    conn.close()
