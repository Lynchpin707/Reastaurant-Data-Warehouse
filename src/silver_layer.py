from pyspark.sql import functions as F

# Chargement des tables Bronze
orders_df = spark.read.table("bronze_restaurant.orders")
items_df = spark.read.table("bronze_restaurant.menu")
employees_df = spark.read.table("bronze_restaurant.employees")
details_df = spark.read.table("bronze_restaurant.order_details")
weather_df = spark.read.table("bronze_restaurant.weather")

# --- NETTOYAGE SILVER ---

# 1. Nettoyage Menu : Correction prix aberrant et catégories
silver_menu = items_df.withColumn(
    "price", 
    F.when(F.col("price") > 400, 25.0).otherwise(F.col("price")) # Correction Juice 500 -> 25
).fillna({"price": 20.0, "cat": "Other"})

# 2. Nettoyage Employees : Standardisation des rôles
silver_employees = employees_df.withColumn(
    "role", F.initcap(F.trim(F.col("role"))) # "waiter" ou "WAITER" -> "Waiter"
).fillna({"hourly_rate": 20.0})

# 3. Nettoyage Orders : Standardisation "To Go" / "Sur Place"
silver_orders = orders_df.withColumn(
    "order_type", 
    F.when(F.lower(F.col("order_type")).contains("to"), "To Go")
     .otherwise("Sur Place")
).dropDuplicates(["order_id"])

# Sauvegarde en Silver
silver_menu.write.format("delta").mode("overwrite").saveAsTable("silver_restaurant.menu")
silver_employees.write.format("delta").mode("overwrite").saveAsTable("silver_restaurant.employees")
silver_orders.write.format("delta").mode("overwrite").saveAsTable("silver_restaurant.orders")
details_df.write.format("delta").mode("overwrite").saveAsTable("silver_restaurant.order_details")
weather_df.write.format("delta").mode("overwrite").saveAsTable("silver_restaurant.weather")