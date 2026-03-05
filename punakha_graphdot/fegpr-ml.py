print('----------------Begin ML---------------------')

import time
import os, glob
import numpy as np
import pandas as pd
from ase.io import read
from graphdot import Graph
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from graphdot.graph.adjacency import AtomicAdjacency
from graphdot.model.gaussian_process import GaussianProcessRegressor
from graphdot.kernel.fix import Normalization
from graphdot.kernel.molecular import Tang2019MolecularKernel as MolecularKernel

base_paths = ["/scratch/dajuarez4/QE_Fe/PBE/",
             "/scratch/dajuarez4/QE_Fe/PBEsol/"]

def search_folder_names(path):
    return sorted(
        d for d in os.listdir(path)
        if os.path.isdir(os.path.join(path, d))
    )

def build_sim_paths(base_paths):
    sim_paths = []
    for base in base_paths:
        for folder in search_folder_names(base):
            folder_path = os.path.join(base, folder)
            for subfolder in search_folder_names(folder_path):
                sim_paths.append(os.path.join(folder_path, subfolder))
    return sim_paths

sim_paths = build_sim_paths(base_paths)



def plot(mu, test_data, target, out_dir):
    y_true = np.asarray(test_data[target])
    y_pred = np.asarray(mu)
    
    mae  = np.mean(np.abs(y_true - y_pred))
    rmse = np.sqrt(np.mean((y_true - y_pred)**2))
    
    lo = min(y_true.min(), y_pred.min())
    hi = max(y_true.max(), y_pred.max())
    pad = 0.03*(hi-lo) if hi > lo else 1.0
    lo -= pad; hi += pad
    
    fig, ax = plt.subplots(figsize=(9, 9), dpi=150)
    
    ax.scatter(y_true, y_pred, s=60, alpha=0.75, edgecolors="k", linewidths=0.4)
    ax.plot([lo, hi], [lo, hi], lw=3)
    
    ax.ticklabel_format(axis='x', style='plain', useOffset=False)
    ax.xaxis.set_major_formatter(mticker.ScalarFormatter(useOffset=False))
    ax.xaxis.get_major_formatter().set_scientific(False)
    
    ax.ticklabel_format(axis='y', style='plain', useOffset=False)
    ax.yaxis.set_major_formatter(mticker.ScalarFormatter(useOffset=False))
    ax.yaxis.get_major_formatter().set_scientific(False)

    ax.set_xlim(lo, hi)
    ax.set_ylim(lo, hi)
    ax.set_aspect("equal", adjustable="box")
    ax.tick_params(axis="x", labelrotation=45)
    for label in ax.get_xticklabels():
        label.set_ha("right")
        
    ax.grid(True, which="major", alpha=0.25, linewidth=1.2)
    ax.minorticks_on()
    ax.grid(True, which="minor", alpha=0.12, linewidth=0.8)
    
    ax.set_xlabel("Ground truth energy (eV)", labelpad=10)
    ax.set_ylabel("Predicted energy (eV)", labelpad=10)
    ax.set_title("GPR Parity Plot", pad=14)
    
    stats = f"N = {len(y_true)}\nMAE = {mae:.4g} eV\nRMSE = {rmse:.4g} eV"
    ax.text(
        0.02, 0.98, stats,
        transform=ax.transAxes,
        va="top", ha="left",
        fontsize=16,
        bbox=dict(boxstyle="round,pad=0.5", alpha=0.90)
    )
    
    plt.tight_layout()
    plt.savefig(
        f"{out_dir}/parity_plot.png",
        dpi=300,
        transparent=True,
        bbox_inches="tight",
        pad_inches=0.05
    )
    plt.show()





def training_graphdot(path):    
    gpr = GaussianProcessRegressor(
        kernel=Normalization(MolecularKernel()),
        alpha=1e-4,
        optimizer=True,
        normalize_y=True,
    )
    
    data_dir = path
    files = [os.path.join(data_dir, f"fe{i}.out") for i in range(1, 6)]
    print("Files:", files)
    
    atoms_list = []
    for fp in files:
        if not os.path.exists(fp):
            # just ignore missing files
            continue
        atoms_list.extend(read(fp, index=":", format="espresso-out"))
    
    # if this folder has no fe*.out (or nothing readable), skip without error
    if len(atoms_list) == 0:
        return None
    
    print("Total frames read:", len(atoms_list))
    
    graphs = [Graph.from_ase(a, adjacency=AtomicAdjacency(shape="compactbell3,2")) for a in atoms_list]
    energy_gt = [a.get_potential_energy() for a in atoms_list]
    
    data = pd.DataFrame({"Graphs": graphs, "Pot_Energy": energy_gt})
    print(data.head())
    
    ntsteps = len(atoms_list)
    target = 'Pot_Energy' 
    N_test = ntsteps//3
    N_train = ntsteps 
    print(N_train)
    print(N_test)
    np.random.seed(0)
    
    train_sel = np.random.choice(ntsteps, N_train, replace=False)
    test_sel = np.random.choice(ntsteps, N_test, replace=False)
    train_data = data.iloc[train_sel]
    test_data = data.iloc[test_sel]
    print(train_data)
    
    start_time = time.time()
    gpr = gpr.fit(train_data['Graphs'], train_data[target], repeat=1, verbose=True)
    end_time = time.time()
    print("the total time consumption for " + str(N_train) + " steps is " + str((end_time - start_time)/3600) + "hr.")
    
    out_dir = data_dir
    os.makedirs(out_dir, exist_ok=True)
    
    fname = f"gpr_DFT_PotEng{N_train}.pkl"
    gpr.save(out_dir, filename=fname, overwrite=True)
    
    print("saved to:", os.path.join(out_dir, fname))
    
    #fname = f"gpr_DFT_PotEng{N_train}.pkl"
    #gpr.load(out_dir, filename=fname)
    
    mu = gpr.predict(test_data["Graphs"])
    return gpr, mu, test_data,target

total = len(sim_paths)

for i, simulation in enumerate(sim_paths, start=1):
    print(f"[{i}/{total}] Processing {simulation}...")
    gpr, mu, test_data, target = training_graphdot(simulation)
    plot(mu, test_data, target, simulation)

