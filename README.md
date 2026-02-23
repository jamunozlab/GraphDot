# GraphDot

## Punakha Setup

### How to access the container, create the tunnel, and open Jupyter Notebook

---

## Terminal 1 (on Punakha)

```bash
# Start an interactive GPU session
srun -p hgx -A punakha_general --gres=gpu:1 --pty bash -i

# Load Docker module
module load docker/27.3.1

# Start rootless Docker
# (Make sure you previously configured ~/.docker/start_rootless_docker.sh)
~/.docker/start_rootless_docker.sh

# Run NVIDIA PyTorch container
docker run --rm -it \
  --gpus all \
  --ipc=host --ulimit memlock=-1 --ulimit stack=67108864 \
  -e NVIDIA_VISIBLE_DEVICES="$CUDA_VISIBLE_DEVICES" \
  -e CUDA_VISIBLE_DEVICES=0 \
  -p 8888:8888 \
  -v /scratch/dajuarez4:/scratch/dajuarez4 \
  -w /scratch/dajuarez4 \
  nvcr.io/nvidia/pytorch:24.12-py3 \
  bash
```

---

## Terminal 2 (Local Machine)

### Option 1 — Password Login (No SSH key required)

```bash
ssh -o PubkeyAuthentication=no \
  -o PreferredAuthentications=password \
  -o IdentitiesOnly=yes \
  dajuarez4@hopper002
```

---

### Option 2 — SSH Tunnel Through Punakha

```bash
ssh -t -t %USERNAME%@punakha.utep.edu \
  -L 8888:localhost:8888 \
  ssh hopper00x -L 8888:localhost:8888
```

Then open in your browser:

```
http://localhost:8888
```

---

# Docker Rootless Setup  
(Recommended: build in `/Work` or `/Scratch`)

> Home directory usually does not have enough space.

```bash
mkdir -p ~/.docker

cp /etc/docker/daemon.json ~/.docker/daemon.json
sed -i 's|"iptables": false|"iptables": true|g' ~/.docker/daemon.json

cp /opt/ohpc/pub/apps/docker/start_rootless_docker.sh ~/.docker/start_rootless_docker.sh
sed -i "s|--config-file=/etc/docker/daemon.json|--config-file=/home/$(whoami)/.docker/daemon.json|g" ~/.docker/start_rootless_docker.sh
```

---

# Create Python 3.6 Environment with GraphDot

## Create environment

```bash
conda create -n py36_env -c conda-forge python=3.6 -y
```

## Install required packages

```bash
conda install -y -n py36_env -c conda-forge pycuda
conda install -y -n py36_env -c conda-forge rdkit

conda run -n py36_env python -m pip uninstall -y pytools
conda run -n py36_env python -m pip install "pytools==2020.4.4"

conda install -y -n py36_env -c conda-forge "pymatgen==2019.11.11"
conda run -n py36_env python -m pip install --force-reinstall "ruamel.yaml==0.17.21"
conda run -n py36_env python -m pip install -U graphdot
```

---

# Register Jupyter Kernel

```bash
conda activate py36_env
python -m pip install ipykernel
python -m ipykernel install --user \
  --name py36_env \
  --display-name "Python 3.6 (py36) with graphdot"
```

---

# Verify CUDA inside container

```bash
python -c "import torch; print('cuda:', torch.cuda.is_available())"
```
