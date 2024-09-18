# [`PMOIRED`](https://github.com/amerand/PMOIRED) practical session for the [2024 VLTI School](https://vltischool2024.sciencesconf.org/)

Clone the github repository (or get the [.zip archive](https://github.com/amerand/VLTI2024/archive/refs/heads/main.zip)):
```
git clone https://github.com/amerand/VLTISchool2024
```

if you already have `PMOIRED`, you still need the latest version (1.2.10, from Sept 18th 2024). You should install `PMOIRED` in a python environment, so it will not interfere with your current installation:
```
python3 -m venv ./pmoired
source ./pmoired/bin/activate
pip3 install pmoired==1.2.10 jupyterlab ipympl
jupyter-lab
```
after exiting `jupyter-lab`, you can type `deactivate` in the terminal to go back to your default python3 installation.
