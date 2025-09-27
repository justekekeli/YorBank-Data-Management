import os
import psycopg2
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Access environment variables
DB_HOST = os.getenv("PG_HOST")
DB_PORT = os.getenv("PG_PORT")
DB_NAME = os.getenv("PG_NAME")
DB_USER = os.getenv("PG_USER")
DB_PASSWORD = os.getenv("PG_PASSWORD")

def connectToSourceDB():
    conn = None
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        print("Connection successful.")
    except Exception as e:
        print("Connection failed:", e)

    return conn

def close_connection(connection):
    if type(connection)!=None:
        connection.close()

def test_connection():
   conn= connectToSourceDB()
   close_connection(conn)


if __name__ == "__main__":
    test_connection()