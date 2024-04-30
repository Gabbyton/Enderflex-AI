from sdlefleets_dev import sdlefleets

# 5 python jobs
sdlefleets(job_name='gop2_caxton_download',
script_path='/mnt/vstor/CSE_MSE_RXF131/cradle-members/mdle/gop2/Git/caxton/extraction/run.py',
parquet_path='/mnt/vstor/CSE_MSE_RXF131/cradle-members/mdle/gop2/Git/caxton/extraction/20240331-152746-source.parquet',
duration='00:15:00')