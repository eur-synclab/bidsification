import os
import shutil
import sys
import glob
# import pandas as pd
from pathlib import Path

# -----------------
# STEP 0: variables
# -----------------

root_dir = '/exports/fsw/Bendlab/SamenUniek'
raw_sessions = ['MCC_ses03-lab', 'MCC_ses05-lab']
bids_sessions = ['ses-w03lab', 'ses-w05lab']
file_type = ['3DT1', 'SNAT1', 'SNAT2', 'SNAT3', 'PCG1', 'PCG2', 'PCG3', 'rsfMRI', 'hires', 'B0-map_RS', 'B0-map', 'jones30_A', 'jones30_P']
new_file_type = ['T1mri', 'bold_SNAT1', 'bold_SNAT2', 'bold_SNAT3', 'bold_PCG1', 'bold_PCG2', 'bold_PCG3', 'bold_rsfmr', 'T2str', 'Bzero_RS', 'Bzero', 'DTIap', 'DTIpa']


for i, session in enumerate(raw_sessions):
    raw_data_dir = os.path.join(root_dir, session)

    # Create log file
    participant_info_fn = os.path.join(root_dir, session + '_participant_info.txt')
    # If the text file already exists, delete it
    if os.path.isfile(participant_info_fn):
        os.remove(participant_info_fn)
    # df = pd.DataFrame(columns=['participant','nr_files])

    # Read directory names from raw data foler, write to text file

    for participant in os.listdir(raw_data_dir):
        participant_dir = os.path.join(raw_data_dir, participant)
        if os.path.isdir(participant_dir):
            # print(participant)
            nr_files = len([name for name in os.listdir(participant_dir) if os.path.isfile(os.path.join(participant_dir, name))])
            f = open(participant_info_fn,'a+')
            f.write(participant + '\t' + nr_files + '\n')
            f.close()