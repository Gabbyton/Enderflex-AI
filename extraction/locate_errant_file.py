import os
import os.path as path

from tqdm import tqdm

if __name__ == '__main__':

  log_path = "/mnt/vstor/CSE_MSE_RXF131/cradle-members/mdle/gop2/Git/caxton/extraction/log-20240331192805"
  KEY = "[SLURMEND]"
  bad_files = []
  files = [file for file in os.scandir(log_path) if file.name.endswith('.out')]
  print
  for file in tqdm(files):
    with open(file.path) as f:
      for line in f.readlines():
        if KEY in line:
          bad_files.append(file.path)
          break

  print(bad_files)