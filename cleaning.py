import pandas as pd


df = pd.read_csv("ebay_tech_deals.csv", dtype=str)

df["price"] = df["price"].astype(str).str.replace("US $", "").str.replace(",", "").str.strip()
df["original_price"] = df["original_price"].astype(str).str.replace("US $", "").str.replace(",", "").str.strip()

df["price"] = pd.to_numeric(df["price"], errors='coerce')
df["original_price"] = pd.to_numeric(df["original_price"], errors='coerce')

df["original_price"].fillna(df["price"], inplace=True)

df.loc[df["shipping"].isna() | df["shipping"].str.strip().isin(["", "N/A"]), "shipping"] = "Shipping info unavailable"
df["shipping"] = df["shipping"].str.strip()

df["discount_percentage"] = ((df["original_price"] - df["price"]) / df["original_price"]) * 100
df["discount_percentage"] = df["discount_percentage"].round(2).fillna(0.0)

df.to_csv("cleaned_ebay_deals.csv", index=False)

print("Data cleaning complete. Saved as cleaned_ebay_deals.csv.")