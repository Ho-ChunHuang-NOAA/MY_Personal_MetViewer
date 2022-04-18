import sys
import datetime
import shutil
import os 
import subprocess

###METviewer_AWS_scripts_dir = "/gpfs/hps3/emc/global/noscrub/Mallory.Row/VRFY/METviewer_AWS"
METviewer_AWS_scripts_dir = "/gpfs/hps3/emc/meso/save/Ho-Chun.Huang/METviewer_AWS"

### PASSED AGRUEMENTS
mv_database = sys.argv[1]
new_or_add = sys.argv[2]
start_date = sys.argv[3]
end_date = sys.argv[4]
exp = sys.argv[5]

### DATABASE INFORMATION
print("=============== METviewer AWS database "+mv_database+" ===============")
if mv_database == "mv_aqm_hchuang":
    mv_desc = "Grid-to-obs VSDB data for operational and experimental CMAQ"
    mv_group = "NCEP_hcHuang"
    data_dir = "/gpfs/td3/emc/meso/noscrub/Ho-Chun.Huang/com/verf/para/vsdb/gridtobs"
    models = [ "cmaq"+exp ]
    ## subdirs = [ "cmaqpara82", "cmaqpara87h" ]
    file_date_format = "%Y%m%d"
    file_format_list = [ "MODEL_DATE.vsdb" ]
    met_version = "8.1.2"
    date_inc = datetime.timedelta(hours=24)
elif mv_database == "mv_hysplit_hchuang":
    mv_desc = "Grid-to-grid VSDB data for operational HYSPLIT Smoke and Dust"
    mv_group = "NCEP_hcHuang"
    data_dir = "/gpfs/td3/emc/meso/noscrub/Ho-Chun.Huang/com/verf/para/vsdb/gridtgrid"
    models = [ "smokecspara82h" ]
    ## subdirs = [ "00Z", "06Z", 
    ##             "12Z", "18Z" ]
    file_date_format = "%Y%m%d"
    file_format_list = [ "MODEL_DATE.vsdb", "MODEL_DATE.vsdb" ]
    met_version = "6.1"
    date_inc = datetime.timedelta(hours=24)
elif mv_database == "mv_gfs_grid2grid_metplus":
    mv_desc = "Grid-to-grid METplus data for operational GFS"
    mv_group = "NCEP_hcHuang"
    data_dir = "/gpfs/dell2/emc/verification/noscrub/Mallory.Row/archive/metplus_data/by_VSDB/grid2grid"
    models = [ "gfs" ]
    subdirs = [ "anom/00Z", "pres/00Z", "sfc/00Z",
                "anom/06Z", "pres/06Z", "sfc/06Z",
                "anom/12Z", "pres/12Z", "sfc/12Z",
                "anom/18Z", "pres/18Z", "sfc/18Z" ]
    file_date_format = "%Y%m%d"
    file_format_list = [ "MODEL_DATE.stat" ]
    met_version = "8.1"
    date_inc = datetime.timedelta(hours=24)
else:
    print(mv_database+" not recongized.")
    exit()
### COPY DATA TO TMP DIRECTORY TO AVOID
### COPYING UNNCESSARY FILES
sdate = datetime.datetime(int(start_date[0:4]), int(start_date[4:6]), int(start_date[6:]))
edate = datetime.datetime(int(end_date[0:4]), int(end_date[4:6]), int(end_date[6:]))
tmp_data_dir = os.path.join(os.getcwd(), 'tmp_data_'+mv_database)
print("1) Linking data from "+data_dir+" to "+os.path.join(os.getcwd(), tmp_data_dir))
if os.path.exists(tmp_data_dir):
    shutil.rmtree(tmp_data_dir)
os.makedirs(tmp_data_dir)
for model in models:
    print("Model = "+model)
