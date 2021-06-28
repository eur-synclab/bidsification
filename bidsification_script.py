import os
import shutil
import sys
import glob
from pathlib import Path

# -----------------
# STEP 0: variables
# -----------------

root_dir = '/exports/fsw/Bendlab/SamenUniek'
raw_sessions = ['test_MCC_ses03-lab', 'test_MCC_ses05-lab']
bids_sessions = ['ses-w03lab', 'ses-w05lab']
file_type = ['3DT1', 'SNAT1', 'SNAT2', 'SNAT3', 'PCG1', 'PCG2', 'PCG3', 'rsfMRI', 'hires', 'B0-map', 'jones30_A', 'jones30_P']
new_file_type = ['T1mri', 'SNAT1', 'SNAT2', 'SNAT3', 'PCG1', 'PCG2', 'PCG3', 'rsfmr', 'T2str', 'Bzero', 'DTIap', 'DTIpa']
config_fn = 'bidsification/config.json'
bids_dir = ''

# --------------------------------
# STEP 1: rename PAR and REC files (in place)
# --------------------------------

for session in raw_sessions:
    raw_data_dir = os.path.join(root_dir, session)

    # From top level directory: MCC_ses03-lab or MCC_ses05-lab
    for root, directories, filenames in os.walk(raw_data_dir):
        if filenames != []:
            for file in filenames:
                # extract the file name and path
                name = root + '/' + file
                name = name.replace("\\", "/")

                if file[-4:] == '.PAR':
                    # open and read the protecolline needed for renaming
                    with open(name, 'r') as f:
                        protocolline = f.readlines()
                    
                    line = protocolline[13]
                    # Find the value in the file_type list that exists in protocolline 13 (old identifier)
                    match = next((x for x in file_type if x in line), False)
                    # Find the index in the new_file_type list that corresponds to the match (new identifier)
                    idx = file_type.index(match)
                    if not match:
                        dontRename = file[:-4]
                    else:

                        rename = raw_data_dir + '/' + root[-10:] + '/' + file[:-4] + '_' + new_file_type[idx] + file[-4:]
                        print('We found a ' + match + ' file: ' + file)
                        # Rename PAR file, if it doesn't already exist
                        if not os.path.isfile(rename):
                            os.rename(name, rename)
                        else:
                            print('WARNING: file ' + rename + ' already exists in the folder! This file will therefore be skipped!')

                        # Find and rename corresponding REC file
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

# --------------------------------
# STEP 2: create BIDS directory structure, copy PAR/REC files
# --------------------------------
# Create top-level pseudobids directory
pseudobids_dir = os.path.join(root_dir, 'test_pseudobids')
if not os.path.exists(pseudobids_dir):
    os.mkdir(pseudobids_dir)
    
for i, session in enumerate(raw_sessions):
    raw_data_dir = os.path.join(root_dir, session)

    # First we'll create a text file into which a list of raw data participants will be written, from directory names
    participants_from_dirs_fn = os.path.join(raw_data_dir, 'participants_from_dirs.txt')
    # If the text file already exists, delete it
    if os.path.isfile(participants_from_dirs_fn):
        os.remove(participants_from_dirs_fn)

    # Read directory names from raw data foler, write to text file
    for participant in os.listdir(raw_data_dir):
        if not participant.startswith('.') and if os.path.isdir(os.path.join(raw_data_dir, participant)):
            print(participant)
            f = open(participants_from_dirs_fn,'a+')
            f.write(participant + '\n')
            f.close()

    # Read participant codes from text file, create bids-like directory structure for every participant
    prefix = 'sub-mcc'
    with open(participants_from_dirs_fn, "r") as participants:
        for line in participants:
            line = line.strip()
            # Subject-level directory
            sub_dir = os.path.join(pseudobids_dir, prefix + str(line[4:10]))
            if os.path.exists(sub_dir):
                os.mkdir(sub_dir)
            # Session-level directory
            session_dir = os.path.join(sub_dir, str(bids_sessions[i]))
            if not os.path.exists(session_dir):
                os.mkdir(session_dir)
            # Copy renamed raw data to pseudobids directory
            raw_sub_dir = os.path.join(root_dir, session, line)
            shutil.copytree(raw_sub_dir, session_dir)

        participants.close()


# -------------------------------------
# STEP 3: run bidsify from command line
# -------------------------------------

# bidsify -c bidsification/config.json -d /exports/fsw/Bendlab/SamenUniek/test_pseudobids -o /exports/fsw/Bendlab/SamenUniek/test_bidsification

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