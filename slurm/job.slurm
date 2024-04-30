#!/bin/bash
#SBATCH 
#SBATCH --account="rxf131_aisc"
#SBATCH --partition="aisc"
#SBATCH --nice=2147483645 
#SBATCH --requeue
#SBATCH --job-name="gop2_caxton_training"
#SBATCH --time=60:00:00
#SBATCH --nodes=1
#SBATCH --output="/mnt/vstor/CSE_MSE_RXF131/cradle-members/mdle/gop2/Git/caxton/slurm/logs/%x-%j.out"
#SBATCH --cpus-per-task=8
#SBATCH --mem=64gb
#SBATCH --gres=gpu:8

/mnt/vstor/CSE_MSE_RXF131/sdle-ondemand/pioneer/config/run.sh --nv /home/rxf131/ondemand/share/build_link/apt_gpu-pt.sif python3 /mnt/vstor/CSE_MSE_RXF131/cradle-members/mdle/gop2/Git/caxton/src/train_slurm.py /mnt/vstor/CSE_MSE_RXF131/cradle-members/mdle/gop2/Git/caxton/slurm/input.parquet 0 1