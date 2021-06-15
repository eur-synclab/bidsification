import os
import shutil
import sys
import glob
from pathlib import Path


# First, we copy all the Structural (T1-weighted) + Resting State fMRI files
# to a new folder and rename then. In this way, later we can read from the
# filenames what kind of file it is. To do this, we read info from the PAR
# file, based on that info we copy and rename

# First we define the old directory (with the data) and the new dir
# Here it is for the early childhood cohort timepoint 5. We do the same for
# timepoint 1 of the Middle childhood cohort. On jun 10th this was done for
# the 3th and 5th timepoints of the Middle childhood cohort (MCC_ses03-lab
# & MCC_ses05-lab), seperately

#newDir = '/exports/fsw/Bendlab/SamenUniek/SU25_SCANS'
newDir = '/exports/fsw/Bendlab/SamenUniek/MCC_ses03-lab' #LW: is the old and new dir the same folder? 
#newDir = '/exports/fsw/Bendlab/SamenUniek/MCC_ses05-lab'

# check PARs: fMRI SERT + SORT > directly rename
for root, directories, filenames in os.walk(newDir):
    if filenames != []:
        for file in filenames:
            #extract the file name and path
            name = root + '/' + file
            name = name.replace("\\", "/")
            
            
            if file[-4:] == '.PAR':
                #open and read the protecolline needed for renaming
                with open(name, 'r') as f:
                    protocolline = f.readlines()
                
                #check what sort of file it is and setup the rename accordingly
                if '3DT1' in protocolline[13]:
                    rename = newDir + '/' + root[-10:] + '/' + file[:-4] + '_' + 'T1mri' + file[-4:]
                    print('We found a 3DT1 file: ' + file)
                    
  #              elif 'ZELF1' in protocolline[13]:
   #                 rename = newDir + '/' + root[-10:] + '/' + file[:-4] + '_' + 'ZELF1' + file[-4:] 
    #                print('We found a zelf1 file: ' + file)
                
     #           elif 'ZELF2' in protocolline[13]:
      #              rename = newDir + '/' + root[-10:] + '/' + file[:-4] + '_' + 'ZELF2' + file[-4:] 
       #             print('We found a Zelf2 file: ' + file)
                
                elif 'SNAT1' in protocolline[13]:
                    rename = newDir + '/' + root[-10:] + '/' + file[:-4] + '_' + 'SNAT1' + file[-4:]
                    print('We found a snat1 file: ' + file)
                    
                elif 'SNAT2' in protocolline[13]:
                    rename = newDir + '/' + root[-10:] + '/' + file[:-4] + '_' + 'SNAT2' + file[-4:]
                    print('We found a snat2 file: ' + file)

#LW: Added SNAT3, PCG1, PCG2, PCG3     
                elif 'SNAT3' in protocolline[13]:
                    rename = newDir + '/' + root[-10:] + '/' + file[:-4] + '_' + 'SNAT3' + file[-4:]
                    print('We found a snat3 file: ' + file)
           
                elif 'PCG1' in protocolline[13]:
                    rename = newDir + '/' + root[-10:] + '/' + file[:-4] + '_' + 'PCG1' + file[-4:]
                    print('We found a pcg1 file: ' + file)
                    
                elif 'PCG2' in protocolline[13]:
                    rename = newDir + '/' + root[-10:] + '/' + file[:-4] + '_' + 'PCG2' + file[-4:]
                    print('We found a pcg2 file: ' + file)
        
                elif 'PCG3' in protocolline[13]:
                    rename = newDir + '/' + root[-10:] + '/' + file[:-4] + '_' + 'PCG3' + file[-4:]
                    print('We found a pcg3 file: ' + file)
                                        
                elif 'rsfMRI' in protocolline[13]:
                    rename = newDir + '/' + root[-10:] + '/' + file[:-4] + '_' + 'rsfmr' + file[-4:]
                    print('We found a rsfmri file: ' + file)
                
                elif 'hires' in protocolline[13]:
                    rename = newDir + '/' + root[-10:] + '/' + file[:-4] + '_' + 'T2str' + file[-4:]
                    print('We found a T2* file: ' + file)

