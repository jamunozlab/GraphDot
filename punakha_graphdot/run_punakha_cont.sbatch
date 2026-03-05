#!/bin/bash
#SBATCH --job-name=fe_ml_gpr
#SBATCH --partition=hgx
#SBATCH --account=punakha_general
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=20:00:00
#SBATCH --output=%j.log
#SBATCH --gres=gpu:1

set -e
pwd
hostname
date
ulimit -s unlimited

# Cache/temp to scratch (avoid quota issues)
export XDG_CACHE_HOME=/scratch/dajuarez4/.cache
mkdir -p $XDG_CACHE_HOME/pycuda

export MPLCONFIGDIR=/scratch/dajuarez4/.matplotlib
mkdir -p $MPLCONFIGDIR

export PYTHONUNBUFFERED=1

module load docker/27.3.1
/scratch/dajuarez4/.docker/start_rootless_docker.sh

# Optional host debug
nvidia-smi || true

docker run --rm \
  --gpus all \
  --ipc=host --ulimit memlock=-1 --ulimit stack=67108864 \
  -e NVIDIA_VISIBLE_DEVICES="${CUDA_VISIBLE_DEVICES}" \
  -e CUDA_VISIBLE_DEVICES=0 \
  -e XDG_CACHE_HOME=/scratch/dajuarez4/.cache \
  -e MPLCONFIGDIR=/scratch/dajuarez4/.matplotlib \
  -e PYTHONUNBUFFERED=1 \
  -e SLURM_JOB_ID="${SLURM_JOB_ID}" \
  -v /scratch/dajuarez4:/scratch/dajuarez4 \
  -v /work/dajuarez4:/work/dajuarez4 \
  -w /work/dajuarez4/test \
  nvcr.io/nvidia/pytorch:24.12-py3 \
  bash -lc '
    echo "=== Inside container ==="
    which nvcc
    nvcc --version
    nvidia-smi

    PYTHON=/scratch/dajuarez4/miniforge3/envs/py36_env/bin/python
    $PYTHON -c "import sys; print(sys.executable)"
    $PYTHON -u fegpr-ml.py 2>&1 | tee /scratch/dajuarez4/test/ml_${SLURM_JOB_ID}.out
  '
