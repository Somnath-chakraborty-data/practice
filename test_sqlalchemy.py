from sqlalchemy import create_engine, text

# change user, password, and dbname as per your PostgreSQL setup
engine = create_engine("postgresql+psycopg2://postgres:yourpassword@localhost:5432/postgres")

with engine.connect() as conn:
    result = conn.execute(text("SELECT version();"))
    print("PostgreSQL version:", result.scalar())
