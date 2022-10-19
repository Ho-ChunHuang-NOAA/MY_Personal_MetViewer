#!/bin/sh
#
## ls *csi.py> tlist
## ls plot2* > tlist
ls plot2.cmaq_b_* > tlist
count=0
while read line
do
  shfile[$count]=$(echo $line | awk '{print $1}')
  ((count++))
done<tlist

old_ver="\"+Ho-Chun.Huang+\"\/"
old_ver='mv_g2o_met_icmaq_aug19,mv_g2o_met_icmaq_aug19v161a,mv_g2o_met_icmaq_aug19v150a'
new_ver='mv_g2o_met_o3pm_prod_202206,mv_g2o_met_o3pm_v70a1_202206,mv_g2o_met_o3pm_v70b1_202206'
old_ver='/gpfs/hps3/emc/global/noscrub'
new_ver='/lfs/h2/emc/vpppg/noscrub'
old_ver='/gpfs/dell2/stmp'
new_ver='/lfs/h2/emc/stmp'
old_ver="\/Ho-Chun.Huang\/"
new_ver="\/\"+os.environ\[\'USER\'\]+\"\/"
old_ver='/gpfs/dell2/emc/modeling/noscrub'
new_ver='/lfs/h2/emc/physics/noscrub'
old_ver='<indy1_stag>true'
new_ver='<indy1_stag>false'
old_ver='mv_g2o_met_cam_v70a1_202206,mv_g2o_met_cam_v70b1_202206'
new_ver='mv_g2o_met_cam_v70a1_"+database_date+",mv_g2o_met_cam_v70b1_"+database_date+"'
old_ver='mv_g2o_met_cam_aug19v150a,mv_g2o_met_cam_aug19v161a'
new_ver='mv_g2o_met_cam_v70a1_202206,mv_g2o_met_cam_v70b1_202206'
old_ver="\\"#006400FF\\",\\"#ff0000FF\\""
new_ver="\\"#ff0000FF\\""
old_ver="mv_g2o_met_o3pm_b_prod"
new_ver="mv_g2o_met_o3pm_prod"
old_ver="mv_g2o_met_o3pm_b_v70b1"
new_ver="mv_g2o_met_o3pm_v70b1"
old_ver='mv_g2o_met_o3pm_prod_"+database_date+",mv_g2o_met_o3pm_v70b1_"+database_date+"'
new_ver='mv_g2o_met_o3pm_b_prod_"+database_date+",mv_g2o_met_o3pm_b_v70b1_"+database_date+"'
old_ver='mv_g2o_met_o3pm_b_prod_"+database_date+",mv_g2o_met_o3pm_b_v70b1_"+database_date+"'
new_ver='mv_g2o_met_o3pm_prod_"+database_date+",mv_g2o_met_o3pm_v70b1_"+database_date+"'
old_ver='mv_g2o_met_o3pm_b_v70b1'
new_ver='mv_g2o_met_o3pm_b_v70c3'
old_ver='v70-b1'
new_ver='v70-c3'
for i in "${shfile[@]}"
do
   echo ${i}
   if [ "${i}" == $0 ]; then continue; fi
   if [ "${i}" == "xtest1" ]; then continue; fi
   if [ -d ${i} ]; then continue; fi
   ## mv ${i}.bak ${i}
   if [ -e xtest1 ]; then /bin/rm -f xtest1; fi
   grep "${old_ver}" ${i} > xtest1
   if [ -s xtest1 ]; then
      mv ${i} ${i}.bak
      sed -e "s!${old_ver}!${new_ver}!" ${i}.bak > ${i}
      ## echo "diff ${i} ${i}.bak"
      chmod u+x ${i}
      diff ${i} ${i}.bak
   fi
done
exit
