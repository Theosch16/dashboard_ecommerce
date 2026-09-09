import pandas as pd
import psycopg2
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CLEANED_DATA = BASE_DIR / "data" / "cleaned_data"

conn = psycopg2.connect(
    database=os.getenv('POSTGRES_DB'),
    user=os.getenv('POSTGRES_USER'),
    password=os.getenv('POSTGRES_PASSWORD'),
    host="database",
    port="5432"
)

cursor = conn.cursor()

# with open(CLEANED_DATA / "geolocation_dataset.csv", "r", encoding="utf-8") as file:
#     cursor.copy_expert(
#         """
#         COPY dashboard_localisation (
#             zip_code,
#             latitude,
#             longitude,
#             state,
#             city
#         )
#         FROM STDIN
#         WITH CSV HEADER
#         """,
#         file,
#     )

# # Insert product data

# with open(CLEANED_DATA / "product_dataset.csv", "r", encoding="utf-8") as file:
#     cursor.copy_expert(
#         """
#         COPY dashboard_product (
#             product_name,
#             product_category_name
#         )
#         FROM STDIN
#         WITH CSV HEADER
#         """,
#         file,
#     )

# # Insert customers data

# cursor.execute("""
#     CREATE TEMP TABLE staging_customer (
#         customer_name VARCHAR(32),
#         customer_unique_id VARCHAR(32),
#         customer_zip_code_prefix VARCHAR(5)
#     );
# """)

# with open(CLEANED_DATA / "customers_dataset.csv", "r", encoding="utf-8") as file:
#     cursor.copy_expert("""
#         COPY staging_customer (
#             customer_name,
#             customer_unique_id,
#             customer_zip_code_prefix
#         )
#         FROM STDIN
#         WITH CSV HEADER
#     """, file)

# cursor.execute("""
#     INSERT INTO dashboard_customer (
#         customer_name,
#         customer_unique_id,
#         localisation_id
#     )
#     SELECT
#         s.customer_name,
#         s.customer_unique_id,
#         l.id
#     FROM staging_customer s
#     JOIN dashboard_localisation l
#         ON s.customer_zip_code_prefix = l.zip_code;
# """)

# # Insert sellers data

# cursor.execute("""
#     CREATE TEMP TABLE staging_seller (
#         seller_name VARCHAR(32),
#         seller_zip_code_prefix VARCHAR(5)
#     );
# """)

# with open(CLEANED_DATA / "sellers_dataset.csv", "r", encoding="utf-8") as file:
#     cursor.copy_expert("""
#         COPY staging_seller (
#             seller_name,
#             seller_zip_code_prefix
#         )
#         FROM STDIN
#         WITH CSV HEADER
#     """, file)

# cursor.execute("""
#     INSERT INTO dashboard_seller (
#         seller_name,
#         localisation_id
#     )
#     SELECT
#         s.seller_name,
#         l.id
#     FROM staging_seller s
#     JOIN dashboard_localisation l
#         ON s.seller_zip_code_prefix = l.zip_code;
# """)

# # Insert orders data

# cursor.execute("""
#     CREATE TEMP TABLE staging_orders (
#         order_name VARCHAR(32),
#         customer_name VARCHAR(32),
#         order_status VARCHAR(32),
#         order_purchase_timestamp TIMESTAMPTZ,
#         order_delivered_carrier_date TIMESTAMPTZ,
#         order_delivered_customer_date TIMESTAMPTZ,
#         order_estimated_delivery_date TIMESTAMPTZ,
#         order_review INTEGER
#     );
# """)

# with open(CLEANED_DATA / "order_dataset.csv", "r", encoding="utf-8") as file:
#     cursor.copy_expert("""
#         COPY staging_orders (
#             order_name,
#             customer_name,
#             order_status,
#             order_purchase_timestamp,
#             order_delivered_carrier_date,
#             order_delivered_customer_date,
#             order_estimated_delivery_date,
#             order_review
#         )
#         FROM STDIN
#         WITH CSV HEADER
#     """, file)

# cursor.execute("""
#     INSERT INTO dashboard_order (
#         order_name,
#         customer_id,
#         order_status,
#         order_purchase_timestamp,
#         order_delivered_carrier_date,
#         order_delivered_customer_date,
#         order_estimated_delivery_date,
#         order_review
#     )
#     SELECT
#         s.order_name,
#         c.id,
#         s.order_status,
#         s.order_purchase_timestamp,
#         s.order_delivered_carrier_date,
#         s.order_delivered_customer_date,
#         s.order_estimated_delivery_date,
#         s.order_review
#     FROM staging_orders s
#     JOIN dashboard_customer c
#         ON s.customer_name = c.customer_name;
# """)



# # Insert orders_payment data

# cursor.execute("""
#     CREATE TEMP TABLE staging_orders_payment (
#         order_name VARCHAR(32),
#         payment_sequential INTEGER,
#         payment_type VARCHAR(12),
#         payment_installments INTEGER,
#         payment_value DECIMAL(9,2)
#     );
# """)

# with open(CLEANED_DATA / "order_payment_dataset.csv", "r", encoding="utf-8") as file:
#     cursor.copy_expert("""
#         COPY staging_orders_payment (
#             order_name,
#             payment_sequential,
#             payment_type,
#             payment_installments,
#             payment_value
#         )
#         FROM STDIN
#         WITH CSV HEADER
#     """, file)

# cursor.execute("""
#     INSERT INTO dashboard_orderpayment (
#         order_id,
#         payment_sequential,
#         payment_type,
#         payment_installments,
#         payment_value
#     )
#     SELECT
#         o.id,
#         p.payment_sequential,
#         p.payment_type,
#         p.payment_installments,
#         p.payment_value
#     FROM staging_orders_payment p
#     JOIN dashboard_order o
#         ON p.order_name = o.order_name;
# """)

## Insert orders_item data

cursor.execute("""
    CREATE TEMP TABLE staging_orders_items (
        order_id VARCHAR(32),
        order_item_name VARCHAR(32),
        product_id VARCHAR(32),
        seller_id VARCHAR(32),
        price DECIMAL(9,2)
    );
""")

with open(CLEANED_DATA / "order_item_dataset.csv", "r", encoding="utf-8") as file:
    cursor.copy_expert("""
        COPY staging_orders_items (
            order_id,
            order_item_name,
            product_id,
            seller_id,
            price
        )
        FROM STDIN
        WITH CSV HEADER
    """, file)

cursor.execute("""
    INSERT INTO dashboard_orderitem (
        order_id,
        order_item_name,
        product_id,
        seller_id,
        price
    )
    SELECT
        o.id,
        i.order_item_name,
        p.id,
        s.id,
        i.price
    FROM staging_orders_items i
    JOIN dashboard_order o
        ON i.order_id = o.order_name
    JOIN dashboard_seller s
        ON i.seller_id = s.seller_name
    JOIN dashboard_product p
        ON i.product_id = p.product_name;
""")

conn.commit()
cursor.close()
conn.close()