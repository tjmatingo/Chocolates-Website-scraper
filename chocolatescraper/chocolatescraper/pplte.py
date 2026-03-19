import psycopg2

conn = psycopg2.connect(host="localhost", dbname="chocolate_scraper", user="postgres", password="12345678", port=5432)

curr = conn.cursor()

curr.execute("""
CREATE TABLE IF NOT EXISTS chocolate_products(
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    price DECIMAL(10, 2) NOT NULL, 
    url VARCHAR(500)
);
""")

conn.commit()

curr.close()
conn.close()