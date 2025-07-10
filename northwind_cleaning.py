# ===============================
# 📦 NORTHWIND DATA CLEANING SCRIPT
# ===============================
# This script loads and cleans the Northwind dataset
# by merging multiple CSVs and engineering features.
# Output: 'northwind_master_dataset.csv'

import pandas as pd
import re

# ===============================
# 1. LOAD RAW DATA FILES
# ===============================
customers = pd.read_csv(r"C:\Users\babul\OneDrive\Desktop\files\demo3\customers.csv")
products = pd.read_csv(r"C:\Users\babul\OneDrive\Desktop\files\demo3\products.csv")
orders = pd.read_csv(r"C:\Users\babul\OneDrive\Desktop\files\demo3\orders.csv")
categories = pd.read_csv(r"C:\Users\babul\OneDrive\Desktop\files\demo3\categories.csv")
shippers = pd.read_csv(r"C:\Users\babul\OneDrive\Desktop\files\demo3\shippers.csv")
order_details = pd.read_csv(r"C:\Users\babul\OneDrive\Desktop\files\demo3\order_details.csv")

# ===============================
# 2. CLEAN CUSTOMERS
# ===============================
customers = customers.drop_duplicates().reset_index(drop=True)

# Fill missing values
customers.fillna({
    "Address": "Unknown",
    "City": "Unknown",
    "Country": "Unknown",
    "Phone": "Unknown",
    "PostalCode": "0000"
}, inplace=True)

# Strip whitespaces and convert to string
def clean_text_columns(df):
    for col in df.columns:
        df[col] = df[col].astype(str).str.strip()
    return df

customers = clean_text_columns(customers)

# Clean phone and fax fields
customers["Phone"] = customers["Phone"].str.replace(r"\s+", "", regex=True)
customers["Fax"] = customers["Fax"].str.replace(r"\s+", "", regex=True)

# ===============================
# 3. CLEAN PRODUCTS
# ===============================
products = products.drop_duplicates().reset_index(drop=True)
products.rename(columns={"Discontinued": "Available"}, inplace=True)
products["Available"] = products["Available"] == 0  # True if available

# ===============================
# 4. CLEAN ORDERS
# ===============================
orders = orders.drop_duplicates().reset_index(drop=True)

# Convert to datetime
orders["OrderDate"] = pd.to_datetime(orders["OrderDate"])
orders["RequiredDate"] = pd.to_datetime(orders["RequiredDate"])
orders["ShippedDate"] = pd.to_datetime(orders["ShippedDate"])

# Fill NA and add flags
orders["ShipRegion"] = orders["ShipRegion"].fillna("Unknown")
orders["ShipPostalCode"] = orders["ShipPostalCode"].fillna("Unknown")

orders["ShippedDateMissing"] = orders["ShippedDate"].isna()

# Clean string fields
text_cols = ["CustomerID", "ShipName", "ShipAddress", "ShipCity", "ShipRegion", "ShipPostalCode", "ShipCountry"]
orders[text_cols] = orders[text_cols].apply(lambda col: col.astype(str).str.strip())

# ===============================
# 5. MERGE ALL FILES TOGETHER
# ===============================
merged_df = (
    order_details
    .merge(orders, on="OrderID", how="left")
    .merge(products, on="ProductID", how="left")
    .merge(categories, on="CategoryID", how="left")
    .merge(customers, on="CustomerID", how="left")
    .merge(shippers, left_on="ShipVia", right_on="ShipperID", how="left")
)

# ===============================
# 6. CLEAN & RENAME COLUMNS
# ===============================
merged_df.rename(columns={
    "UnitPrice_x": "OrderDetailUnitPrice",
    "UnitPrice_y": "ProductUnitPrice",
    "CompanyName_x": "CustomerCompany",
    "CompanyName_y": "ShipperCompany",
    "Phone_x": "CustomerPhone",
    "Phone_y": "ShipperPhone"
}, inplace=True)

# Drop unnecessary columns
cols_to_drop = [
    "Fax", "Description", "SupplierID", "QuantityPerUnit", "UnitsInStock",
    "UnitsOnOrder", "ReorderLevel", "Available", "ContactName", "ContactTitle",
    "Address", "City", "Region", "PostalCode", "CustomerPhone", "ShipperPhone"
]
merged_df.drop(columns=cols_to_drop, inplace=True)

# ===============================
# 7. FEATURE ENGINEERING
# ===============================
merged_df["Revenue"] = merged_df["Quantity"] * merged_df["OrderDetailUnitPrice"]
merged_df["DeliveryDays"] = (merged_df["ShippedDate"] - merged_df["OrderDate"]).dt.days
merged_df["OrderMonth"] = merged_df["OrderDate"].dt.to_period("M")

# ===============================
# 8. SAVE FINAL CLEANED FILE
# ===============================
merged_df.to_csv("northwind_master_dataset.csv", index=False)

# ===============================
# 9. CLEANING SUMMARY
# ===============================
print("\n📦 DATA CLEANING SUMMARY")
print("==============================")
print(f"Customers cleaned: {customers.shape[0]} unique entries")
print(f"Products cleaned: {products.shape[0]} unique entries")
print(f"Orders cleaned: {orders.shape[0]} unique entries")
print(f"Final dataset rows: {merged_df.shape[0]}")
print(f"Final dataset columns: {merged_df.shape[1]}")
print(f"Missing values remaining: {merged_df.isna().sum().sum()}")
print(f"Revenue column added: {'Revenue' in merged_df.columns}")
print(f"DeliveryDays column added: {'DeliveryDays' in merged_df.columns}")
print("==============================")
print("✅ Data cleaning complete. Final dataset saved as 'northwind_master_dataset.csv'\n")
