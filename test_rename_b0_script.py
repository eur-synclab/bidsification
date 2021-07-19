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
file_type = ['3DT1', 'SNAT1', 'SNAT2', 'SNAT3', 'PCG1', 'PCG2', 'PCG3', 'rsfMRI', 'hires', 'B0-map_RS', 'B0-map', 'B0-map', 'B0-map', 'jones30_A', 'jones30_P']
new_file_type = ['T1mri', 'bold_SNAT1', 'bold_SNAT2', 'bold_SNAT3', 'bold_PCG1', 'bold_PCG2', 'bold_PCG3', 'bold_rsfmr', 'T2str', 'B0RS', 'Bzero1', 'Bzero2', 'Bzero3', 'DTIap', 'DTIpa', 'unknown_type', 'log']
cols = ['participant','nr_files'] + new_file_type
prefix = 'sub-mcc'
pseudobids_dir = os.path.join(root_dir, 'pseudobids')
bids_dir = os.path.join(root_dir, 'test_bidsify_output')
unallocated_dir = os.path.join(bids_dir, 'unallocated')

b0_opts = ['Bzero1', 'Bzero2', 'Bzero3', 'B0RS']
b0_opts_ind = ['1', '2', '3', '4']

participants = [name for name in os.listdir(unallocated_dir) if os.path.isdir(os.path.join(unallocated_dir, name))]
print(len(participants))

for p, participant in enumerate(participants):
    participant_str = f"{str(p+1).zfill(3)}: {participant}"
    participant_dir = os.path.join(unallocated_dir, participant)
    for session in bids_sessions:
        session_dir = os.path.join(participant_dir, session)
        if not os.path.isdir(session_dir):
            participant_str = participant_str + f" | No data for {session}"
        else:
            all_files = [fn for fn in os.listdir(session_dir) if os.path.isfile(os.path.join(session_dir, fn))]
            for file in all_files:
                nii_fn = os.path.join(session_dir, file)

                fmap_dir = os.path.join(bids_dir, participant, session, 'fmap')
                if not os.path.isdir(fmap_dir):
                    mkdir(fmap_dir)
                
                # find run
                # Find the first value in the b0_opts list that exists in file name
                match = next((x for x in b0_opts if x in file), False)
                run = b0_opts.index(match) + 1

                # find bids filename and move/rename
                if 'fieldmaphz_magnitude1' in file:
                    new_nii_fn = os.path.join(fmap_dir, participant + '_' + session + '_run-' + str(run) + '_fieldmap.nii')
                elif 'magnitude1' in file:
                    new_nii_fn = os.path.join(fmap_dir, participant + '_' + session + '_run-' + str(run) + '_magnitude.nii')
                else:
                    participant_str = participant_str + f" | EXTRA FILE: non-BO unallocated file found for {participant}: {file}"
                
                # move/rename
                os.rename(nii_fn, new_nii_fn)
    print(participant_str)
