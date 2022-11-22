#!/bin/bash
from_code=aws_batch_plot_icmaq
to_code=aws_batch_plot_c3
declare -a aqm_var=( o3 pm25 ozmax8 pmave )
for i in "${aqm_var[@]}"; do
        if [ -s ${from_code}_${i}.py ]; then
            cp ${from_code}_${i}.py ${to_code}_${i}.py
        else
            echo "Can not find ${from_code}_${i}.py"
        fi
done
