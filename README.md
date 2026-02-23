## GraphDot


# Punakha

How to access to the container, create the tunnel and open Jupyter notebook:
# ---- Terminal 1)
#enter punakha
#start an interactive
srun -p hgx -A punakha_general --gres=gpu:1 --pty bash -i
#load docker container
module load docker/27.3.1
# Go to your path where you built you header .docker/start_rootless_docker.sh
/.docker/start_rootless_docker.sh
# run the following script but change your path where you built you header .docker/start_rootless_docker.sh
docker run --rm -it \
  --gpus all \
  --ipc=host --ulimit memlock=-1 --ulimit stack=67108864 \
  -e NVIDIA_VISIBLE_DEVICES="$CUDA_VISIBLE_DEVICES" \
  -e CUDA_VISIBLE_DEVICES=0 \
  -p 8888:8888 \
  -v /scratch/dajuarez4:/scratch/dajuarez4 \
  -w /scratch/dajuarez4 \
  nvcr.io/nvidia/pytorch:24.12-py3 \
  bash -lc "python -c 'import torch; print(\"cuda:\", torch.cuda.is_available()); print(\"dev:\", torch.cuda.g>

# Mac users or me: 
# --- Terminal 2)

# Just run the following command 
ssh -o PubkeyAuthentication=no -o PreferredAuthentications=password -o IdentitiesOnly=yes dajuarez4@hopper002
# In that way you dont need to create a key in your local computer 
# if you dont have problems with that just run the command:
ssh -t -t %USERNAME%@punakha.utep.edu -L 8888:localhost:8888 ssh hopper00x -L 8888:localhost:8888
#Note: in your local machine


# As there is not enough space in Home you can work in: /Work or /Scratch so I recommend build there the follo>
mkdir -p .docker

cp /etc/docker/daemon.json ~/.docker/daemon.json
sed -i 's|"iptables": false|"iptables": true|g' ~/.docker/daemon.json

cp /opt/ohpc/pub/apps/docker/start_rootless_docker.sh ~/.docker/start_rootless_docker.sh
sed -i "s|--config-file=/etc/docker/daemon.json|--config-file=/home/$(whoami)/.docker/daemon.json|g" ~/.docker>


Create environment with python3.6 that has Graphdot

conda create -n py36_env -c conda-forge python=3.6 -y
#conda activate py36_env
# or not activate and run like this 
conda install -y -n py36_env -c conda-forge pycuda
conda install -y -n py36_env -c conda-forge rdkit
conda run -n py36_env python -m pip uninstall -y pytools
conda run -n py36_env python -m pip install "pytools==2020.4.4"
conda install -y -n py36_env -c conda-forge "pymatgen==2019.11.11"
conda run -n py36_env python -m pip install --force-reinstall "ruamel.yaml==0.17.21"
conda run -n py36_env python -m pip install -U graphdot
python -m pip install ipykernel
conda activate py36_env
python -m pip install ipykernel
python -m ipykernel install --user --name py36_env --display-name "Python 3.6 (py36) with graphdot"


