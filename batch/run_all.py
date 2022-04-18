import sys
import datetime
import shutil
import os 
import subprocess

### PASSED AGRUEMENTS
if len(sys.argv) < 3:
    print("you must set 3 arguments as var[all|o3|pm25] start_date end_date")
    sys.exit()
else:
    plot_var = sys.argv[1]
    start_date = sys.argv[2]
    end_date = sys.argv[3]

if plot_var == "all":
    var = [ "o3", "pm25" ]
elif plot_var == "o3":
    var = [ "o3" ]
elif plot_var == "pm25":
    var = [ "pm25" ]
else:
    print("selected variable is not defined for this graphic program")
    sys.exit()
    
###METviewer_AWS_scripts_dir = "/gpfs/dell2/emc/verification/noscrub/emc.metplus/METviewer_AWS"
METviewer_AWS_scripts_dir = "/gpfs/dell2/emc/modeling/noscrub/"+os.environ['USER']+"/METviewer_AWS"
stat=[ "csi", "medl", "mets", "rmsedl", "rmsets", "performance", "taylor" ]

for i in var:
    script_name = "aws_batch_plot_hc_cmaq_"+i.lower()+".py"
    print("python "+script_name+" "+i+" all "+start_date+" "+end_date)
    subprocess.call(["python", script_name, i, "all", start_date, end_date])
    for j in stat:
         print("python "+script_name+" "+j+" all "+start_date+" "+end_date)
         subprocess.call(["python", script_name, j, "all", start_date, end_date])

