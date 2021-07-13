import os
import shutil
import sys
import glob
from pathlib import Path
import pandas as pd

# -----------------
# STEP 0: variables
# -----------------

root_dir = '/exports/fsw/Bendlab/SamenUniek'
raw_sessions = ['test_MCC_ses03-lab', 'test_MCC_ses05-lab']
bids_sessions = ['ses-w03lab', 'ses-w05lab']
file_type = ['3DT1', 'SNAT1', 'SNAT2', 'SNAT3', 'PCG1', 'PCG2', 'PCG3', 'rsfMRI', 'hires', 'B0-map_RS', 'B0-map', 'B0-map', 'B0-map', 'jones30_A', 'jones30_P']
new_file_type = ['T1mri', 'bold_SNAT1', 'bold_SNAT2', 'bold_SNAT3', 'bold_PCG1', 'bold_PCG2', 'bold_PCG3', 'bold_rsfmr', 'T2str', 'B0RS', 'Bzero1', 'Bzero2', 'Bzero3', 'DTIap', 'DTIpa', 'unknown_type', 'log']
cols = ['participant','nr_files'] + new_file_type
config_fn = 'bidsification/config.json'
bids_dir = ''
prefix = 'sub-mcc'
# Create top-level pseudobids directory
pseudobids_dir = os.path.join(root_dir, 'test_pseudobids')
if not os.path.exists(pseudobids_dir):
    os.mkdir(pseudobids_dir)

# --------------------------------
# STEP 1: Loop through sessions, participants:
# - rename PAR and REC files (in place)
# - copy participant files to new pseudobids directory structure
# --------------------------------
for i, session in enumerate(raw_sessions):
    raw_data_dir = os.path.join(root_dir, session)
    print(raw_data_dir)

    # Log file
    conversion_log_fn = os.path.join(root_dir, session + '_conversion_log.csv')
    # If the log file already exists, read contents into dataframe. If not, create dataframe.
    if os.path.isfile(conversion_log_fn):
        df = pd.read_csv(conversion_log_fncsv)
    else:
        df = pd.DataFrame(columns=cols)
    
    # Read directory names from raw data foler, write to text file
    for p, participant in enumerate(os.listdir(raw_data_dir)):

        # Check in log-file if conversion has already been done.
        # If done, skip.
        if participant in df['participant'].tolist():
            print(f"Participant {participant} already converted. Skipping...")
            continue

        # Access participant_dir, continue if it exists
        participant_dir = os.path.join(raw_data_dir, participant)
        first_b0_found = False
        b0_found = 0
        fsl_found = False
        if os.path.isdir(participant_dir):
            print(f"{str(p).zfill(3)}: {participant}")

            all_files = [name for name in os.listdir(participant_dir) if os.path.isfile(os.path.join(participant_dir, name))]

            new_row = [None] * len(cols)
            new_row[0] = participant
            new_row[1] = len(all_files)

            all_codes = [('0' + file[11:-4] if len(file[11:-4]) < 4 else file[11:-4]) for file in all_files] # assumes unique codes
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
                    if new_row[-1] is not None:
                        new_row[-1] = f"{new_row[-1]} | WARNING: found {len(fns)} files with pattern {code}.PAR for participant {participant}. Using first one..."
                    else:
                        new_row[-1] = f"WARNING: found {len(fns)} files with pattern {code}.PAR for participant {participant}. Using first one..."
                    print(new_row[-1])
                    continue
                elif len(fns) == 0:
                    if new_row[-1] is not None:
                        new_row[-1] = f"{new_row[-1]} | ERROR: found NO files with pattern {code}.PAR for participant {participant}. Ignoring this file..."
                    else:
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
                    b0_found = b0_found + 1
                    idx = 9 + b0_found
                    if new_row[-1] is not None:
                        new_row[-1] = f"{new_row[-1]} | NOTE: B0 map found ({code}.PAR) for participant {participant}."
                    else:
                        new_row[-1] = f"NOTE: B0 map found ({code}.PAR) for participant {participant}."
                    print(new_row[-1])
                else:
                    idx = file_type.index(match)
                
                new_row[idx+2] = code

                # Rename PAR file, if it doesn't already exist
                if new_file_type[idx] in name:
                    print('WARNING: renamed file ' + name + ' already exists in the folder! This file will therefore be skipped!')
                else:
                    rename = name[:-4] + '_' + new_file_type[idx] + name[-4:]
                    os.rename(name, rename)
                    # Rename REC file, if it doesn't already exist
                    nameREC = name[:-4] + '.REC'
                    if os.path.isfile(nameREC):
                        renameREC = name[:-4] + '_' + new_file_type[idx] + '.REC'
                        # If the renameREC file does not yet exist, proceed with renaming
                        if not os.path.isfile(renameREC):
                            os.rename(nameREC, renameREC)
                        else:
                            print('WARNING: file ' + renameREC + ' already exists in the folder! This file will therefore be skipped!')
                    else:
                        print('ERROR: corresponding REC file not found for: ' + name)

            # Create bids-like directory structure for participant
            sub_dir = os.path.join(pseudobids_dir, prefix + str(participant[4:10]))
            if not os.path.exists(sub_dir):
                os.mkdir(sub_dir)
            # Session-level directory
            session_dir = os.path.join(sub_dir, str(bids_sessions[i]))
            # Copy renamed raw data to pseudobids directory
            if os.path.exists(session_dir):
                shutil.copy(participant_dir, session_dir)
            else:
                shutil.copytree(participant_dir, session_dir)

            # Add participant info to log file
            df_new_row = pd.DataFrame([new_row], columns=cols)
            df = df.append(df_new_row, ignore_index=True)
            df.to_csv(conversion_log_fn)
        else:
            print('Error: participant directory not found for ' + participant)


# -------------------------------------
# STEP 3: run bidsify from command line
# -------------------------------------

# bidsify -c bidsification/config.json -d /exports/fsw/Bendlab/SamenUniek/test_pseudobids -o /exports/fsw/Bendlab/SamenUniek/test_bidsification_nonmerge

# bidsify -c /home/jsheunis/bidsification/config.json -d /exports/fsw/Bendlab/SamenUniek/test_MCC_ses03-lab/SU33000702/renamed_files -o /exports/fsw/Bendlab/SamenUniek/test_MCC_ses03-lab/SU33000702/bidsify_test

# bidsify -c /home/jsheunis/bidsification/config.json -d /exports/fsw/Bendlab/SamenUniek/test_MCC_ses05-lab/SU35075901/renamed -o /exports/fsw/Bendlab/SamenUniek/test_MCC_ses05-lab/SU35075901/bidsify_test
# /exports/fsw/Bendlab/SamenUniek/test_MCC_ses05-lab/SU35075901/
# -------------------------------------
# STEP 4: rename T2w to T2star
# -------------------------------------