#!/bin/sh
module load ips/18.0.5.274
module load prod_util/1.1.6
module load prod_envir/1.1.0

declare -a nspec=( o3 pm25 )
declare -a mettype=( csi mets medl rmsets rmsedl diurnal performance taylor time_series )
from_code=plot2
to_code=plot3
for i in "${nspec[@]}"; do
    for j in "${mettype[@]}"; do
        if [ -s ${from_code}.cmaq_${i}_${j}.py ]; then
             cp ${from_code}.cmaq_${i}_${j}.py ${to_code}.cmaq_${i}_${j}.py
        else
             echo "Can not find ${from_code}.cmaq_${i}_${j}.py"
        fi
    done
done
exit
