from pyspark.sql.functions import current_timestamp, lit

raw_data_path = "/Volumes/workspace/restaurantdb/data"
bronze_db_name = "workspace.bronze_restaurant"
source_db = "workspace.restaurantdb"
tables_to_move = ["order_details", "menu", "employees", "orders", "weather"]

spark.sql(f"CREATE DATABASE IF NOT EXISTS {bronze_db_name}")

def ingest_to_bronze(source_db, table_name, target_schema):
    """
    Ingests data from an existing Databricks table into the Bronze layer 
    with added metadata for auditing.
    """
    print(f"Ingesting {source_db}.{table_name} into {target_schema}.{table_name}.")
    
    df_raw = spark.table(f"{source_db}.{table_name}")
    
    df_bronze = df_raw.withColumn("ingestion_timestamp", current_timestamp()) \
                      .withColumn("source_system", lit(source_db))
    
    df_bronze.write.format("delta") \
              .mode("overwrite") \
              .option("overwriteSchema", "true") \
              .saveAsTable(f"{target_schema}.{table_name}")
    
    print(f"Successfully loaded {table_name}.")

for t in tables_to_move:
    ingest_to_bronze(source_db, t, bronze_db_name)