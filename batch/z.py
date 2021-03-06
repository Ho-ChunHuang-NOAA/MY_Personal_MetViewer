import sys
import datetime
import shutil
import os 
import subprocess

### PASSED AGRUEMENTS
if len(sys.argv) < 4:
    print("you must set 4 arguments as stat[aod|rmse|...] [all|day1|day2] start_date end_date")
    sys.exit()
else:
    stat_var = sys.argv[1]
    flag_vday = sys.argv[2]
    start_date = sys.argv[3]
    end_date = sys.argv[4]
if stat_var == "aod":
    stat_var = "time_series"
sdate = datetime.datetime(int(start_date[0:4]), int(start_date[4:6]), int(start_date[6:]))
edate = datetime.datetime(int(end_date[0:4]), int(end_date[4:6]), int(end_date[6:]))
file_date_format = "%Y%m%d"
database_date_format = "%Y%m"
database_year_format = "%Y"
database_date = sdate.strftime(database_date_format)
database_year = sdate.strftime(database_year_format)

fig_sdate = sdate.strftime(file_date_format)
fig_edate = edate.strftime(file_date_format)
###METviewer_AWS_scripts_dir = "/gpfs/dell2/emc/verification/noscrub/emc.metplus/METviewer_AWS"
METviewer_AWS_scripts_dir = "/gpfs/dell2/emc/modeling/noscrub/"+os.environ['USER']+"/METviewer_AWS"
print(METviewer_AWS_scripts_dir)
if flag_vday == "all":
   vday=[ "day1", "day2" ]
elif flag_vday == "day1":
   vday=[ "day1" ]
elif flag_vday == "day2":
   vday=[ "day2" ]
else:
    print("verification verify day "+vday+" not recongized.")
    exit()
run_cycle = [ "06Z", "12Z" ]
region = [ "FULL", "G236", "G245", "G246" ]
xml_data_dir = "/gpfs/dell2/emc/modeling/noscrub/Ho-Chun.Huang/METviewer_AWS/my_plot_xmls"
xml_gen_python_name = "plot.hysplit_dust_"+stat_var.lower()+".py"
plot_xml_file = "plot_hysplit_dust_"+stat_var.lower()+".xml"
scripts_dir = "/gpfs/dell2/emc/modeling/noscrub/"+os.environ['USER']+"/METviewer_AWS/script"
batch_script_name = "mv_batch_on_aws.sh"
tmp_data_dir = "/gpfs/dell2/stmp/Ho-Chun.Huang/run_batch_plot_"+stat_var.lower()
figure_dir = "/gpfs/dell2/stmp/Ho-Chun.Huang/figure_"+stat_var.lower()+"_"+database_date
if os.path.exists(figure_dir):
    shutil.rmtree(figure_dir)
os.makedirs(figure_dir)
if os.path.exists(tmp_data_dir):
    shutil.rmtree(tmp_data_dir)
os.makedirs(tmp_data_dir)
subprocess.call("chmod 644 *", shell=True)

os.chdir(figure_dir)
subprocess.call("chmod 644 *", shell=True)
parta=os.path.join("/usr", "bin", "scp")
partb=os.path.join("hchuang@rzdm:", "home", "www", "emc", "htdocs", "mmb", "hchuang", "web", "fig", database_year, database_date)
subprocess.call(['scp -p * '+partb], shell=True)
