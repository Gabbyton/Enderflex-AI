import os
import os.path as path
from datetime import datetime
import numpy as np
import pandas as pd
import re

def check_finished(download_path, end_idx, start_idx=1):
  all_numbers = set(range(start_idx, end_idx + 1))
  folders = [folder for folder in os.listdir(download_path) if path.isdir(path.join(download_path, folder))]
  print(folders)
  numbers = set([int(re.search('print(\\d+)', folder).group(1)) for folder in folders])
  print(numbers)
  return list(all_numbers - numbers)

if __name__ == '__main__':
  DOWNLOAD_LIMIT = None
  END_IDX = 191
  FORMAT = "ZIP file"
  COLUMNS = ["url", "name"]
  INPUT_PATH = "/mnt/vstor/CSE_MSE_RXF131/cradle-members/mdle/gop2/Git/caxton/extraction/caxton-data-download.csv"
  DOWNLOAD_PATH = "/mnt/vstor/CSE_MSE_RXF131/cradle-members/mdle/gop2/hdd/caxton_dataset"
  PARQUET_PATH = "source.parquet"

  PRINT_PATTERN = r'print(\d+)\.zip'

  df = pd.read_csv(INPUT_PATH)
  filtered_df = df[df['format'] == FORMAT]
  filtered_df = filtered_df[COLUMNS]
  filtered_df["download_path"] = DOWNLOAD_PATH
  filtered_df["number"] = filtered_df["name"].str.replace(PRINT_PATTERN, r'\1', regex=True)
  filtered_df["number"] = filtered_df["number"].astype(int)

  pending_list = check_finished(DOWNLOAD_PATH, END_IDX)
  filtered_df = filtered_df[filtered_df['number'].isin(pending_list)]

  if DOWNLOAD_LIMIT:
    filtered_df = filtered_df.head(DOWNLOAD_LIMIT)
  parent, basename = path.split(PARQUET_PATH)
  parquet_path = path.join(parent, f'{datetime.now().strftime("%Y%m%d-%H%M%S")}-{basename}')

  print("Preview of Parquet:")
  print(filtered_df)

  filtered_df.to_parquet(parquet_path)
  print(f"Saved parquet to: {parquet_path}")

