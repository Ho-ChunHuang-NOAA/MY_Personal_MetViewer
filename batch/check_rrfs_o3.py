import sys
import datetime
import shutil
import os 
import subprocess

# PASSED N AGRUEMENTS IN : total number of argument including [0] is N+1
if len(sys.argv) < 6:
    print("you must set 6 arguments as stat[o3|rmse|...] [06|12|all] [day1|day2|day3|all] start_date end_date fig_date event_equal[optional]")
    sys.exit()
else:
    stat_var = sys.argv[1]
    flag_cyc  = sys.argv[2]
    flag_vday = sys.argv[3]
    start_date = sys.argv[4]
    end_date = sys.argv[5]
    figname_date = sys.argv[6]
if stat_var == "o3":
    stat_var = "time_series"
print(str(len(sys.argv)))
if len(sys.argv) > 7:
    event_equal_flag = sys.argv[7]
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

ftp_year=figname_date[0:4]
ftp_dir=figname_date

fig_sdate = sdate.strftime(file_date_format)
fig_edate = edate.strftime(file_date_format)

ibeg=int(start_date[0:6])
iend=int(end_date[0:6])
addbase=[ ]
for i in range(ibeg,iend+1):
    idate=str(i)
    icheck=int(idate[4:6])
    if icheck > 0 and icheck <= 12:
        addbase.append(str(i))
    i+=1
## print(addbase)

METviewer_AWS_scripts_dir = "/lfs/h2/emc/vpppg/save/"+os.environ['USER']+"/METviewer_AWS"
print(METviewer_AWS_scripts_dir)
if flag_cyc == "all":
   run_cycle=[ "06Z", "12Z" ]
elif flag_cyc == "06":
   run_cycle=[ "06Z" ]
elif flag_cyc == "12":
   run_cycle=[ "12Z" ]
else:
    print("verification verify day "+cyc+" not recongized.")
    exit()
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
   vday=[ "day3" ]
elif stat_var == "medl":
   vday=[ "day3" ]
region = [ "Appalachia", "CONUS_Central", "CONUS_East", "CONUS", "CONUS_South", "CONUS_West", "CPlains", "DeepSouth", "GreatBasin", "GreatLakes", "Mezquital", "MidAtlantic", "NorthAtlantic", "NPlains", "NRockies", "PacificNW", "PacificSW", "Prairie", "Southeast", "Southwest", "SPlains", "SRockies" ]
region = [ "CONUS_Central", "CONUS_East", "CONUS", "CONUS_South", "CONUS_West" ]
region = [ "NRockies", "SRockies", "GreatBasin", "PacificNW", "PacificSW", "CONUS_Central", "CONUS_East", "CONUS", "CONUS_South", "CONUS_West", "Southwest" ]
region = [ "CONUS" ]
region = [ "MidAtlantic", "NorthAtlantic" ]
region = [ "CONUS_East" ]
xml_data_dir = "/lfs/h2/emc/vpppg/save/"+os.environ['USER']+"/METviewer_AWS/my_plot_xmls_base"
plot_xml_file = "plot_cmaq_o3_"+stat_var.lower()+".xml"
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

database_header="mv_g2o_met_o3pm_b_"
exp_incl=[ "prod", "v70c43", "v70c45" ]
exp_incl=[ "prod", "prod_bc", "v70c55", "v70c55_bc" ]
exp_incl=[ "v70c55", "v70c55_bc", "v70csv", "v70csv_bc" ]
inum=len(exp_incl)
exp_labl=[]
for i in range(0,inum):
    ic=i+1
    exp_labl.append("LBL"+str(ic))
exp_symb=[]
for i in range(0,inum):
    ic=i+1
    exp_symb.append("MDL"+str(ic))
xml_python_basename = "plot"+str(inum)+".cmaq_o3_"+stat_var.lower()+".base"
xml_python_basename = "plot"+str(inum)+".cmaq_o3_"+stat_var.lower()+".70.base"
xml_python_basename = "plot"+str(inum)+".cmaq_o3_"+stat_var.lower()+".75.base"
xml_gen_python_name = "common_plot.cmaq_o3."+stat_var.lower()+".py"

checkfile=os.path.join(xml_data_dir,xml_python_basename)
if not os.path.exists(checkfile):
    print("Can not find "+checkfile)
    sys.exit()

os.chdir(tmp_data_dir)
shutil.copy(os.path.join(scripts_dir, batch_script_name), tmp_data_dir)
shutil.copy(os.path.join(xml_data_dir, xml_python_basename), tmp_data_dir)

iexp=0
print(addbase)
for j in addbase:
    explist=[]
    for i in exp_incl:
        if iexp == 0 :
            nfind=i.find("_bc")
            if nfind == -1:
                EXP=i
            else:
                EXP=i[0:nfind]
            met_database_run=database_header+EXP.lower()+"_"+j
            explist.append(EXP)
        else:
            nfind=i.find("_bc")
            if nfind == -1:
                EXP=i
            else:
                EXP=i[0:nfind]
            add_exp=True
            for old_exp in explist:
                if old_exp == EXP:
                    add_exp=False
            if add_exp:
                 met_database_run=met_database_run+','+database_header+EXP.lower()+"_"+j
                 explist.append(EXP)
        iexp+=1
run_command='sed -e "s!XYZdatabase_nameXYZ!'+met_database_run+'!" '
for i in range(0,inum):
    run_command=run_command+' -e "s!XYZ'+exp_symb[i]+'XYZ!'+exp_incl[i].upper()+'!" '
    if i == 0  or i == 1:
        run_command=run_command+' -e "s!XYZ'+exp_labl[i]+'XYZ!'+exp_incl[i].upper()+'!" '
    else:
        run_command=run_command+' -e "s!XYZ'+exp_labl[i]+'XYZ!'+exp_incl[i].lower()+'!" '
run_cmmmand=run_command+' '+xml_python_basename+' > '+xml_gen_python_name
subprocess.call([run_cmmmand], shell=True)

if 1 == 1:
    for area in region:
        for verf_day in vday:
            for verf_cycle in run_cycle:
                subprocess.call(["python", xml_gen_python_name, area, area, verf_day.lower(), fig_sdate, fig_edate, figname_date, verf_cycle, event_equal_flag])
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
       partb=os.path.join("hchuang@rzdm:", "home", "www", "emc", "htdocs", "mmb", "hchuang", "transfer")
       partb=os.path.join("hchuang@rzdm:", "home", "www", "emc", "htdocs", "mmb", "hchuang", "evs_verif", ftp_year, ftp_dir )
       partb=os.path.join("hchuang@rzdm:", "home", "www", "emc", "htdocs", "mmb", "hchuang", "ftp")

    subprocess.call(['scp -p * '+partb], shell=True)
