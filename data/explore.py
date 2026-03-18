import pandas as pd
import os

data_dir = '/Volumes/workspace/restaurantdb/data'

def explore_restaurant_data():
    # Load all tables
    files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
    
    for file in files:
        df = pd.DataFrame()
        try:
            df = pd.read_csv(os.path.join(data_dir, file))
        except Exception as e:
            print(f"Error loading {file}: {e}")
            continue

        print(f"\n{'='*20} EXPLORING: {file} {'='*20}")
        
        # 1. Quick View
        print(f"Shape: {df.shape[0]} rows, {df.shape[1]} columns")
        
        # 2. Check for Missing Values 
        null_counts = df.isnull().sum()
        if null_counts.any():
            print("\n[!] MISSING VALUES DETECTED:")
            print(null_counts[null_counts > 0])
        
        # 3. Check for Duplicates
        dup_count = df.duplicated().sum()
        if dup_count > 0:
            print(f"\n[!] DUPLICATE ROWS: {dup_count}")

        # 4. Deep Dive into Specific Columns
        if 'menu' in file:
            print("\nTop 5 Most Expensive Items (Checking for Outliers):")
            print(df.nlargest(5, 'price')[['name', 'price']])
            
        if 'orders' in file:
            print("\nOrder Type Distribution (Checking Casing Issues):")
            print(df['order_type'].value_counts(dropna=False))
            
            print("\nInvalid Server IDs (ID 999 is a known error):")
            print(f"Count of ID 999: {len(df[df['server_id'] == 999])}")

        if 'employees' in file:
            print("\nUnique Roles (Checking Normalization needs):")
            print(df['role'].unique())

# Run the exploration
explore_restaurant_data()