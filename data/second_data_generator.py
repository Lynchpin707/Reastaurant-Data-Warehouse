import pandas as pd
import numpy as np
import random
import os
from datetime import datetime, timedelta

output_dir = 'data/raw'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# --- 1. MENU (Schéma strict conservé) ---
menu_items = [
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
    {'item_id': 11, 'name': 'Zaalouk', 'cat': 'Appetizer', 'price': 35.0},
    {'item_id': 12, 'name': 'Harira Soup', 'cat': 'Appetizer', 'price': 30.0},
    {'item_id': 13, 'name': 'Briotat Cheese', 'cat': 'Appetizer', 'price': 45.0},
    {'item_id': 14, 'name': 'Taktouka', 'cat': 'Appetizer', 'price': 35.0},
    {'item_id': 15, 'name': 'Mixed Olives', 'cat': 'Appetizer', 'price': None}, 
    {'item_id': 16, 'name': 'Mint Tea (Pot)', 'cat': 'Beverage', 'price': 20.0},
    {'item_id': 17, 'name': 'Nespresso', 'cat': 'Beverage', 'price': 25.0},
    {'item_id': 18, 'name': 'Fresh Orange Juice', 'cat': 'Beverage', 'price': 500.0}, 
    {'item_id': 19, 'name': 'Avocado Shake', 'cat': 'Beverage', 'price': 35.0},
    {'item_id': 20, 'name': 'Mineral Water', 'cat': 'Beverage', 'price': 15.0},
    {'item_id': 21, 'name': 'Coca-Cola', 'cat': 'Beverage', 'price': 18.0},
    {'item_id': 22, 'name': 'Pomegranate Juice', 'cat': 'Beverage', 'price': 30.0},
    {'item_id': 23, 'name': 'French Fries', 'cat': 'Side', 'price': 20.0},
    {'item_id': 24, 'name': 'Tafernout', 'cat': 'Side', 'price': 5.0},
    {'item_id': 25, 'name': 'Rice Pilaf', 'cat': 'Side', 'price': 25.0},
    {'item_id': 26, 'name': 'Side Salad', 'cat': 'Side', 'price': 15.0},
    {'item_id': 27, 'name': 'Chebakia', 'cat': 'Dessert', 'price': 15.0},
    {'item_id': 28, 'name': 'Almond Ghoriba', 'cat': None, 'price': 12.0}, 
    {'item_id': 29, 'name': 'Orange with Cinnamon', 'cat': 'Dessert', 'price': 25.0},
    {'item_id': 30, 'name': 'Fekkas', 'cat': 'Dessert', 'price': 20.0}
]
df_menu = pd.DataFrame(menu_items)

# --- 2. EMPLOYEES (Schéma strict conservé) ---
employees_data = [
    {'emp_id': 101, 'name': 'Maryem', 'role': 'Manager', 'hourly_rate': 55.0},
    {'emp_id': 102, 'name': 'Aymane', 'role': 'chef', 'hourly_rate': 22.0},
    {'emp_id': 103, 'name': 'Soufiane', 'role': 'WAITER', 'hourly_rate': 22.0},
    {'emp_id': 104, 'name': 'Lina', 'role': 'Chef', 'hourly_rate': 50.0},
    {'emp_id': 105, 'name': 'Mouhsine', 'role': 'waiter', 'hourly_rate': None}
]
df_employees = pd.DataFrame(employees_data)

# --- 3. CONFIGURATION DU TEMPS (Août 2025 sur 6 mois) ---
start_date = datetime(2025, 8, 1) # 1er Août 2025
end_date = start_date + timedelta(days=184) # 184 jours = ~6 mois (jusqu'à fin Janvier 2026)

