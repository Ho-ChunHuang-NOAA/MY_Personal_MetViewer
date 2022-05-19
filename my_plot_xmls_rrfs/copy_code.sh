#!/bin/sh
from_code=plot2.cmaq
to_code=plot.cmaq
declare -a met_var=( dpt gust hpbl rh tcdc tmp )
declare -a statistics=( time_series medl rmsedl taylor )

for i in "${met_var[@]}"; do
    for j in "${statistics[@]}"; do
        if [ -s ${from_code}_${i}_${j}.py ]; then
            cp ${from_code}_${i}_${j}.py ${to_code}_${i}_${j}.py
        else
            echo "Can not find ${from_code}_${i}_${j}.py"
        fi
    done
done

cp ${from_code}_vwind_bias.py ${to_code}_vwind_bias.py
cp ${from_code}_vwind_vcnt_rmsve.py ${to_code}_vwind_vcnt_rmsve.py


