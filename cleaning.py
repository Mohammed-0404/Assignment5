import pandas as pd
import numpy as np

def clean_price_column(series):

    cleaned_series = series.astype(str).copy()
    cleaned_series = cleaned_series.str.replace('US $', '', regex=False).str.replace('$', '', regex=False).str.replace(',', '', regex=False).str.strip()
    cleaned_series.replace(['', 'nan', 'N/A'], np.nan, inplace=True)
    return cleaned_series

def clean_data(input_file, output_file):

    try:
        df = pd.read_csv(input_file, dtype=str)
    except Exception:
        return

    df['price'] = clean_price_column(df['price'])
    df['original_price'] = clean_price_column(df['original_price'])
    
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df.dropna(subset=['price'], inplace=True)

    df['original_price'] = pd.to_numeric(df['original_price'], errors='coerce')
    df['original_price'] = df['original_price'].fillna(df['price'])

    df['shipping'] = df['shipping'].fillna("Shipping info unavailable")

    discount = df['original_price'] - df['price']
    df['discount_percentage'] = np.where(
        (df['original_price'] > 0) & (discount > 0),
        (discount / df['original_price']) * 100,
        0.0
    ).round(2)

    try:
        df.to_csv(output_file, index=False)
    except Exception:
        return

if __name__ == "_main_":
    clean_data("ebay_tech_deals.csv", "cleaned_ebay_deals.csv")