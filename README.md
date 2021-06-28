# bidsification
This repo contains a notebook to convert par/rec data to bids format, using the bidsify package (https://github.com/NILAB-UvA/bidsify).



## Installation

On SHARK, first purge all modules and add the `miniconda` module:

```
module purge
module add tools/miniconda/python3.8/4.9.2
```

Then create a new `conda` environment:

(*Note: if you have previously created the conda environment and already installed the packages in the environment, you do not have to repeat that.*
*You just have to run `conda activate bidsification` and then continue with the instructions in the `Running the code` section below*)

```
conda create -n bidsification python=3.8
```

The process will ask you for input: enter `y` (yes), press `return`, and wait for the process to finish. Then activate your new environment:

```
conda activate bidsification
```

Then install `dcm2niix`:

```
conda install -c conda-forge dcm2niix
```

Then install `bidsify`:

```
pip install git+https://github.com/NILAB-UvA/bidsify.git@master
```

## Running the code

*WORK IN PROGRESS*

*not all directory locations are correctly specified yet, and ideally all scripts and call to bidsify should all be contained in a single script file*

After installation, navigate to the bidsification directory and run the main data setup script with python:

```
python bidsification_script.py
```

This will take some time to complete, since it renames all raw files
and then copies them to a pseudobids directory.

Then run `bidsify`:

```
bidsify -c /exports/fsw/Bendlab/SamenUniek/SU31_bids/config.json -d /exports/fsw/Bendlab/SamenUniek/SU31_bids/pseudobids
```

Then run the T2w to T2star renaming script:

```
python rename_t2star_script.py
```







