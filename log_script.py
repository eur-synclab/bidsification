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
# /exports/fsw/Bendlab/SamenUniek/MCC_ses03-lab/SU33100901/ FSL_14_1
raw_sessions = ['MCC_ses03-lab', 'MCC_ses05-lab']
bids_sessions = ['ses-w03lab', 'ses-w05lab']
# raw_sessions = ['MCC_ses05-lab']
# bids_sessions = ['ses-w05lab']
file_type = ['3DT1', 'SNAT1', 'SNAT2', 'SNAT3', 'PCG1', 'PCG2', 'PCG3', 'rsfMRI', 'hires', 'B0-map_RS', 'B0-map', 'B0-map', 'jones30_A', 'jones30_P']
new_file_type = ['T1mri', 'bold_SNAT1', 'bold_SNAT2', 'bold_SNAT3', 'bold_PCG1', 'bold_PCG2', 'bold_PCG3', 'bold_rsfmr', 'T2str', 'Bzero_RS', 'Bzero_1', 'Bzero_2', 'DTIap', 'DTIpa', 'FSLnii', 'log']

for i, session in enumerate(raw_sessions):
    raw_data_dir = os.path.join(root_dir, session)
    print(raw_data_dir)

    # Create log file
    participant_info_fn = os.path.join(root_dir, session + '_participant_info_extended.tsv')
    participant_info_fncsv = os.path.join(root_dir, session + '_participant_info_extended.csv')
    # If the text file already exists, delete it
    if os.path.isfile(participant_info_fn):
        os.remove(participant_info_fn)
    if os.path.isfile(participant_info_fncsv):
        os.remove(participant_info_fncsv)
    
    cols = ['participant','nr_files'] + new_file_type
    df = pd.DataFrame(columns=cols)
    
    # Read directory names from raw data foler, write to text file
    for p, participant in enumerate(os.listdir(raw_data_dir)):
        participant_dir = os.path.join(raw_data_dir, participant)
        first_b0_found = False
        fsl_found = False
        if os.path.isdir(participant_dir):
            print(f"{str(p).zfill(3)}: {participant}")
            all_files = [name for name in os.listdir(participant_dir) if os.path.isfile(os.path.join(participant_dir, name))]

            new_row = [None] * len(cols)
            new_row[0] = participant
            new_row[1] = len(all_files)

            all_codes = [('0' + file[11:-4] if len(file[11:-4]) < 4 else file[11:-4]) for file in all_files]
            all_codes_sorted = sorted(all_codes)
            all_codes_sorted = list(dict.fromkeys(all_codes_sorted))

            for j, code in enumerate(all_codes_sorted):
                if 'FSL' in code:
                    new_row[-2] = code
                    continue
                if code[0] == '0':
                    code = code[1:]
                fns = glob.glob(os.path.join(participant_dir, '*_' + code + '.PAR'))
                if len(fns) > 1:
                    new_row[-1] = f"WARNING: found {len(fns)} files with pattern {code}.PAR for participant {participant}. Using first one..."
                    print(new_row[-1])
                elif len(fns) == 0:
                    new_row[-1] = f"ERROR: found NO files with pattern {code}.PAR for participant {participant}. Ignoring this file..."
                    print(new_row[-1])
                    continue
                name = fns[0]
                # open and read the protecolline needed for renaming
                with open(name, 'r') as f:
                    protocolline = f.readlines()
                
                line = protocolline[13]
                # Find the first value in the file_type list that exists in protocolline 13 (old identifier)
                match = next((x for x in file_type if x in line), False)
                # Find the index in the new_file_type list that corresponds to the match (new identifier)
                if not match:
                    if new_row[-1] is not None:
                        new_row[-1] = f"{new_row[-1]} | ERROR: no known file type found in ({code}.PAR) file for participant {participant}. Ignoring this file..."
                    else:
                        new_row[-1] = f"ERROR: no known file type found in ({code}.PAR) file for participant {participant}. Ignoring this file..."
                    continue
                elif match == 'B0-map':
                    if not first_b0_found:
                        first_b0_found = True
                        idx = 10
                    else:
                        idx = 11
                        if new_row[-1] is not None:
                            new_row[-1] = f"{new_row[-1]} | NOTE: second B0 map found ({code}.PAR) for participant {participant}."
                        else:
                            new_row[-1] = f"NOTE: second B0 map found ({code}.PAR) for participant {participant}."
                        
                        print(new_row[-1])
                else:
                    idx = file_type.index(match)
                new_row[idx+2] = code

            # print('New row list:')
            # print(new_row)
            df_new_row = pd.DataFrame([new_row], columns=cols)
            # print('New row df:')
            # print(df_new_row)
            df = df.append(df_new_row, ignore_index=True)
            # print('New row df appended:')
            # print(df)
        else:
            print('Error: participant directory not found')
    df.to_csv(participant_info_fn, sep='\t')
    df.to_csv(participant_info_fncsv)