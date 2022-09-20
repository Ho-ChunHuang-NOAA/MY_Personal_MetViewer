#!/bin/sh
from_code=plot2.cmaq
to_code=plot4.cmaq
declare -a met_var=( dpt gust hpbl rh tcdc tmp )
declare -a statistics=( time_series medl rmsedl taylor )
declare -a aqm_var=( o3 pm25 ozmax1 ozmax8 pdmax1 pmave )
declare -a statistics=( csi medl mets performance rmsedl rmsets taylor time_series )
Time_series

for i in "${aqm_var[@]}"; do
    for j in "${statistics[@]}"; do
        if [ -s ${from_code}_${i}_${j}.py ]; then
            cp ${from_code}_${i}_${j}.py ${to_code}_${i}_${j}.py
        else
            echo "Can not find ${from_code}_${i}_${j}.py"
        fi
    done
done

## cp ${from_code}_vwind_bias.py ${to_code}_vwind_bias.py
## cp ${from_code}_vwind_vcnt_rmsve.py ${to_code}_vwind_vcnt_rmsve.py


