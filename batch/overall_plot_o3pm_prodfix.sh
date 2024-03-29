#!/bin/bash
declare -a o3pm_var=( o3 pm25 )
select_day=day2
beg_date=20220601 
end_date=20220831
for i in "${o3pm_var[@]}"; do
    python aws_batch_plot_prodfix_${i}.py medl ${select_day} ${beg_date} ${end_date}
    python aws_batch_plot_prodfix_${i}.py rmsedl ${select_day} ${beg_date} ${end_date}
done
declare -a o3pm_var=( ozmax8 pmave )
for i in "${o3pm_var[@]}"; do
    python aws_batch_plot_prodfix_${i}.py ${i} ${select_day} ${beg_date} ${end_date} 
    python aws_batch_plot_prodfix_${i}.py csi ${select_day} ${beg_date} ${end_date}
done
declare -a o3pm_var=( pm25 )
select_day=day2
beg_date=20220601 
end_date=20220301
for i in "${o3pm_var[@]}"; do
    python aws_batch_plot_prodfix_${i}.py ${i} ${select_day} ${beg_date} ${end_date} 
done
declare -a o3pm_var=( pm25 )
select_day=day2
beg_date=20220901 
end_date=20220930
for i in "${o3pm_var[@]}"; do
    python aws_batch_plot_prodfix_${i}.py ${i} ${select_day} ${beg_date} ${end_date} 
done
