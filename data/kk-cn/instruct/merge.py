import pandas as pd
import glob
import os

file_name = "train"
parquet_files = glob.glob(f'./*/{file_name}.parquet')
print(f"Found {len(parquet_files)} files")
dfs = []

for file in parquet_files:
    if "8ppl" in file:
        continue
    df = pd.read_parquet(file)
    dfs.append(df)
    print(f"Loaded file: {file}, shape: {df.shape}")

merged_df = pd.concat(dfs, ignore_index=True)
print(f"After concat: {merged_df.shape}")
os.makedirs('./allppl', exist_ok=True)
merged_df.to_parquet(f'./allppl/{file_name}.parquet')