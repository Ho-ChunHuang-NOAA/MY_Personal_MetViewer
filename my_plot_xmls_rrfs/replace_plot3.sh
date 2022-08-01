#!/bin/sh
#
ls plot3* > tlist
count=0
while read line
do
  shfile[$count]=$(echo $line | awk '{print $1}')
  ((count++))
done<tlist

old_ver='mv_g2o_met_cam_aug19v150a,mv_g2o_met_cam_aug19v161a'
new_ver='mv_g2o_met_cam_v70a1_202206,mv_g2o_met_cam_v70b1_202206'
old_ver='"V150A", "V161A"'
new_ver='"V70A1", "V70B1"'
old_ver='"NAM-CMAQ", "v150-a", "v161-a"'
new_ver='"GFS-CMAQ", "v70-a1", "v70-b1"'
old_ver='"v161a'
new_ver='"v70b1'
old_ver='"v150a'
new_ver='"v70a1'
old_ver='"NAM-CMAQ'
old_ver='"GFS-CMAQ'
old_ver='"PROD", "v70-a1"'
new_ver='"GFS-CMAQ", "v70-a1"'
old_ver='\\\"#006400FF\\\",\\\"#0000ffFF\\\"'
new_ver='\\\"#0000ffFF\\\",\\\"#006400FF\\\"'
old_ver='mv_g2o_met_icmaq_aug19,mv_g2o_met_icmaq_aug19v161a,mv_g2o_met_icmaq_aug19v150a'
new_ver='mv_g2o_met_o3pm_prod_202206,mv_g2o_met_o3pm_v70a1_202206,mv_g2o_met_o3pm_v70b1_202206'
old_ver='mv_g2o_met_icmaq_aug19,mv_g2o_met_icmaq_aug19v150a,mv_g2o_met_icmaq_aug19v161a'
new_ver='mv_g2o_met_o3pm_prod_202206,mv_g2o_met_o3pm_v70a1_202206,mv_g2o_met_o3pm_v70b1_202206'
old_ver='mv_g2o_met_o3pm_prod_202206,mv_g2o_met_o3pm_v70a1_202206,mv_g2o_met_o3pm_v70b1_202206'
new_ver='mv_g2o_met_o3pm_prod_202207,mv_g2o_met_o3pm_v70a1_202207,mv_g2o_met_o3pm_v70b1_202207'
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
