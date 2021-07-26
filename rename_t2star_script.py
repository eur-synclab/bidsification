import os
import shutil
import sys
import glob
from pathlib import Path

# -----------------
# STEP 0: variables
# -----------------

root_dir = '/exports/fsw/Bendlab/SamenUniek'
# raw_sessions = ['MCC_ses03-lab', 'MCC_ses05-lab']
# bids_sessions = ['ses-w03lab', 'ses-w05lab']
raw_sessions = ['MCC_ses01-lab']
bids_sessions = ['ses-w01lab']
file_type = ['3DT1', 'SNAT1', 'SNAT2', 'SNAT3', 'PCG1', 'PCG2', 'PCG3', 'rsfMRI', 'hires', 'B0-map_RS', 'B0-map', 'B0-map', 'B0-map', 'jones30_A', 'jones30_P']
new_file_type = ['T1mri', 'bold_SNAT1', 'bold_SNAT2', 'bold_SNAT3', 'bold_PCG1', 'bold_PCG2', 'bold_PCG3', 'bold_rsfmr', 'T2str', 'B0RS', 'Bzero1', 'Bzero2', 'Bzero3', 'DTIap', 'DTIpa', 'unknown_type', 'log']
cols = ['participant','nr_files'] + new_file_type
prefix = 'sub-mcc'
pseudobids_dir = os.path.join(root_dir, 'pseudobids')
bids_dir = os.path.join(root_dir, 'bidsify_output')

participants = [name for name in os.listdir(bids_dir) if os.path.isdir(os.path.join(bids_dir, name))]

# Read directory names from raw data foler, write to text file
for p, participant in enumerate(participants):
    participant_str = f"{str(p+1).zfill(3)}: {participant}"
    participant_dir = os.path.join(bids_dir, participant)
    for session in bids_sessions:
        session_dir = os.path.join(participant_dir, session)
        if not os.path.isdir(session_dir):
            participant_str = participant_str + f" | No data for {session}"
        else:
            T2w_str = participant + '_' + session + '_T2w'
            nii_fn = os.path.join(session_dir, 'anat', T2w_str + '.nii')
            json_fn = os.path.join(session_dir, 'anat', T2w_str + '.json')
            if not os.path.isfile(nii_fn):
                participant_str = participant_str + f" | Note: No file {T2w_str}.nii"
            else:
                os.rename(nii_fn, nii_fn.replace('_T2w', '_T2starw'))
                if not os.path.isfile(json_fn):
                    participant_str = participant_str + f" | ERROR: no accompanying file {T2w_str}.json"
                else:
                    os.rename(nii_fn, json_fn.replace('_T2w', '_T2starw'))
    print(participant_str)