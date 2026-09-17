import pandas as pd
import geopandas as gpd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA = BASE_DIR / "data" / "raw_data"
CLEANED_DATA = BASE_DIR / "data" / "cleaned_data"

## Cleaning order_list.csv and order_reviews.csv

def clean_order():
    # Remove all unnecessary data from dataframe such as the order_approved_at column.
    df_order=pd.read_csv(RAW_DATA / "olist_orders_dataset.csv")
    df_order = df_order.drop(columns=['order_approved_at'])

    # Change types of columns
    columns_to_change=[
        'order_estimated_delivery_date',
        'order_delivered_customer_date',
        'order_delivered_carrier_date',
        'order_purchase_timestamp'
    ]
    df_order[columns_to_change]=df_order[columns_to_change].apply(pd.to_datetime)

    ## ------ order_reviews.csv
    df_order_review=pd.read_csv("data/raw_data/olist_order_reviews_dataset.csv")
    df_order_review = df_order_review.drop(columns=['review_id', 'review_comment_title','review_comment_message','review_creation_date','review_answer_timestamp'])
    df_order=df_order.merge(df_order_review, left_on= "order_id", right_on="order_id", how="left")
    df_order["review_score"]=df_order["review_score"].astype("Int64")
    df_order.to_csv(CLEANED_DATA / "order_dataset.csv", index=None)

# Cleaning customers.csv

def clean_customers():
    df_customers=pd.read_csv(RAW_DATA / "olist_customers_dataset.csv")

    # Remove all unecessary data from dataframe
    df_customers = df_customers.drop(columns=['customer_city', 'customer_state'])

    # Correct zip_code
    df_customers['customer_zip_code_prefix'] = df_customers['customer_zip_code_prefix'].astype(str).str.zfill(5)
    df_customers.to_csv(CLEANED_DATA / "customers_dataset.csv", index=None)

## Cleaning Order_geolocation_dataset.csv
def clean_geolocation():
    df_geolocation=pd.read_csv(RAW_DATA / "olist_geolocation_dataset.csv")

    # Correct zip_code by giving them minimum 5 digits
    df_geolocation['geolocation_zip_code_prefix'] = df_geolocation['geolocation_zip_code_prefix'].astype(str).str.zfill(5)

    # Remove all duplicates values
    df_geolocation=df_geolocation.drop_duplicates(['geolocation_zip_code_prefix', 'geolocation_city','geolocation_state'])

    # Loading another files with geopandas to have the correct naming of cities
    towns = gpd.read_file(
        RAW_DATA/"BR_Municipios_2024.zip"
    )

    # Using our coordinates to do a join with the correct coordinates style
    points = gpd.GeoDataFrame(
        df_geolocation,
        geometry=gpd.points_from_xy(
            df_geolocation["geolocation_lng"],
            df_geolocation["geolocation_lat"]
        ),
        crs="EPSG:4326"
    )

    df_geolocation = gpd.sjoin(
        points,
        towns[["NM_MUN", "geometry"]],
        how="left",
        predicate="within"
    )

    df_geolocation = df_geolocation.drop(columns=['geolocation_city', 'geometry', 'index_right'])

    df_geolocation = df_geolocation.rename(columns={
        "NM_MUN": "geolocation_city"
    })

    # Adding the remaining dozen towns left that are missing
    missing_names={
        "18243":"Bom Retiro da Esperança",
        "28165":"Vila Nova de Campos",
        "28155":"Santa Maria",
        "29654":"Santo Antônio do Canaã",
        "35179":"Santana do Paraíso",
        "57319":"Pau-d'Arco",
        "58441":"São José da Mata",
        "68275":"Porto Trombetas",
        "68447":"Vila dos Cabanos",
        "78131":"Várzea Grande",
        "83252":"Ilha dos Valadares",
        "83810":"Areia Branca dos Assis",
        "95130":"Santa Lúcia do Piaí",
        "98780":"Santa Rosa"
    }

    for zip_code, city in missing_names.items():
        df_geolocation.loc[df_geolocation['geolocation_zip_code_prefix'] == zip_code, 'geolocation_city']=city
    df_geolocation.to_csv(CLEANED_DATA / "geolocation_dataset.csv", index=None)

## Cleaning order_items.csv

def clean_order_item():
    df_order_item=pd.read_csv(RAW_DATA / "olist_order_items_dataset.csv")
    df_order_item = df_order_item.drop(columns=['shipping_limit_date', 'freight_value'])
    df_order_item.to_csv(CLEANED_DATA/ "order_item_dataset.csv", index=None)

## Cleaning order_payment.csv

def clean_order_payment():
    df_order_payment=pd.read_csv(RAW_DATA / "olist_order_payments_dataset.csv")
    df_order_payment.to_csv(CLEANED_DATA / "order_payment_dataset.csv", index=None)

## Cleaning products.csv

def clean_product():
    df_product=pd.read_csv(RAW_DATA / "olist_products_dataset.csv")
    df_product = df_product.drop(columns=['product_name_lenght', 'product_description_lenght','product_photos_qty','product_weight_g','product_length_cm','product_height_cm','product_width_cm'])

    df_product_translated=pd.read_csv("data/raw_data/product_category_name_translation.csv")

    df_product=df_product.merge(df_product_translated, on="product_category_name", how="left")
    df_product = df_product.drop(columns=['product_category_name'])
    df_product = df_product.rename(columns={
        "product_category_name_english": "product_category_name"
    })
    df_product.to_csv(CLEANED_DATA / "product_dataset.csv", index=None)


## Cleaning sellers.csv

def clean_sellers():
    df_sellers=pd.read_csv(RAW_DATA / "olist_sellers_dataset.csv")
    df_sellers=df_sellers.drop(columns=['seller_state','seller_city'])
    df_sellers.to_csv(CLEANED_DATA / "sellers_dataset.csv", index=None)

def main():
    clean_order()
    clean_customers()
    clean_geolocation()
    clean_order_item()
    clean_order_payment()
    clean_product()
    clean_sellers()

if __name__ == "__main__":
    main()