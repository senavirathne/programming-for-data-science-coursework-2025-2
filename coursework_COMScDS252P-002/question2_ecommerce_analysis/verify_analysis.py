
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import os
import time

DATA_FILE = 'books_raw.csv'

def wait_for_data(timeout=300):
    start_time = time.time()
    while not os.path.exists(DATA_FILE):
        if time.time() - start_time > timeout:
            print("Timeout waiting for data file.")
            return False
        time.sleep(5)
    
    # Wait a bit more for file to be fully written
    time.sleep(2)
    return True

def clean_price(price_str):
    if isinstance(price_str, str):
        return float(price_str.replace('£', ''))
    return price_str

rating_map = {
    'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5
}

def clean_rating(rating_str):
    return rating_map.get(rating_str, 0)

def clean_availability(avail_str):
    return 'In stock' in str(avail_str)

def categorize_price(price):
    if price < 20:
        return 'Budget'
    elif 20 <= price <= 40:
        return 'Mid-range'
    else:
        return 'Premium'

def run_verification():
    print("Waiting for data...")
    if not wait_for_data():
        return

    print("Data found. Starting verification...")
    try:
        df = pd.read_csv(DATA_FILE)
        print(f"Loaded {len(df)} rows.")
        
        # Cleaning
        df['Price_Cleaned'] = df['Price'].apply(clean_price)
        df['Rating_Num'] = df['Rating'].apply(clean_rating)
        df['In_Stock'] = df['Availability'].apply(clean_availability)
        df = df.drop_duplicates()
        df['Price_Category'] = df['Price_Cleaned'].apply(categorize_price)
        
        # Stats
        print(f"Mean Price: {df['Price_Cleaned'].mean()}")
        
        # Regression
        if len(df) > 10:
            X = pd.get_dummies(df[['Rating_Num', 'Category']], drop_first=True)
            y = df['Price_Cleaned']
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            model = LinearRegression()
            model.fit(X_train, y_train)
            print("Regression model trained successfully.")
        
        print("Verification Successful!")
        
    except Exception as e:
        print(f"Verification Failed: {e}")

if __name__ == "__main__":
    run_verification()
