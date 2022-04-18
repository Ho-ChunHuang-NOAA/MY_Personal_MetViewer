import sys
import datetime
import shutil
import os 
import subprocess

###METviewer_AWS_scripts_dir = "/gpfs/hps3/emc/global/noscrub/Mallory.Row/VRFY/METviewer_AWS"
METviewer_AWS_scripts_dir = "/gpfs/dell2/emc/modeling/noscrub/Ho-Chun.Huang/METviewer_AWS/script"

### PASSED AGRUEMENTS
mv_database = sys.argv[1]
new_or_add = sys.argv[2]

tmp_data_dir = "/gpfs/dell2/stmp/Ho-Chun.Huang/verif"
### DATABASE INFORMATION
load_xml_file = os.path.join(os.path.join(os.getcwd(), "load_test.xml"))
print("Using "+load_xml_file)
### CREATE DATABASE IF NEEDED AND LOAD DATA
# mv_create_db_on_aws.sh agruments:
#    1 - username
#    2 - database name
# mv_load_to_aws.sh agruments:
#    1 - username
#    2 - base dir
#    3 - XML file
#    4 (opt) - sub dir
if new_or_add == "new":
    print("3) Creating database on METviewer AWS using mv_create_db_on_aws.sh")
    ### subprocess.call([os.path.join(METviewer_AWS_scripts_dir, "mv_create_db_on_aws.sh"), os.environ['USER'].lower(), mv_database])
    print("4) Loading data to METviewer AWS using mv_load_to_aws.sh")
else:
    print("3) Loading data to METviewer AWS using mv_load_to_aws.sh")
subprocess.call([os.path.join(METviewer_AWS_scripts_dir, "mv_load_to_aws.sh"), os.environ['USER'].lower(), tmp_data_dir, load_xml_file])

### CHECK METVIEWER AWS DATABASES
# mv_db_size_on_aws.sh
#    1 - username
if new_or_add == "new":
    print("5) Check METviewer AWS database list using mv_db_size_on_aws.sh")
else:
    print("4) Check METviewer AWS database list using mv_db_size_on_aws.sh")
subprocess.call([os.path.join(METviewer_AWS_scripts_dir, "mv_db_size_on_aws.sh"), os.environ['USER'].lower()])
