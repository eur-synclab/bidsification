import os
import shutil
import sys
import glob
from pathlib import Path

# -----------------
# STEP 0: variables
# -----------------

root_dir = '/exports/fsw/Bendlab/SamenUniek'
raw_sessions = ['MCC_ses03-lab', 'MCC_ses05-lab']
bids_sessions = ['ses-w03lab', 'ses-w05lab']
file_type = ['3DT1', 'SNAT1', 'SNAT2', 'SNAT3', 'PCG1', 'PCG2', 'PCG3', 'rsfMRI', 'hires', 'B0-map', 'jones30_A', 'jones30_P']
new_file_type = ['T1mri', 'SNAT1', 'SNAT2', 'SNAT3', 'PCG1', 'PCG2', 'PCG3', 'rsfmr', 'T2str', 'Bzero', 'DTIap', 'DTIpa']
config_fn = '/exports/fsw/Bendlab/SamenUniek/SU31_bids/config.json'

# -------------------------------------
# STEP 4: rename T2w to T2star
# -------------------------------------
for root, directories, filenames in os.walk(bids_dir):
    if filenames != []:
        for file in filenames:
            #extract the file name and path
            name = root + '/' + file
            name = name.replace("\\", "/")
            renameT2 = root + '/' + file[:26] + 'T2star' + file[29:]
 
            if file[26:29] == 'T2w':
                print(name)
                if not os.path.isfile(renameT2):
                    print(renameT2)
                    os.rename(name, renameT2)
                else:
                    print('WARNING: file ' + renameT2 + ' already exists in the folder! This file will therefore be skipped!')