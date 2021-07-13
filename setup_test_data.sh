# Setup test data:
cd /exports/fsw/Bendlab/SamenUniek
rm -R test_MCC_ses03-lab
rm -R test_MCC_ses05-lab
rm -R test_pseudobids
rm -R test_bidsification
rm -R test_bidsification_nonmerge

mkdir test_MCC_ses03-lab && \
mkdir test_MCC_ses05-lab && \
mkdir test_bidsification

rsync -arv /exports/fsw/Bendlab/SamenUniek/MCC_ses03-lab/SU33000702 /exports/fsw/Bendlab/SamenUniek/test_MCC_ses03-lab/ && \
rsync -arv /exports/fsw/Bendlab/SamenUniek/MCC_ses05-lab/SU35000702 /exports/fsw/Bendlab/SamenUniek/test_MCC_ses05-lab/ && \
rsync -arv /exports/fsw/Bendlab/SamenUniek/MCC_ses05-lab/SU35000602 /exports/fsw/Bendlab/SamenUniek/test_MCC_ses05-lab/ && \
rsync -arv /exports/fsw/Bendlab/SamenUniek/MCC_ses03-lab/SU33000601 /exports/fsw/Bendlab/SamenUniek/test_MCC_ses03-lab/ && \
rsync -arv /exports/fsw/Bendlab/SamenUniek/SU31_bids/data/sub-mcc000702 /exports/fsw/Bendlab/SamenUniek/test_bidsification/ && \
rsync -arv /exports/fsw/Bendlab/SamenUniek/SU31_bids/data/sub-mcc000601 /exports/fsw/Bendlab/SamenUniek/test_bidsification/