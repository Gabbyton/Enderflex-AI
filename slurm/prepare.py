import pandas as pd

# Create sample parquet to ensure compatibility with CWRU HPC SLURM
data = {'output': ['hello world!']}
df = pd.DataFrame(data)
df.to_parquet("input.parquet")