from pyspark.sql import functions as F
from pyspark.sql.functions import col

# 1. Charger avec des alias clairs pour éviter les conflits
s_orders = spark.read.table("silver_restaurant.orders").alias("orders")
s_details = spark.read.table("silver_restaurant.order_details").alias("details")
s_menu = spark.read.table("silver_restaurant.menu").alias("menu")
s_weather = spark.read.table("silver_restaurant.weather").alias("weather")
s_emp = spark.read.table("silver_restaurant.employees").alias("emp")

# 2. Construction avec préfixes explicites (df_alias.colonne)
gold_sales = s_details.join(s_orders, "order_id") \
    .join(s_menu, s_details.item_id == s_menu.item_id) \
    .join(s_weather, "weather_id") \
    .join(s_emp, s_orders.server_id == s_emp.emp_id, "left") \
    .select(
        F.col("orders.order_id"), 
        # On choisit explicitement le timestamp de la commande
        F.col("orders.timestamp").alias("sale_time"), 
        F.to_date("orders.timestamp").alias("sale_date"),
        F.hour("orders.timestamp").alias("sale_hour"),
        F.col("menu.name").alias("item_name"),
        F.col("menu.cat").alias("item_category"),
        F.col("menu.price").alias("unit_price"),
        F.col("details.qty"),
        (F.col("menu.price") * F.col("details.qty")).alias("total_revenue"),
        F.col("orders.order_type"),
        F.col("weather.condition").alias("weather_condition"),
        F.col("weather.temp").alias("temperature"),
        # Vérifie si la colonne dans Employees est 'name' ou 'name_emp'
        F.col("emp.name").alias("server_name"), 
        F.col("emp.role").alias("server_role")
    )

# 3. Sauvegarde
gold_sales.write.format("delta").mode("overwrite").saveAsTable("gold_restaurant.fact_sales")