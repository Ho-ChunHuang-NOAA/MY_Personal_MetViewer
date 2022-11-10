#!/bin/bash
declare -a aod_var=( aod )
declare -a sat_var=( goes viirs )
select_day=day2
beg_date=20220822 
end_date=20220831
for i in "${aod_var[@]}"; do
    for j in "${sat_var[@]}"; do
        python aws_batch_plot_${j}_${i}.py ${i} ${select_day} ${beg_date} ${end_date}
        python aws_batch_plot_${j}_${i}.py csi ${select_day} ${beg_date} ${end_date}
    done
done
select_day=day3
for i in "${aod_var[@]}"; do
    for j in "${sat_var[@]}"; do
        python aws_batch_plot_${j}_${i}.py medl ${select_day} ${beg_date} ${end_date}
        python aws_batch_plot_${j}_${i}.py rmsedl ${select_day} ${beg_date} ${end_date}
    done
done
