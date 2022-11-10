#!/bin/bash
from_code=aws_batch_plot_prod
to_code=aws_batch_plot_prodfix
declare -a aqm_var=( o3 pm25 ozmax1 ozmax8 pdmax1 pmave )
for i in "${aqm_var[@]}"; do
        if [ -s ${from_code}_${i}.py ]; then
            cp ${from_code}_${i}.py ${to_code}_${i}.py
        else
            echo "Can not find ${from_code}_${i}.py"
        fi
done