#LW: DTI files are not included? B0-map, jones30_P_NoCardiac, jones30_A_NoCardiac 
               
                elif 'B0-map' in protocolline[13]:
                    rename = newDir + '/' + root[-10:] + '/' + file[:-4] + '_' + 'rsfmr' + file[-4:]
                    print('We found a B0-map file: ' + file)
                
                elif 'jones30_P_NoCardiac' in protocolline[13]:
                    rename = newDir + '/' + root[-10:] + '/' + file[:-4] + '_' + 'T2str' + file[-4:]
                    print('We found a jones30_P_NoCardiac file: ' + file)
                
                elif 'jones30_A_NoCardiac' in protocolline[13]:
                    rename = newDir + '/' + root[-10:] + '/' + file[:-4] + '_' + 'T2str' + file[-4:]
                    print('We found a jones30_A_NoCardiac file: ' + file)


                else:
                    dontRename = file[:-4]
                    continue
                    
            
                #rename the files in the backup folder (gives warning if the file name already exists in the newDir)
                if not os.path.isfile(rename):
                    os.rename(name, rename)
                else:
                    print('WARNING: file ' + rename + ' already exists in the folder! This file will therefore be skipped!')


# Next, we rename the .REC files based on the corresponding .PAR files

#try this one first:
for root, directories, filenames in os.walk(newDir):
    if filenames != []:
        for file in filenames:
            #extract the file name and path
            name = root + '\\' + file
            name = name.replace("\\", "/")
            
            if file[-4:] == '.PAR':
                namePAR = name
                print(namePAR)
                numberPAR = namePAR[-13:-10]
                print(numberPAR)
                sortPAR = namePAR[-9:-4]
                print(sortPAR)
                
                if sortPAR =='T1mri':
                    nameREC = name[:-10] + '.REC'
                    print(nameREC)
                    renameREC = nameREC[:-4] + '_' + sortPAR + '.REC'
                    
 #               elif sortPAR =='ZELF1':
  #                  nameREC = name[:-10] + '.REC'
   #                 print(nameREC)
    #                renameREC = nameREC[:-4] + '_' + sortPAR + '.REC'
                    
     #           elif sortPAR =='ZELF2':
      #              nameREC = name[:-10] + '.REC'
       #             print(nameREC)
        #            renameREC = nameREC[:-4] + '_' + sortPAR + '.REC'
                    
                elif sortPAR =='SNAT1':
                    nameREC = name[:-10] + '.REC'
                    print(nameREC)
                    renameREC = nameREC[:-4] + '_' + sortPAR + '.REC'
                    
                elif sortPAR =='SNAT2':
                    nameREC = name[:-10] + '.REC'
                    print(nameREC)
                    renameREC = nameREC[:-4] + '_' + sortPAR + '.REC'

#LW: added PCG1, PCG2, PCG3 and SNAT 3 
                elif sortPAR =='SNAT3':
                    nameREC = name[:-10] + '.REC'
                    print(nameREC)
                    renameREC = nameREC[:-4] + '_' + sortPAR + '.REC'

                    
                elif sortPAR =='PCG1':
                    nameREC = name[:-10] + '.REC'
                    print(nameREC)
                    renameREC = nameREC[:-4] + '_' + sortPAR + '.REC'
                    
                elif sortPAR =='PCG2':
                    nameREC = name[:-10] + '.REC'
                    print(nameREC)
                    renameREC = nameREC[:-4] + '_' + sortPAR + '.REC'

                elif sortPAR =='PCG3':
                    nameREC = name[:-10] + '.REC'
                    print(nameREC)
                    renameREC = nameREC[:-4] + '_' + sortPAR + '.REC'

                elif sortPAR =='rsfmr':
                    nameREC = name[:-10] + '.REC'
                    print(nameREC)
                    renameREC = nameREC[:-4] + '_' + sortPAR + '.REC'
                                  
                elif sortPAR =='T2str':
                    nameREC = name[:-10] + '.REC'
                    print(nameREC)
                    renameREC = nameREC[:-4] + '_' + sortPAR + '.REC'

