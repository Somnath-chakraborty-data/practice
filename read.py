import pandas as pd

# Step 1: Create sample data
data = {
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 35],
    "City": ["New York", "Los Angeles", "Chicago"]
}

df = pd.DataFrame(data)

# Step 2: Save as Parquet (overwrite if exists)
df.to_parquet("sample.parquet", engine="pyarrow", index=False)
print("Parquet file created successfully!")

# Step 3: Read the Parquet file
df_read = pd.read_parquet("sample.parquet", engine="pyarrow")
print("\nData read from Parquet file:")
print(df_read)
