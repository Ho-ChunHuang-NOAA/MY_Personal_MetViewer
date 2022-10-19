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
###METviewer_AWS_scripts_dir = "/lfs/h2/emc/vpppg/save/"+os.environ['USER']+"/METviewer_AWS"
METviewer_AWS_scripts_dir = "/lfs/h2/emc/vpppg/save/"+os.environ['USER']+"/METviewer_AWS"
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
xml_data_dir = "/lfs/h2/emc/vpppg/save/"+os.environ['USER']+"/METviewer_AWS/my_plot_xmls"
xml_gen_python_name = "plot.hysplit_dust_"+stat_var.lower()+".py"
plot_xml_file = "plot_hysplit_dust_"+stat_var.lower()+".xml"
scripts_dir = "/lfs/h2/emc/vpppg/save/"+os.environ['USER']+"/METviewer_AWS/script"
batch_script_name = "mv_batch_on_aws.sh"
tmp_data_dir = "/lfs/h2/emc/stmp/"+os.environ['USER']+"/run_batch_plot_"+stat_var.lower()
figure_dir = "/lfs/h2/emc/stmp/"+os.environ['USER']+"/figure_"+stat_var.lower()+"_"+database_date
if os.path.exists(figure_dir):
    shutil.rmtree(figure_dir)
os.makedirs(figure_dir)
if os.path.exists(tmp_data_dir):
    shutil.rmtree(tmp_data_dir)
os.makedirs(tmp_data_dir)
subprocess.call("chmod 644 *", shell=True)

os.chdir(tmp_data_dir)
shutil.copy(os.path.join(scripts_dir, batch_script_name), tmp_data_dir)
shutil.copy(os.path.join(xml_data_dir, xml_gen_python_name), tmp_data_dir)
for area in region:
    for verf_day in vday: 
        for verf_cycle in run_cycle: 
            subprocess.call(["python", xml_gen_python_name, area, area, verf_day.lower(), fig_sdate, fig_edate, verf_cycle])
            fig_file=area+"_HYSPLIT_DUST_"+stat_var.upper()+"_"+verf_day.upper()+"_"+verf_cycle+"_"+database_date+".png"

## if os.path.isfile(os.path.join(tmp_data_dir, plot_xml_file)):
            if os.path.isfile(plot_xml_file):
                subprocess.call([os.path.join(".", batch_script_name), os.environ['USER'].lower(), figure_dir, plot_xml_file])
            else:
                print("Can not find"+os.path.join(tmp_data_dir,plot_xml_file))
os.chdir(figure_dir)
subprocess.call("chmod 644 *", shell=True)
parta=os.path.join("/usr", "bin", "scp")
partb=os.path.join("hchuang@rzdm:", "home", "www", "emc", "htdocs", "mmb", "hchuang", "web", "fig", database_year, database_date)
subprocess.call(['scp -p * '+partb], shell=True)
