import json
import pandas as pd

# -----------------------------
# Step 1: Create sample JSON file
# -----------------------------
sample_data = {
    "company": "Tech Solutions",
    "employees": [
        {
            "id": 1,
            "name": "Alice Johnson",
            "age": 28,
            "department": "Engineering",
            "skills": ["Python", "SQL", "Azure"]
        },
        {
            "id": 2,
            "name": "Bob Smith",
            "age": 34,
            "department": "Data Science",
            "skills": ["R", "Machine Learning", "Power BI"]
        },
        {
            "id": 3,
            "name": "Charlie Brown",
            "age": 25,
            "department": "Cloud",
            "skills": ["AWS", "Docker", "Kubernetes"]
        }
    ]
}

# Save JSON file
with open("sample.json", "w") as f:
    json.dump(sample_data, f, indent=4)

print("JSON file created successfully!\n")

# -----------------------------
# Step 2: Read JSON file
# -----------------------------
with open("sample.json", "r") as f:
    data = json.load(f)

# Print full JSON data
print("Full JSON data:")
print(data)
print("\nEmployees details:")

# Print employee info
for emp in data["employees"]:
    print(f"{emp['name']} works in {emp['department']} with skills {emp['skills']}")

# -----------------------------
# Step 3: Convert JSON to DataFrame
# -----------------------------
df = pd.DataFrame(data["employees"])
print("\nDataFrame created from JSON:")
print(df)

# -----------------------------
# Step 4: Save DataFrame as Parquet
# -----------------------------
df.to_parquet("sample.parquet", engine="pyarrow", index=False)
print("\nParquet file created successfully!")

# -----------------------------
# Step 5: Read Parquet file back
# -----------------------------
df_read = pd.read_parquet("sample.parquet", engine="pyarrow")
print("\nData read from Parquet file:")
print(df_read)