#LW Also added DTI files here

                elif sortPAR =='B0-map':
                    nameREC = name[:-10] + '.REC'
                    print(nameREC)
                    renameREC = nameREC[:-4] + '_' + sortPAR + '.REC'

                elif sortPAR =='jones30_P_NoCardiac':
                    nameREC = name[:-10] + '.REC'
                    print(nameREC)
                    renameREC = nameREC[:-4] + '_' + sortPAR + '.REC'
                                  
                elif sortPAR =='jones30_A_NoCardia':
                    nameREC = name[:-10] + '.REC'
                    print(nameREC)
                    renameREC = nameREC[:-4] + '_' + sortPAR + '.REC'



                else:
                    dontRename = file[:-4]
                    continue
                
                if not os.path.isfile(renameREC):
                    print(renameREC)
                    os.rename(nameREC, renameREC)
                else:
                    print('WARNING: file ' + renameREC + ' already exists in the folder! This file will therefore be skipped!')


###
## FILE CHECK
# import os
# for root, directories, filenames in os.walk(newDir):
#     print(root) 
#     for filename in filenames:
#         print(filename)
#         #break


###
# Turning your data into BIDS format
# Eduard Klapwijk & Philip Brandner, October 21 2019, Edits by Suzanne van de Groep, October 25 2019

# This notebook can be used to convert data with PAR/REC images (MRI image format generated by Philips scanners) into BIDS. The first step of this notebook will show you how to structure your data into pseudoBIDS format. After this, we use the bidsify tool (https://github.com/NILAB-UvA/bidsify) created by Lukas Snoek to convert the pseudoBIDS data into BIDS. 
# All kudos should go to the bidsify creators, this is just a guide that allows the usage of bidsify with an interactive notebook. When turning my own data (Eduard) into BIDS I got great help at Neurohackademy 2019 (https://neurohackademy.org).

# For more information on BIDS visit https://bids.neuroimaging.io and read the Gorgolewski et al. paper about the BIDS format here: https://doi.org/10.1038/sdata.2016.44
# Another useful resource is the BIDS starter kit: https://github.com/bids-standard/bids-starter-kit

# There are multiple tools out there to convert datasets into Nifti (one of the main ones being Heudiconv: https://github.com/nipy/heudiconv). We use bidsify because this is as far as I am aware the only converter capable of working with PAR/REC files.



###
# Step 0: Change directory
# To use this notebook, you first have to navigate to the directory where you have stored the data you want to turn into BIDS. In my case this is 'E:/docker/bids'. In the code below you can change 'E:/docker/bids' to your working directory (i.e., the directory/folder where you have your data). 
# Make sure to put the raw data that you want to convert to BIDS in a directory called 'raw'.
# This will be a subfolder of your base directory. In my case, I put the raw data in folder 'E:/docker/bids/raw'. 
# We also declare a directory called pseudobids (this directory will be created in step 1). We will use this directory to convert the data to pseudoBIDS format. In my case, I called this directory 'E:/docker/bids/pseudobids'. You can replace this in the code below with your own pseudobids directory. 
# Note that you have to change all the directories below that have a red color to make sure that you can use this notebook. 

#base_dir = os.chdir('/exports/fsw/Bendlab/SamenUniek/SU25_bids/')
base_dir = os.chdir('/exports/fsw/Bendlab/SamenUniek/SU31_bids/')
#rawpath = '/exports/fsw/Bendlab/SamenUniek/SU25_SCANS/'
rawpath = '/exports/fsw/Bendlab/SamenUniek/MCC_ses03-lab/'
#bids_path = '/exports/fsw/Bendlab/SamenUniek/SU25_bids/pseudobids'
#LW: Do we make a new SU31_bids folder? E.g. SU33_bids and SU35_bids? Or do we put all the longitudinal data in the SU31_bids folder?
bids_path = '/exports/fsw/Bendlab/SamenUniek/SU31_bids/pseudobids'#LW: Where do you specify the waves? 
dir = os.listdir(rawpath)


