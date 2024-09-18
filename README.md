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
deactivate
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
deactivate
```
# run the tutorials

Assuming you already are in directory `pmoired_tutorial`

```
source ./pmoired/bin/activate
jupyter-lab
```
to return to your python default installation, type `deactivate` after exciting `jupyter-lab`.


## Requirements
- Python 3.10 or newer
- A web-browser to run [Jupyter-lab](https://jupyter.org/)
- about 800Mb on disk (notebooks, data and full Python3 environment for `PMOIRED`)
- tested on Unix (MacOS and Linux)