# --- 4. WEATHER LOGS ---
weather_records = []
total_hours = int((end_date - start_date).total_seconds() // 3600) + 24 # +24h de marge de sécurité

for i in range(total_hours): 
    weather_records.append({
        'weather_id': i,
        'timestamp': start_date + timedelta(hours=i),
        'temp': round(random.uniform(12, 32), 1),
        'condition': np.random.choice(['Sunny', 'Rainy', 'Cloudy'], p=[0.6, 0.2, 0.2])
    })
df_weather = pd.DataFrame(weather_records)

# --- 5. ORDERS & DETAILS ---
orders = []
details = []
detail_id_counter = 1
service_types = ['On Site', 'TO GO', 'sur place', 'To Go', None]

def get_weather_id(dt):
    """Récupère l'ID météo correspondant à l'heure actuelle"""
    delta = dt - start_date
    w_id = int(delta.total_seconds() // 3600)
    return min(w_id, len(df_weather) - 1)

order_id = 1
current_time = start_date + timedelta(hours=8) # Ouverture à 8h le 1er Août

# CHANGEMENT CLÉ : La boucle tourne tant qu'on n'a pas atteint la date de fin (6 mois plus tard)
while current_time < end_date:
    hr = current_time.hour
    
    # DISTRIBUTION 1 : Pics d'affluence (Bimodal)
    # J'ai légèrement augmenté les "gaps" (temps entre commandes) pour que sur 6 mois, 
    # le volume final soit réaliste pour un restaurant de cette taille (environ 20k-30k commandes)
    if 12 <= hr <= 14:   # Rush du midi
        gap = random.randint(3, 8)
    elif 19 <= hr <= 22: # Rush du soir
        gap = random.randint(2, 6)
    elif 8 <= hr <= 11 or 15 <= hr <= 18: # Heures creuses
        gap = random.randint(15, 30)
    else: # Très tard le soir
        gap = random.randint(60, 120)
        
    current_time += timedelta(minutes=gap)
    
    # Fermeture du restaurant de 2h à 8h du matin
    if 2 <= current_time.hour < 8:
        current_time = current_time.replace(hour=8, minute=0)
        continue

    # DISTRIBUTION 2 : Boost du Weekend
    if current_time.weekday() >= 4 and random.random() > 0.8: 
        num_orders_in_slot = 2 
    else:
        num_orders_in_slot = 1

    for _ in range(num_orders_in_slot):
        w_id = get_weather_id(current_time)
        weather_cond = df_weather.iloc[w_id]['condition']
        temp = df_weather.iloc[w_id]['temp']
        
        # DISTRIBUTION 3 : Rotation des serveurs (Shifts)
        if 8 <= current_time.hour <= 16:
            server = random.choice([101, 102, 103,999]) 
        else:
            server = random.choice([101, 104, 105, 999])
            
        order_type = random.choice(service_types)
        
        orders.append({
            'order_id': order_id,
            'server_id': server,
            'order_type': order_type,
            'timestamp': current_time,
            'weather_id': w_id
        })
        
        # DISTRIBUTION 4 : Logique des items commandés
        num_items = random.randint(1, 6)
        
        for _ in range(num_items):
            if current_time.hour < 11:
                item_pool = df_menu[df_menu['cat'].isin(['Beverage', 'Dessert', None])]
            else:
                item_pool = df_menu
                
            if weather_cond == 'Rainy' and random.random() > 0.6:
                item_pool = df_menu[df_menu['item_id'].isin([12, 16])]
            elif temp > 28 and random.random() > 0.6:
                item_pool = df_menu[df_menu['item_id'].isin([18, 19, 20, 21, 22, 26])]

            if item_pool.empty:
                item_pool = df_menu
                
            item = item_pool.sample(1).iloc[0]
            qty = random.randint(1, 2) if item['cat'] in ['Main', 'Appetizer'] else random.randint(1, 4)

            details.append({
                'detail_id': detail_id_counter,
                'order_id': order_id,
                'item_id': item['item_id'],
                'qty': qty
            })
            detail_id_counter += 1
            
        order_id += 1

df_orders = pd.DataFrame(orders)
df_details = pd.DataFrame(details)

# --- 6. EXPORT ---
tables = {'menu': df_menu, 'employees': df_employees, 'weather': df_weather, 'orders': df_orders, 'details': df_details}
for name, df in tables.items():
    df.to_csv(f"{output_dir}/{name}_raw.csv", index=False)
    print(f"Generated {name}_raw.csv - Rows: {len(df)}")