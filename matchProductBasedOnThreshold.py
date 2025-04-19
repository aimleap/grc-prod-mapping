#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from fuzzywuzzy import fuzz
import os
from itertools import combinations

# ---- CONFIGURATION ----
CATEGORY = "breadNBakery"
input_file = CATEGORY+"ProductMatching.xlsx"  # <-- Change this to your actual file name
sheet_name = 0
output_file = CATEGORY+"product_match_results.xlsx"
product_columns = ["Walmart Product", "Target Product", "Mariano Product", "Jewelosco Product"]
match_threshold = 85  # Adjust similarity threshold as needed
# ------------------------

# # Load the Excel file
# if not os.path.exists(input_file):
#     raise FileNotFoundError(f"Cannot find the input file: {input_file}")

df = pd.read_excel(input_file, sheet_name=sheet_name)
# df = pd.read_excel(input_file, sheet_name=sheet_name)
del df['Unnamed: 0']
df = df.fillna("")
# Check that required columns exist
missing_cols = [col for col in product_columns if col not in df.columns]
if missing_cols:
    raise ValueError(f"Missing required columns: {missing_cols}")

# Matching function
def is_match(a, b, threshold):
    if pd.isna(a) or pd.isna(b):
        return False
    parts_a = [p.strip() for p in str(a).split("|")]
    parts_b = [p.strip() for p in str(b).split("|")]
    for x in parts_a:
        for y in parts_b:
            if fuzz.token_set_ratio(x, y) >= threshold:
                return True
    return False

# Function to check all pairwise matches in a row
def compare_all_products(row):
    matches = []
    for col1, col2 in combinations(product_columns, 2):
        if is_match(row[col1], row[col2], match_threshold):
            matches.append(f"{col1} ↔ {col2}")
    if matches:
        return f"Matches found: {', '.join(matches)}"
    else:
        return "No Match"

# Apply to DataFrame
df["Match Result"] = df.apply(compare_all_products, axis=1)
df = df[df["Match Result"]!='No Match']
del df['Match Result']
# Save to Excel
df.to_excel(output_file, index=False)
print(f"✅ Results saved to: {output_file}")

