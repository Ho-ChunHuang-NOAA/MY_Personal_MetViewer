import sys
import datetime
import shutil
import os
import subprocess
import fnmatch

current=os.getcwd()
METviewer_AWS_scripts_dir = "/gpfs/dell2/emc/modeling/noscrub/Ho-Chun.Huang/METviewer_AWS/script"
MOIDS_dust_obs_dir = "/gpfs/dell2/emc/modeling/noscrub/Ho-Chun.Huang/aod_dust/conc/aquamodis."
MET_verif_out_dir = "/gpfs/dell2/emc/modeling/noscrub/Ho-Chun.Huang/com/verif/prod/hysplitdust."
tmp_data_dir="/gpfs/dell2/stmp/Ho-Chun.Huang/working/check_fcst_lead"
if os.path.exists(tmp_data_dir):
    shutil.rmtree(tmp_data_dir)
os.makedirs(tmp_data_dir)

obs_fhead = "MYDdust.aod_conc.v6.3.4."
obs_ftail = ".grib"
stat_var = "csi"
plot_var = "csi"

### if os.path.getsize(find_tmp) == 0:
###     print(find_tmp+' File is empty')
### else:
###     print(find_tmp+' File is not empty')
verf_day_id = "day2"
start_date = "20190801"
end_date = "20190831"
sdate = datetime.datetime(int(start_date[0:4]), int(start_date[4:6]), int(start_date[6:]), 00)
edate = datetime.datetime(int(end_date[0:4]), int(end_date[4:6]), int(end_date[6:]), 23)
date_inc = datetime.timedelta(hours=24)
hour_inc = datetime.timedelta(hours=1)
val_date_format = "%Y-%m-%d %H:%M:%S"
lbl_date_format = "%m-%d %H"
title_date_format = "%Y%m%d"
title_hour_format = "%H"
database_date_format = "%Y%m"
database_date = sdate.strftime(database_date_format)

verf_cycle_id =  "06z"
if verf_cycle_id == "12Z":
   hour_cycle=12
elif verf_cycle_id == "06z":
   hour_cycle=6
else:
    print("verification cycle hour "+verf_cycle_id+" not recongized.")
    exit()
if verf_day_id == "day1":
    vhour_beg = 1
    vhour_end = 24
elif verf_day_id == "day2":
    vhour_beg = 25
    vhour_end = 48
else:
    print("verification day "+verf_day_id+" not recongized.")
    exit()
vhour_inc = 1
print("{0:0>2}".format(vhour_beg)+"  "+str(vhour_end))
fcst_valid_file = os.path.join(os.path.join(os.getcwd(), "fcst_valid."+start_date[0:6]+plot_var+".xml"))
print("2) Creating plot xml "+fcst_valid_file)
if os.path.exists(fcst_valid_file):
    os.remove(fcst_valid_file)
with open(fcst_valid_file, 'a') as xml:
    xml.write("                </set>\n")
    xml.write("            </field>\n")
    xml.write("            <field equalize=\"false\" name=\"fcst_lead\">\n")
    xml.write("                <set name=\"fcst_lead_1\">\n")
    date = sdate
    while date <= edate:
        verifout=MET_verif_out_dir+date.strftime(title_date_format)+"/hysplitdust_prod_"+date.strftime(title_date_format)+".stat.tar"
        if os.path.isfile(verifout):
            shutil.copy(verifout, tmp_data_dir)
            os.chdir(tmp_data_dir)
            subprocess.call(["/usr/bin/tar", "-xf", verifout])
        else:
            print("Can not find "+verifout)
        date = date + date_inc
    os.chdir(tmp_data_dir)
    vhour = vhour_beg
    while vhour <= vhour_end:
        search_index="*F"+"{0:0>2}".format(vhour)+"*"
        for file in os.listdir(tmp_data_dir):
            if fnmatch.fnmatch(file, search_index):
                xml.write("                    <val>"+str(vhour)+"0000</val>\n")
                break
        vhour = vhour + vhour_inc
    xml.write("                </set>\n")
    xml.write("            </field>\n")
    xml.write("            <field equalize=\"false\" name=\"fcst_init_beg\">\n")
    xml.write("                <set name=\"fcst_init_beg_2\">\n")
    date = sdate - date_inc
    date = date  - date_inc
    while date <= edate:
        if date.hour == hour_cycle:
            val_date = date.strftime(val_date_format)
            xml.write("                    <val>"+val_date+"</val>\n")
        date = date + hour_inc
    xml.write("                </set>\n")
    xml.write("            </field>\n")
    xml.write("            <field equalize=\"false\" name=\"fcst_valid_beg\">\n")
    xml.write("                <set name=\"fcst_valid_beg_3\">\n")
    date = sdate
    while date <= edate:
        obs_dir=MOIDS_dust_obs_dir+date.strftime(title_date_format)
        if os.path.exists(obs_dir):
            obsfile=os.path.join(obs_dir, obs_fhead+date.strftime(title_date_format)+".hr"+date.strftime(title_hour_format)+obs_ftail)
            if os.path.isfile(obsfile):
                val_date = date.strftime(val_date_format)
                label_date = date.strftime(lbl_date_format)
                xml.write("                    <val>"+val_date+"</val>\n")
        else:
            print("Can not find "+obs_dir)
        date = date + hour_inc
    xml.write("                </set>\n")
    xml.write("            </field>\n")
    xml.write("        </plot_fix>\n")

