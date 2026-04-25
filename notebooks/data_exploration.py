
import pandas as pd
import os

file_path = os.path.join(os.path.dirname(__file__), "..", "data", "recalls_raw.csv")

df = pd.read_csv(file_path)
# =========================
# 1. LOAD DATA
# =========================


print("\n=== RAW DATA OVERVIEW ===")
print("Shape:", df.shape)
print("\nColumns:\n", df.columns)
print("\nFirst 5 rows:\n", df.head())


# =========================
# 2. BASIC CLEANING
# =========================

# Convert Date column
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Drop missing important fields
df = df.dropna(subset=['ProductDescription', 'Company'])

# Clean text fields
df['ProductDescription'] = df['ProductDescription'].astype(str).str.lower()
df['Company'] = df['Company'].astype(str).str.lower()
df['ProductType'] = df['ProductType'].astype(str).str.lower()
df['Reason'] = df['Reason'].astype(str).str.lower()

print("\n=== AFTER CLEANING ===")
print("Shape:", df.shape)
print(df.info())


# =========================
# 3. DATA QUALITY CHECK
# =========================

print("\n=== MISSING VALUES ===")
print(df.isnull().sum())


# =========================
# 4. PRODUCT TYPE ANALYSIS
# =========================

print("\n=== PRODUCT TYPE DISTRIBUTION ===")
print(df['ProductType'].value_counts())


# =========================
# 5. TOP RECALLING COMPANIES
# =========================

print("\n=== TOP 10 COMPANIES WITH RECALLS ===")
print(df['Company'].value_counts().head(10))


# =========================
# 6. TIME TREND ANALYSIS
# =========================

df['Year'] = df['Date'].dt.year

print("\n=== RECALLS PER YEAR ===")
print(df['Year'].value_counts().sort_index())


# =========================
# 7. SIMPLE INSIGHTS
# =========================

print("\n=== KEY INSIGHTS ===")

top_company = df['Company'].value_counts().idxmax()
top_product_type = df['ProductType'].value_counts().idxmax()

print("Most frequent recalling company:", top_company)
print("Most common product type:", top_product_type)