##
# Step 1: Use the code below to rename participants and put data in PseudoBIDS format
# You can use the code below to make a file list.txt with all your participant names (1 per line). Assuming that your directories contain all the participant names, this can be easily done.
# Note that we skip hidden directories starting with '.'

# Note that this will only work if you used participant numbers as your directory names within your 'raw' folder.

for partcpnts in dir:
    if not partcpnts.startswith('.'):
        print(partcpnts)
        f = open('list.txt','a+')
        f.write(partcpnts + '\n')
        f.close()

# Check the content of the new txt file. 
# This is especially useful to check if you reran the previous command (i.e., used the command multiple times), which will add the same participants to the list again. We only want every participant to be in the txt file once.

with open('list.txt', 'r') as f:
    print(f.read())

##
# Step 1.1: Make a new directory 'PseudoBIDS' to put the data into something that resembles BIDS format. 
# We have earlier created a directory called 'pseudobids'. By executing the code below, we will use the list.txt file we created with the previous lines of code to make a directory for every participant within pseudobids. 

#prefix = 'sub-ecc'
prefix = 'sub-mcc'
if not os.path.exists(bids_path):
    os.mkdir(bids_path)
 
    with open('list.txt', "r") as prtcpnts:
        for line in prtcpnts:
            line = line.strip()
            os.mkdir(os.path.join(bids_path,(prefix + str(line[4:10]))))
        prtcpnts.close()

os.listdir(bids_path)

##
# Step 1.2: Make a sub-directory for sessions (i.e., runs of the fMRI task)
# Above we gave an example of how to create one session. 
# You can also have more sessions, in that case add ses-02, ses-03 etc (you can delete the '#' for those lines).

#LW this is already there for the mcc 
with open('list.txt', "r") as prtcpnts:
        for line in prtcpnts:
            line = line.strip()
            session_path1 = os.path.join(bids_path,(prefix + str(line[4:10])),str('ses-w05lab'))
            
            if not os.path.exists(session_path1):
                os.makedirs(session_path1)
            
        prtcpnts.close()

# Let's use the code below to check the directories in our bids_path, now we should see a list of participants directories followed by a list of session directories (note that you can check this also in Windows Explorer if you find this helpful). 
for root, directories, filenames in os.walk(bids_path):
    for directory in directories:
         print(directory)


##
# Step 1.3: Use the code below to place every PAR/REC file and all other files you want to convert to BIDS format, in the correct sub-directories (e.g. subject/ses-01 dir). We start with the PARs + RECs: 
# Note that you have to specify the correct names of your t1 scans and functional scans (for each run) below. You can do that by replacing the file names in red. Note that the file names should contain stars ('*') at the start and the end to make sure that the code runs for all participants (i.e. you only specify what the filenames of all participants have in common). 
# Note that this code is still a bit too long, but it works for now (planning to make it more readable soon).

prefix = 'sub-mcc'

for root, directories, filenames in os.walk(rawpath):
    if filenames != []:
        for file in filenames:
            #extract the file name and path
            name = root + '/' + file
            name = name.replace("\\", "/")
            dest_bold = os.path.join(bids_path, prefix + file[4:10] + '/' + 'ses-w05lab' + '/' + \
                                     file[-25:-4] + '_bold' + file[-4:])
            dest = os.path.join(bids_path, prefix + file[4:10] + '/' + 'ses-w05lab' + '/')

#LW: And I have added the DTI scans here
            if file[-9:-4] == 'PCG1' or file[-9:-4] == 'PCG2' or file[-9:-4] == 'PCG3' \
            or file[-9:-4] == 'SNAT1' or file[-9:-4] == 'SNAT2' or file[-9:-4] == 'SNAT3'\
            or file[-9:-4] == 'rsfmr' or file[-9:-4] == 'B0-map' or file[-9:-4] == 'jones30_P_NoCardiac'\
            or file[-9:-4] == 'jones30_A_NoCardiac':
                if not os.path.isfile(dest_bold):
                    print(dest_bold)
                    shutil.copy(name, dest_bold)
            elif file[-9:-4] == 'T1mri' or file[-9:-4] == 'T2str':
                if not os.path.isfile(dest):
                    print(dest)
                    shutil.copy(name, dest)
                else:
                    print('WARNING: file ' + dest + ' already exists in the folder! This file will therefore be skipped!')

