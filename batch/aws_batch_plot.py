import sys
import datetime
import shutil
import os 
import subprocess

### PASSED AGRUEMENTS
if len(sys.argv) < 4:
    print("you must set 4 arguments as stat[aod|rmse|...] [day1|day2] start_date end_date")
    sys.exit()
else:
    stat_var = sys.argv[1]
    verf_day = sys.argv[2]
    start_date = sys.argv[3]
    end_date = sys.argv[4]
if stat_var == "aod":
    stat_var = "time_series"
sdate = datetime.datetime(int(start_date[0:4]), int(start_date[4:6]), int(start_date[6:]))
edate = datetime.datetime(int(end_date[0:4]), int(end_date[4:6]), int(end_date[6:]))
file_date_format = "%Y%m%d"
database_date_format = "%Y%m"
database_date = sdate.strftime(database_date_format)

fig_sdate = sdate.strftime(file_date_format)
fig_edate = edate.strftime(file_date_format)
###METviewer_AWS_scripts_dir = "/gpfs/hps3/emc/global/noscrub/Mallory.Row/VRFY/METviewer_AWS"
###METviewer_AWS_scripts_dir = "/gpfs/dell2/emc/verification/noscrub/emc.metplus/METviewer_AWS"
METviewer_AWS_scripts_dir = "/gpfs/hps3/emc/meso/save/"+os.environ['USER']+"/METviewer_AWS"
print(METviewer_AWS_scripts_dir)
region = [ "CONUS", "EAST", "WEST", "NEC", "SEC", "APL",
         "LMV", "MDW", "NMT", "NPL", "SMT", "SPL" ] 
region = [ "EAST", "SEC", "LMV", "GMC" ]
xml_data_dir = "/gpfs/dell2/emc/modeling/noscrub/Ho-Chun.Huang/METviewer_AWS/my_plot_xmls"
xml_gen_python_name = "plot.cmaq_aod_"+stat_var.lower()+".py"
plot_xml_file = "plot_cmaq_aod_"+stat_var.lower()+".xml"
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

os.chdir(tmp_data_dir)
shutil.copy(os.path.join(scripts_dir, batch_script_name), tmp_data_dir)
shutil.copy(os.path.join(xml_data_dir, xml_gen_python_name), tmp_data_dir)
for area in region:
    subprocess.call(["python", xml_gen_python_name, area, area, verf_day.lower(), fig_sdate, fig_edate])
    fig_file=area+"_CMAQ_AOD_"+stat_var.upper()+"_"+verf_day.upper()+"_"+fig_sdate+"_"+fig_edate+".png"

## if os.path.isfile(os.path.join(tmp_data_dir, plot_xml_file)):
    if os.path.isfile(plot_xml_file):
        subprocess.call([os.path.join(".", batch_script_name), os.environ['USER'].lower(), figure_dir, plot_xml_file])
    else:
        print("Can not find"+os.path.join(tmp_data_dir,plot_xml_file))
