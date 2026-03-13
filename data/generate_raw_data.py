import pandas as pd
import numpy as np
import random
import os
from datetime import datetime, timedelta

output_dir = 'data/raw'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


menu_items = [
    # Main Courses (10)
    {'item_id': 1, 'name': 'Lamb Tagine', 'cat': 'Main', 'price': 95.0},
    {'item_id': 2, 'name': 'Chicken Bastilla', 'cat': 'Main', 'price': 110.0},
    {'item_id': 3, 'name': 'COUSCOUS VEGETARIAN', 'cat': 'Main', 'price': 85.0},
    {'item_id': 4, 'name': 'Kefta', 'cat': 'Main', 'price': 80.0},
    {'item_id': 5, 'name': 'Beef Tajine', 'cat': 'Main', 'price': 120.0},
    {'item_id': 6, 'name': 'Fish Tajine', 'cat': 'Main', 'price': 95.0},
    {'item_id': 7, 'name': 'Rfissa Chicken', 'cat': 'Main', 'price': 105.0},
    {'item_id': 8, 'name': 'Mechoui', 'cat': 'Main', 'price': 150.0},
    {'item_id': 9, 'name': 'Seafood Bastilla', 'cat': 'Main', 'price': 130.0},
    {'item_id': 10, 'name': 'Royal Couscous', 'cat': 'Main', 'price': 140.0},
    # Appetizers (5)
    {'item_id': 11, 'name': 'Zaalouk', 'cat': 'Appetizer', 'price': 35.0},
    {'item_id': 12, 'name': 'Harira Soup', 'cat': 'Appetizer', 'price': 30.0},
    {'item_id': 13, 'name': 'Briotat Cheese', 'cat': 'Appetizer', 'price': 45.0},
    {'item_id': 14, 'name': 'Taktouka', 'cat': 'Appetizer', 'price': 35.0},
    {'item_id': 15, 'name': 'Mixed Olives', 'cat': 'Appetizer', 'price': None}, # NULL Price
    # Beverages (7)
    {'item_id': 16, 'name': 'Mint Tea (Pot)', 'cat': 'Beverage', 'price': 20.0},
    {'item_id': 17, 'name': 'Nespresso', 'cat': 'Beverage', 'price': 25.0},
    {'item_id': 18, 'name': 'Fresh Orange Juice', 'cat': 'Beverage', 'price': 500.0}, # Outlier
    {'item_id': 19, 'name': 'Avocado Shake', 'cat': 'Beverage', 'price': 35.0},
    {'item_id': 20, 'name': 'Mineral Water', 'cat': 'Beverage', 'price': 15.0},
    {'item_id': 21, 'name': 'Coca-Cola', 'cat': 'Beverage', 'price': 18.0},
    {'item_id': 22, 'name': 'Pomegranate Juice', 'cat': 'Beverage', 'price': 30.0},
    # Sides (4)
    {'item_id': 23, 'name': 'French Fries', 'cat': 'Side', 'price': 20.0},
    {'item_id': 24, 'name': 'Tafernout', 'cat': 'Side', 'price': 5.0},
    {'item_id': 25, 'name': 'Rice Pilaf', 'cat': 'Side', 'price': 25.0},
    {'item_id': 26, 'name': 'Side Salad', 'cat': 'Side', 'price': 15.0},
    # Desserts (4)
    {'item_id': 27, 'name': 'Chebakia', 'cat': 'Dessert', 'price': 15.0},
    {'item_id': 28, 'name': 'Almond Ghoriba', 'cat': None, 'price': 12.0}, # NULL Cat
    {'item_id': 29, 'name': 'Orange with Cinnamon', 'cat': 'Dessert', 'price': 25.0},
    {'item_id': 30, 'name': 'Fekkas', 'cat': 'Dessert', 'price': 20.0}
]
df_menu = pd.DataFrame(menu_items)

# --- 2. EMPLOYEES ---
employees_data = [
    {'emp_id': 101, 'name': 'Maryem', 'role': 'Manager', 'hourly_rate': 55.0},
    {'emp_id': 102, 'name': 'Aymane', 'role': 'chef', 'hourly_rate': 22.0},
    {'emp_id': 103, 'name': 'Soufiane', 'role': 'WAITER', 'hourly_rate': 22.0},
    {'emp_id': 104, 'name': 'Lina', 'role': 'Chef', 'hourly_rate': 50.0},
    {'emp_id': 105, 'name': 'Mouhsine', 'role': 'waiter', 'hourly_rate': None}
]
df_employees = pd.DataFrame(employees_data)

# --- 3. WEATHER LOGS ---
weather_records = []
start_date = datetime(2026, 1, 1)
for i in range(24 * 60): # 5 days
    weather_records.append({
        'weather_id': i,
        'timestamp': start_date + timedelta(hours=i),
        'temp': round(random.uniform(15, 25), 1),
        'condition': random.choice(['Sunny', 'Rainy', 'Cloudy'])
    })
df_weather = pd.DataFrame(weather_records)

# --- 4. ORDERS & DETAILS ---
orders = []
details = []
detail_id_counter = 1
# Mix of valid and messy labels for service types
service_types = ['On Site', 'TO GO', 'sur place', 'To Go', None] 

for i in range(1, 15162):
    order_type = random.choice(service_types)
    orders.append({
        'order_id': i,
        'server_id': random.choice([101, 102, 103, 105, 999]),
        'order_type': order_type,
        'timestamp': start_date + timedelta(minutes=i*30),
        'weather_id': random.randint(0, 119)
    })
    
    # 1-6 items per order
    for _ in range(random.randint(1, 6)):
        item = df_menu.sample(1).iloc[0]
        details.append({
            'detail_id': detail_id_counter,
            'order_id': i,
            'item_id': item['item_id'],
            'qty': random.randint(1, 3)
        })
        detail_id_counter += 1

df_orders = pd.DataFrame(orders)
df_details = pd.DataFrame(details)

# --- 5. EXPORT ---
tables = {'menu': df_menu, 'employees': df_employees, 'weather': df_weather, 'orders': df_orders, 'details': df_details}
for name, df in tables.items():
    df.to_csv(f"{output_dir}/{name}_raw.csv", index=False)
    print(f"Generated {name}_raw.csv")
    print(df.size)