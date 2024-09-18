# [`PMOIRED`](https://github.com/amerand/PMOIRED) practical session for the [2024 VLTI School](https://vltischool2024.sciencesconf.org/)

## Install the tutorial

You can clone the github repository:
```
git clone https://github.com/amerand/PMOIRED_VLTI2024
cd PMOIRED_VLTI2024
```

Or get the [.zip archive](https://github.com/amerand/PMOIRED_VLTI2024/archive/refs/heads/main.zip):
```
unzip PMOIRED_VLTI2024-main.zip
cd PMOIRED_VLTI2024-main
```

## Install `PMOIRED` (in a Python environment)

If you already have `PMOIRED`, you still need the latest version (1.2.10, from Sept 18th 2024). You should install `PMOIRED` in a python environment, so it will not interfere with your current Python installation:
```
python3 -m venv ./pmoired
source ./pmoired/bin/activate
pip3 install pmoired==1.2.10 jupyterlab ipympl
jupyter-lab tutorial1.ipynb
```

After exiting `jupyter-lab` (ctrl-c), you can type `deactivate` in the terminal to go back to your default Python installation.

## Requirements
- Python 3.10 or newer
- A web-browser to run [Jupyter-lab](https://jupyter.org/)
- about 700Mb on disk (tutorial + full Python3 environment for `PMOIRED`)
- tested on Unix (MacOS and Linux)
