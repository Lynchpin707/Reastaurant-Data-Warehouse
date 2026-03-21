from pyspark.sql.functions import current_timestamp, lit

bronze_db_name = "workspace.bronze_restaurant"
spark.sql(f"CREATE DATABASE IF NOT EXISTS {bronze_db_name}")

def ingest_to_bronze(source_db, table_name, target_schema):
    """
    Ingests a source table into the Bronze layer with auditing metadata.

    Reads a specified table from the source database using the active Spark session, 
    appends 'ingestion_timestamp' and 'source_system' columns for tracking, and saves 
    the result as a Delta table in the target schema using overwrite mode.

    Args:
        source_db (str): The name of the source database containing the raw table.
        table_name (str): The name of the table to be ingested.
        target_schema (str): The target database schema for the Bronze layer.

    Returns:
        None
    """
    print(f"Ingesting {source_db}.{table_name} into {target_schema}.{table_name}.")
    
    df_raw = spark.table(f"{source_db}.{table_name}_raw")
    
    df_bronze = df_raw.withColumn("ingestion_timestamp", current_timestamp()) \
                      .withColumn("source_system", lit(source_db))
    
    df_bronze.write.format("delta") \
              .mode("overwrite") \
              .option("overwriteSchema", "true") \
              .saveAsTable(f"{target_schema}.{table_name}")
    
    print(f"Successfully loaded {table_name}.")

source_db = "workspace.restaurantdb"
tables_to_move = ["order_details", "menu", "employees", "orders", "weather"]
for t in tables_to_move:
    ingest_to_bronze(source_db, t, bronze_db_name)