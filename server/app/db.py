import os
import psycopg2
from psycopg2.extras import RealDictCursor
from urllib.parse import urlparse

def get_db_connection():
    """Get PostgreSQL database connection."""
    database_url = os.getenv("DATABASE_URL") or os.getenv("POSTGRES_URL")
    
    if database_url:
        # Parse the DATABASE_URL
        result = urlparse(database_url)
        return psycopg2.connect(
            host=result.hostname,
            port=result.port or 5432,
            user=result.username,
            password=result.password,
            database=result.path[1:],  # Remove leading '/'
            sslmode='require',
            cursor_factory=RealDictCursor
        )
    else:
        # Fallback to individual env vars (local dev with MySQL-style vars)
        return psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", 5432)),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "neondb"),
            cursor_factory=RealDictCursor
        )
