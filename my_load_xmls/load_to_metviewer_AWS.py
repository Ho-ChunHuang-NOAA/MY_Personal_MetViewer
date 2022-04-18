import sys
import datetime
import shutil
import os 
import subprocess

METviewer_AWS_scripts_dir = "/gpfs/hps3/emc/global/noscrub/Mallory.Row/VRFY/METviewer_AWS"

### PASSED AGRUEMENTS
mv_database = sys.argv[1]
new_or_add = sys.argv[2]
start_date = sys.argv[3]
end_date = sys.argv[4]

### DATABASE INFORMATION
print("=============== METviewer AWS database "+mv_database+" ===============")
if mv_database == "mv_gfs_grid2grid_vsdb":
    mv_desc = "Grid-to-grid VSDB data for operational GFS"
    mv_group = "NOAA NCEP"
    data_dir = "/gpfs/hps3/emc/global/noscrub/Fanglin.Yang/stat/vsdb_data"
    models = [ "gfs" ]
    subdirs = [ "anom/00Z", "pres/00Z", "sfc/00Z", 
                "anom/06Z", "pres/06Z", "sfc/06Z",
                "anom/12Z", "pres/12Z", "sfc/12Z",
                "anom/18Z", "pres/18Z", "sfc/18Z" ]
    file_date_format = "%Y%m%d"
    file_format_list = [ "MODEL_DATE.vsdb" ]
    met_version = "6.1"
    date_inc = datetime.timedelta(hours=24)
elif mv_database == "mv_gfs_grid2obs_vsdb":
    mv_desc = "Grid-to-obs VSDB data for operational GFS"
    mv_group = "NOAA NCEP"
    data_dir = "/gpfs/hps3/emc/global/noscrub/Fanglin.Yang/stat/vsdb_data/grid2obs"
    models = [ "gfs" ]
    subdirs = [ "00Z", "06Z", 
                "12Z", "18Z" ]
    file_date_format = "%Y%m%d"
    file_format_list = [ "MODEL_air_DATE.vsdb", "MODEL_sfc_DATE.vsdb" ]
    met_version = "6.1"
    date_inc = datetime.timedelta(hours=24)
elif mv_database == "mv_gfs_grid2grid_metplus":
    mv_desc = "Grid-to-grid METplus data for operational GFS"
    mv_group = "NOAA NCEP"
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
    for subdir in subdirs:
        date = sdate
        while date <= edate:
            file_date = date.strftime(file_date_format)
            for file_format in file_format_list:
                file_name = file_format.replace('MODEL', model).replace('DATE', file_date)
                full_file_name = os.path.join(data_dir, subdir, model, file_name)
                link_file_name_prefix = file_name.split(".")[0]
                link_file_name_suffix = file_name.split(".")[1]
                link_file_name = link_file_name_prefix+"_"
                for subdir_to_filename in subdir.split("/"):
                    link_file_name = link_file_name+subdir_to_filename
                link_file_name = link_file_name+"."+link_file_name_suffix
                full_link_file_name = os.path.join(os.getcwd(), tmp_data_dir, link_file_name)
                if os.path.exists(full_file_name):
                    print("Linking "+full_file_name+" as "+full_link_file_name)
                    subprocess.call(['ln', '-sf', full_file_name, full_link_file_name])
                else:
                    print(full_file_name+" does not exist")
            date = date + date_inc

### CREATE LOAD XML
load_xml_file = os.path.join(os.path.join(os.getcwd(), "load_"+mv_database+".xml"))
print("2) Creating load xml "+load_xml_file)
if new_or_add == "new":
    drop_index = "false"
else:
    drop_index = "true"
if os.path.exists(load_xml_file):
    os.remove(load_xml_file)
with open(load_xml_file, 'a') as xml:
    xml.write("<load_spec>\n")
    xml.write("  <connection>\n")
    xml.write("    <host>metviewer-dev-cluster.cluster-czbts4gd2wm2.us-east-1.rds.amazonaws.com:3306</host>\n")
    xml.write("    <database>"+mv_database+"</database>\n")
    xml.write("    <user>rds_user</user>\n")
    xml.write("    <password>rds_pwd</password>\n")
    xml.write("    <management_system>aurora</management_system>\n")
    xml.write("  </connection>\n")
    xml.write("\n")
    xml.write("  <met_version>V"+met_version+"</met_version>\n")
    xml.write("\n")
    xml.write("  <verbose>true</verbose>\n")
    xml.write("  <insert_size>1</insert_size>\n")
    xml.write("  <mode_header_db_check>true</mode_header_db_check>\n")
    xml.write("  <stat_header_db_check>true</stat_header_db_check>\n")
    xml.write("  <drop_indexes>"+drop_index+"</drop_indexes>\n")
    xml.write("  <apply_indexes>true</apply_indexes>\n")
    xml.write("  <load_stat>true</load_stat>\n")
    xml.write("  <load_mode>true</load_mode>\n")
    xml.write("  <load_mpr>true</load_mpr>\n")
    xml.write("  <load_orank>true</load_orank>\n")
    xml.write("  <force_dup_file>false</force_dup_file>\n")
    xml.write("  <group>"+mv_group+"</group>\n")
    xml.write("  <description>"+mv_desc+"</description>\n")
    xml.write("  <load_files>\n")
for model in models:
    for subdir in subdirs:
        date = sdate
        while date <= edate:
            file_date = date.strftime(file_date_format)
            for file_format in file_format_list:
                file_name = file_format.replace("MODEL", model).replace("DATE", file_date)
                link_file_name_prefix = file_name.split(".")[0]
                link_file_name_suffix = file_name.split(".")[1]
                link_file_name = link_file_name_prefix+"_"
                for subdir_to_filename in subdir.split("/"):
                    link_file_name = link_file_name+subdir_to_filename
                link_file_name = link_file_name+"."+link_file_name_suffix
                full_link_file_name = os.path.join(os.getcwd(), tmp_data_dir, link_file_name)
                if os.path.exists(full_link_file_name):
                    with open(load_xml_file, 'a') as xml:
                        xml.write("    <file>/base_dir/"+link_file_name+"</file>\n")
            date = date + date_inc
with open(load_xml_file, 'a') as xml:
    xml.write("  </load_files>\n")
    xml.write("\n")
    xml.write("</load_spec>")

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
    subprocess.call([os.path.join(METviewer_AWS_scripts_dir, "mv_create_db_on_aws.sh"), os.environ['USER'].lower(), mv_database])
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
shutil.rmtree(tmp_data_dir)
