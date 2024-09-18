# [`PMOIRED`](https://github.com/amerand/PMOIRED) practical session for the [2024 VLTI School](https://vltischool2024.sciencesconf.org/)


## Full install scripts (`PMOIRED` in python environments)

With `git`:
```
mkdir pmoired_tutorial
cd pmoired_tutorial
git clone https://github.com/amerand/PMOIRED_examples
git clone https://github.com/amerand/PMOIRED_VLTI2024
python3 -m venv ./pmoired
source ./pmoired/bin/activate
pip3 install pmoired==1.2.10 jupyterlab ipympl
jupyter-lab
```

getting zip files using `wget`:
```
mkdir pmoired_tutorial
cd pmoired_tutorial
wget https://github.com/amerand/PMOIRED_examples/archive/refs/heads/main.zip
wget https://github.com/amerand/PMOIRED_VLTI2024/archive/refs/heads/main.zip
unzip *zip
python3 -m venv ./pmoired
source ./pmoired/bin/activate
pip3 install pmoired==1.2.10 jupyterlab ipympl
jupyter-lab
```

to exit the environment, type `deactivate`.

## Requirements
- Python 3.10 or newer
- A web-browser to run [Jupyter-lab](https://jupyter.org/)
- about 700Mb on disk (tutorial + full Python3 environment for `PMOIRED`)
- tested on Unix (MacOS and Linux)
