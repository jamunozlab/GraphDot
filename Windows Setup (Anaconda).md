# GraphDot (0.6.6)

## Windows Setup (Anaconda)

### GraphDot Dependencies 
First, you will need CUDA Toolkit 11.8. You can download it from https://developer.nvidia.com/cuda-11-8-0-download-archive.

You will also need VS 2019 build tools. This is no longer possible to directly download from the Visual Studio website. You will need to instead download VS 2022 or a later version.

### How to get VS 2019 Build Tools from VS 2022 Installer
1. Open Visual Studio Installer
   
2. Click on Modify
   
3. On the installation details, select "MSVC v142 - VS 2019 C++ x64/x86 build tools (v14.29)". Leave everything else the same.

### Anaconda Environment for Graphdot
1. Open Anaconda Navigator

2. Click on Environments

3. Create a new environment by clicking on the plus icon on the bottom.

4. Select Python Version 3.8.20

### Required Python Libraries
Pycuda 2022.1

ASE 3.23.0

Mendeleev 0.6.0

Networkx 3.1

Numy 1.23.5

Pandas 2.0.3

Pymatgen 2022.5.18.1

Scipy 1.10.1

Sympy 1.6

Treelib 1.8.0

### If Conda is unable to find cl.exe, you will need to make an environment inside the Native Tools Command Prompt for VS 2022.

C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat" -vcvars_ver=14.29

### How to open Jupyter Notebooks 
Open native tools command prompt for VS 2022. Initially, you will most likely be inside a directory with permissions disabled. Use the cd command to move to another directory with permissions enabled.
```cmd
"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat" -vcvars_ver=14.29

CALL C:\Users\ricky\anaconda3\Scripts\activate.bat

conda activate env

cd C:\Users\user\Dir_Permissions_Enabled\Jupyter_Notebooks_VS

Jupyter notebook
```

