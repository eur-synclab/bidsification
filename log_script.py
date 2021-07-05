import os
import shutil
import sys
import glob
import pandas as pd
from pathlib import Path

# -----------------
# STEP 0: variables
# -----------------

root_dir = '/exports/fsw/Bendlab/SamenUniek'
# /exports/fsw/Bendlab/SamenUniek/MCC_ses03-lab
raw_sessions = ['MCC_ses03-lab', 'MCC_ses05-lab']
bids_sessions = ['ses-w03lab', 'ses-w05lab']
file_type = ['3DT1', 'SNAT1', 'SNAT2', 'SNAT3', 'PCG1', 'PCG2', 'PCG3', 'rsfMRI', 'hires', 'B0-map_RS', 'B0-map', 'B0-map', 'jones30_A', 'jones30_P']
new_file_type = ['T1mri', 'bold_SNAT1', 'bold_SNAT2', 'bold_SNAT3', 'bold_PCG1', 'bold_PCG2', 'bold_PCG3', 'bold_rsfmr', 'T2str', 'Bzero_RS', 'Bzero_1', 'Bzero_2', 'DTIap', 'DTIpa']

for i, session in enumerate(raw_sessions):
    raw_data_dir = os.path.join(root_dir, session)

    # Create log file
    participant_info_fn = os.path.join(root_dir, session + '_participant_info.tsv')
    # If the text file already exists, delete it
    # if os.path.isfile(participant_info_fn):
    #     os.remove(participant_info_fn)
    
    cols = ['participant','nr_files'] + new_file_type
    df = pd.DataFrame(columns=cols)
    # df.append(df2, ignore_index=True)

    # Read directory names from raw data foler, write to text file

    for participant in os.listdir(raw_data_dir):
        participant_dir = os.path.join(raw_data_dir, participant)
        first_b0_found = False
        if os.path.isdir(participant_dir):
            # print(participant)
            all_files = [name for name in os.listdir(participant_dir) if os.path.isfile(os.path.join(participant_dir, name))]
            nr_files = len(all_files)

            new_row = [None] * len(cols)
            new_row[0] = participant
            new_row[1] = len(cols)

            for j, file = enumerate(all_files):
                if file[-4:] == '.PAR':
                    code = file[11:-4]
                    # open and read the protecolline needed for renaming
                    with open(name, 'r') as f:
                        protocolline = f.readlines()
                    
                    line = protocolline[13]
                    # Find the first value in the file_type list that exists in protocolline 13 (old identifier)
                    match = next((x for x in file_type if x in line), False)
                    # Find the index in the new_file_type list that corresponds to the match (new identifier)
                    if match == 'B0-map':
                        if not first_b0_found:
                            first_b0_found = True
                            idx = 10
                        else:
                            idx = 11
                    else:
                        idx = file_type.index(match)
                    
                    new_row[idx+2] = code
            df_new_row = pd.DataFrame(new_row, columns=cols)
            df.append(df_new_row, ignore_index=True)
                    
            df.to_csv(participant_info_fn, sep='\t')
        else:
            print('Error: participant directory not found')