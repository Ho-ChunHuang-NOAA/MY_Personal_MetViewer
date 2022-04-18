import sys
import datetime
import shutil
import os 
import subprocess

### PASSED AGRUEMENTS
if len(sys.argv) < 4:
    print("you must set 4 arguments as stat[pmave|rmse|...] [day1|day2|day3] start_date end_date event_equal[optional]")
    sys.exit()
else:
    stat_var = sys.argv[1]
    flag_vday = sys.argv[2]
    start_date = sys.argv[3]
    end_date = sys.argv[4]
if stat_var == "pmave":
    stat_var = "time_series"
if len(sys.argv) > 5:
    event_equal_flag = sys.argv[5]
else:
    event_equal_flag = "true"
    print("the evn equalizer is set to true, if you want to change it please add true/false for the 5th argument")
sdate = datetime.datetime(int(start_date[0:4]), int(start_date[4:6]), int(start_date[6:]))
edate = datetime.datetime(int(end_date[0:4]), int(end_date[4:6]), int(end_date[6:]))
file_date_format = "%Y%m%d"
database_date_format = "%Y%m"
database_year_format = "%Y"
database_date = sdate.strftime(database_date_format)
database_year = sdate.strftime(database_year_format)

fig_sdate = sdate.strftime(file_date_format)
fig_edate = edate.strftime(file_date_format)
###METviewer_AWS_scripts_dir = "/gpfs/hps3/emc/global/noscrub/Mallory.Row/VRFY/METviewer_AWS"
###METviewer_AWS_scripts_dir = "/gpfs/dell2/emc/verification/noscrub/emc.metplus/METviewer_AWS"
METviewer_AWS_scripts_dir = "/gpfs/dell2/emc/modeling/noscrub/"+os.environ['USER']+"/METviewer_AWS"
print(METviewer_AWS_scripts_dir)
if flag_vday == "all":
   vday=[ "day1", "day2" ]
elif flag_vday == "day1":
   vday=[ "day1" ]
elif flag_vday == "day2":
   vday=[ "day2" ]
elif flag_vday == "day3":
   vday=[ "day3" ]
else:
    print("verification verify day "+vday+" not recongized.")
    exit()
## For diurnal cycle plot fix day as the # of fcst day
if stat_var == "rmsedl":
   vday=[ "day2" ]
elif stat_var == "medl":
   vday=[ "day2" ]
run_cycle = [ "06Z", "12Z" ]
region = [ "FULL", "CONUS", "EAST", "WEST", "NEUS", "SEUS", "NWUS", "SWUS", "NEC", "SEC", "APL",
           "GMC", "LMV", "MDW", "NMT", "NPL", "SMT", "SPL", "NWC", "SWC", "SWD" ] 
region = [ "CONUS", "WEST", "SWC", "NWC" ]
region = [ "CONUS", "WEST", "EAST", "NWC" ]
## vday=[ "day2" ]
run_cycle = [ "12Z" ]
region = [ "CONUS", "WEST", "EAST", "SWC", "NWC", "NEC", "SEC" ]
region = [ "CONUS", "WEST", "EAST", "SWC", "NWC", "NEC", "SEC", "MDW", "NMT", "NPL" ]
region = [ "EAST" ]
region = [ "WEST" ]
region = [ "NWC" ]
region = [ "CONUS", "WEST", "EAST", "NWC" ]
region = [ "CONUS" ]
region = [ "CONUS", "WEST", "EAST", "NWC", "NEC", "SWC" ]
xml_data_dir = "/gpfs/dell2/emc/modeling/noscrub/Ho-Chun.Huang/METviewer_AWS/my_plot_xmls_icmaq"
xml_gen_python_name = "plot3.cmaq_pmave_"+stat_var.lower()+".py"
plot_xml_file = "plot_cmaq_pmave_"+stat_var.lower()+".xml"
scripts_dir = "/gpfs/dell2/emc/modeling/noscrub/"+os.environ['USER']+"/METviewer_AWS/script"

checkfile=os.path.join(xml_data_dir,xml_gen_python_name)
if not os.path.exists(checkfile):
    print("Can not find "+checkfile)
    sys.exit()

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
if 1 == 1:
    for area in region:
        for verf_day in vday:
            for verf_cycle in run_cycle:
                subprocess.call(["python", xml_gen_python_name, area, area, verf_day.lower(), fig_sdate, fig_edate, verf_cycle, event_equal_flag])
                if os.path.isfile(plot_xml_file):
                    subprocess.call([os.path.join(".", batch_script_name), os.environ['USER'].lower(), figure_dir, plot_xml_file])
                else:
                    print("Can not find"+os.path.join(tmp_data_dir,plot_xml_file))
if 1 == 1:
    os.chdir(figure_dir)
    subprocess.call("chmod 644 *", shell=True)
    parta=os.path.join("/usr", "bin", "scp")
    if 1 == 2:
       partb=os.path.join("hchuang@rzdm:", "home", "www", "emc", "htdocs", "mmb", "hchuang", "web", "fig", database_year, database_date)
    else:
       ## partb=os.path.join("hchuang@rzdm:", "home", "www", "emc", "htdocs", "mmb", "hchuang", "transfer")
       partb=os.path.join("hchuang@rzdm:", "home", "www", "emc", "htdocs", "mmb", "hchuang", "ftp")

    subprocess.call(['scp -p * '+partb], shell=True)
