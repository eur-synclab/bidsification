# bidsification
This repo contains a notebook to convert par/rec data to bids format, using the bidsify package (https://github.com/NILAB-UvA/bidsify).



## 1. Installation


### Step 1.1: clone this repository

On SHARK, from your home directory (`/home/your-shark-username/`), clone this repo:

```
git clone https://github.com/eur-synclab/bidsification.git
```

This creates the directory: `/home/your-shark-username/bidsification`.


### Step 1.2: create / activate `conda` environment

On SHARK, first purge all modules and add the `miniconda` module:

```
module purge
module add tools/miniconda/python3.8/4.9.2
```

Then create a new `conda` environment:

(*Note: if you have previously created the conda environment and already installed the packages in the environment, you do not have to repeat this step.*
*You just have to run the `module add...` command, then `conda activate bidsification` and then continue with the instructions in the `2. Running the code` section below*)

```
conda create -n bidsification python=3.8
```

The process will ask you for input: enter `y` (yes), press `return`, and wait for the process to finish. Then activate your new environment:

```
conda activate bidsification
```

### Step 1.3: install required packages

Then install `dcm2niix`:

```
conda install -c conda-forge dcm2niix
```

Then install `bidsify`:

```
pip install git+https://github.com/NILAB-UvA/bidsify.git@master
```

Lastly install `pandas`:

```
pip install pandas
```

## 2. Running the code

*IMPORTANT: before running the code, coordinate with colleagues to see if they have already run parts of it, or if they're busy running parts of it*

After installation/activatiom of the conda environment, navigate to the bidsification directory and ensure that the `master` branch is checked out:

```
git checkout master
```

### Step 2.1: run the main data setup script with python

```
python /home/your-shark-username/bidsification/bidsification_script.py
```

If you are currently located in the cloned `bidsification` directory, you can exclude the `/home/your-shark-username/bidsification/` and run:

```
python bidsification_script.py 2>&1 | tee bidsification_log_<unique-id>.txt
```

This will take some time to complete, since it renames all raw files
and then copies required files to the `pseudobids` directory located in the root data location (`/exports/fsw/Bendlab/SamenUniek/pseudobids`).

This script also adds every subject identifier and related metadata to a conversion log file per session, e.g. `MCC_ses03-lab_conversion_log.csv`.

If the script stops running for some reason, you can rerun it and it will know from the conversion log file which subjects have already been processed fully.
It will then skip these and continue with the rest.

The `2>&1 | tee bidsification_log_<unique-id>.txt` part of the command writes all of the script output to a log file, so that it can be viewed later.
Remember to replace the `<unique-id>` part every time you run it (e.g. `bidsification_log_14Jul01.txt`)


### Step 2.2: run `bidsify`

```
bidsify -c /home/your-shark-username/bidsification/config.json -d /exports/fsw/Bendlab/SamenUniek/pseudobids -o /exports/fsw/Bendlab/SamenUniek/bidsify_output 2>&1 | tee bidsify_log_<unique-id>.txt
```

If you are currently located in the cloned `bidsification` directory, you can exclude the `/home/your-shark-username/bidsification/` and run:

```
bidsify -c config.json -d /exports/fsw/Bendlab/SamenUniek/pseudobids -o /exports/fsw/Bendlab/SamenUniek/bidsify_output 2>&1 | tee bidsify_log_<unique-id>.txt
```

The `2>&1 | tee bidsify_log_<unique-id>.txt` part of the command writes all of the command line output to a log file, so that it can be viewed later.
Remember to replace the `<unique-id>` part every time you run it (e.g. `bidsify_log_14Jul01.txt`)

### Step 2.3: run the B0 file renaming script

*TODO*

```
python ---.py
```

### Step 2.4: run `bidsify` again on the `unallocated` subdirectory 

This is to convert the previously ambiguosly named B0 maps to BIDS because they were deliberately skipped in the previous `bidsify` run.

*TODO*

```
python ---.py
```

### Step 2.5: run the T2w to T2star renaming script

*TODO*

```
python ---.py
```

### Step 2.6: run the script to add any further required JSON info for BIDS

*TODO*

```
python ---.py
```

### Step 2.7: run data checking script

Compare the amount and type of files per subject/session between raw data and BIDS data, for quality control.

*TODO*

```
python ---.py
```

### Step 2.8: run BIDS validator

*TODO*

```
python ---.py
```