# We can check the files in the pseudobids directories to see if this went well:
for root, directories, filenames in os.walk(bids_path):
    for directory in directories:
        print(directory)
    for filename in filenames:    
        print(filename)

for root, directories, filenames in os.walk(bids_path):
    for directory in directories:
        for filename in filenames:
            if not directory.startswith('.'):
                print(os.path.join(directory,filename))


## 
# Step 2: Use BIDSify to turn pseudoBIDS data into BIDS format

# For this step we first have to install bidsify and its dependencies. 

# This is what we have to do:
# 1. Install bidsify:
# pip install bidsify
# 2. Install / check dependencies:
# dcm2niix (release v1.0.20181125 or newer)
# nibabel
# scipy
# numpy
# joblib (for parallelization)
# pandas
# 3. Make a config-file in either the json or YAML format. 

# Step 2.1: Install bidsify + most dependencies (see for more info https://github.com/NILAB-UvA/bidsify)
pip install bidsify
# Step 2.2: Install dcm2niix
#### installing dcm2niix on Shark:
cd /home/jupyter/bin
git clone https://github.com/rordenlab/dcm2niix.git
cd dcm2niix
mkdir build && cd build
# to avoid the error when using make .., do: 
cmake -DUSE_STATIC_RUNTIME=OFF ..
make
# finally copy binary to user/bin:
cp dcmniix etklapwijk/bin


##
# Step 2.3: Make a config-file in either the json or YAML format 
# In order to run the bidsify script we have to make a config-file in either the json or YAML format. This file contains information about the experiment, such as the types and names of the anatomical and functional scans. The bidsify script needs this information to strucure the data according to the BIDS format. You will have to create this json file yourself as it is specific for each functional MRI task. You can find an example here: https://github.com/eduardklap/braindev-nipype/blob/master/config.json.
# We'll go for json. We can either use R package 'jsonlite' or use http://jsoneditoronline.org. See https://github.com/NILAB-UvA/bidsify#the-config-file for details.
# Place the file in the current directory --> see example ./config.json

#with open('/exports/fsw/Bendlab/SamenUniek/SU25_bids/config.json', 'r') as config:
with open('/exports/fsw/Bendlab/SamenUniek/SU31_bids/config.json', 'r') as config:
    print(config.read())


##
# Step 2.4: Run Bidsify command to turn data into BIDS format
# see https://github.com/NILAB-UvA/bidsify#how-does-it-work for details
# To run the bidsify script, you have to replace the path to your .json file and pseudobids directory below with the path to your own json file and pseudobids directory. 

#!bidsify -c /exports/fsw/Bendlab/SamenUniek/SU25_bids/config.json -d /exports/fsw/Bendlab/SamenUniek/SU25_bids/pseudobids
bidsify -c /exports/fsw/Bendlab/SamenUniek/SU31_bids/config.json -d /exports/fsw/Bendlab/SamenUniek/SU31_bids/pseudobids

# We rename the T2w to T2star (for more clarity, and according to bids specifications)

#for root, directories, filenames in os.walk('/exports/fsw/Bendlab/SamenUniek/SU25_SCANS/bids'):
for root, directories, filenames in os.walk('/exports/fsw/Bendlab/SamenUniek/SU31_SCANS/bids'):
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


##
# Step 2.5: If everything went well, we now have a new directory called 'bids' with our data in BIDS format
# Let's have a look:

#for root, directories, filenames in os.walk('/exports/fsw/Bendlab/SamenUniek/SU25_SCANS/bids'):
for root, directories, filenames in os.walk('/exports/fsw/Bendlab/SamenUniek/SU31_SCANS/bids'):
    for directory in directories:
        print(directory)
    for filename in filenames:
        print(filename)

# To add here: BIDS validator in the notebook to validate whether everything is correct