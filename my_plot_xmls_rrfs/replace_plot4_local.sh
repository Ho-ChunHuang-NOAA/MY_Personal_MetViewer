#!/bin/sh
#
## ls *csi.py> tlist
ls plot2.cmaq_o* > tlist
ls plot2.cmaq_p* >> tlist
ls plot4* > tlist
count=0
while read line
do
  shfile[$count]=$(echo $line | awk '{print $1}')
  ((count++))
done<tlist

old_ver='mv_g2o_met_o3pm_v70b1'
new_ver='mv_g2o_met_o3pm_v70c3'
old_ver='mv_g2o_met_o3pm_v70c43'
new_ver='mv_g2o_met_o3pm_b_v70c43'
old_ver='V70C3_BC'
new_ver='V70C43_BC'
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
