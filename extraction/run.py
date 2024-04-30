import sys
import os.path as path
import subprocess

from datetime import datetime
import pandas as pd
import time

# Do not edit the print statements!!!!

try:
    #line contains one line of your input CSV file
    parquet_path = sys.argv[1]
    start = int(sys.argv[2])
    end = int(sys.argv[3])

    print(f'[SLURMSTART] {datetime.now().strftime("%Y-%m-%d-%H:%M:%S")} Job started with args:-{parquet_path} {start} {end}') 
    input_df = pd.read_parquet(parquet_path, engine='pyarrow').iloc[start:end]
    print(input_df.to_string())
    # CODE
    try:
        url, name, download_path = input_df[["url", "name", "download_path"]].iloc[0]
        unzip_path = path.join(download_path, name)
        subprocess.run(f'curl -o {unzip_path} -L {url}', shell=True)
        time.sleep(1)
        subprocess.run(f'unzip -q {unzip_path} -d {download_path}', shell=True)
        time.sleep(1)
        subprocess.run(f'rm {unzip_path}', shell=True)
        time.sleep(1)
    except Exception as e:
        print("[CODE_ERROR]")
        print(f"error output: {e}")


    print(f'[SLURMEND] {datetime.now().strftime("%Y-%m-%d-%H:%M:%S")} Job finished successfully')
except Exception as e:
    print(f'[SLURMFAIL] {datetime.now().strftime("%Y-%m-%d-%H:%M:%S")} Job failed, see error below')

