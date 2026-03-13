from pyspark.sql.functions import current_timestamp, lit

raw_data_path = "/Volumes/workspace/restaurantdb/data"
bronze_db_name = "bronze_restaurant"

spark.sql(f"CREATE DATABASE IF NOT EXISTS {bronze_db_name}")


def ingest_to_bronze(file_name, table_name):
    print(f"Ingesting {file_name} into {bronze_db_name}.{table_name}.")
    
    # Read CSV
    df_raw = (spark.read
              .format("csv")
              .option("header", "true")
              .option("inferSchema", "true")
              .load(f"{raw_data_path}/{file_name}"))
    
    # Add metadata: ingestion time and source file
    df_bronze = df_raw.withColumn("ingestion_timestamp", current_timestamp()) \
                      .withColumn("source_file", lit(file_name))
    
    # Write to Delta
    (df_bronze.write
     .format("delta")
     .mode("overwrite") # Use "append" for daily batches
     .option("overwriteSchema", "true")
     .saveAsTable(f"{bronze_db_name}.{table_name}"))
    
    print(f"Table {table_name} updated successfully.\n")

tables_to_ingest = [
    ("menu_raw.csv", "menu"),
    ("employees_raw.csv", "employees"),
    ("weather_raw.csv", "weather"),
    ("orders_raw.csv", "orders"),
    ("details_raw.csv", "order_details")
]

for csv_file, delta_table in tables_to_ingest:
    ingest_to_bronze(csv_file, delta_table)