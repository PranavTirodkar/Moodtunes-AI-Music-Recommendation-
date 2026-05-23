import pandas as pd
import os

# Check current directory
print("Current directory:", os.getcwd())

# List files in current directory
print("Files in current directory:")
for file in os.listdir('.'):
    print(f"  {file}")

# List files in parent directory
print("\nFiles in parent directory:")
for file in os.listdir('..'):
    print(f"  {file}")

# Try to load the datasets
dataset1_path = os.path.join('..', 'Music Recommendation System using Spotify Dataset.csv')
dataset2_path = os.path.join('..', 'Music Recommendation System using Spotify New Dataset.csv')

print(f"\nChecking for dataset 1 at: {dataset1_path}")
print(f"Dataset 1 exists: {os.path.exists(dataset1_path)}")

print(f"\nChecking for dataset 2 at: {dataset2_path}")
print(f"Dataset 2 exists: {os.path.exists(dataset2_path)}")

# Try to load a small sample of the data
if os.path.exists(dataset1_path):
    try:
        # Load just the first few rows to test
        df1 = pd.read_csv(dataset1_path, nrows=5)
        print(f"\nSuccessfully loaded dataset 1 sample:")
        print(f"Columns: {list(df1.columns)}")
        print(df1.head())
    except Exception as e:
        print(f"Error loading dataset 1: {e}")

if os.path.exists(dataset2_path):
    try:
        # Load just the first few rows to test
        df2 = pd.read_csv(dataset2_path, nrows=5)
        print(f"\nSuccessfully loaded dataset 2 sample:")
        print(f"Columns: {list(df2.columns)}")
        print(df2.head())
    except Exception as e:
        print(f"Error loading dataset 2: {e}")