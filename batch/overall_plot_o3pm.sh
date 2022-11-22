#!/bin/bash
declare -a cyc=( all )
declare -a fday=( all )
declare -a cyc=( 06  12 )
declare -a fday=( day1 day2 day3 )
declare -a o3pm_var=( o3 pm25 )
declare -a cyc=( 12 )
declare -a fday=( day2 )
declare -a fday=( all )
declare -a fday=( day1 day3 )
declare -a cyc=( 06 )
declare -a fday=( day3 )
select_day=day2
beg_date=20221101 
end_date=20221113
for i in "${o3pm_var[@]}"; do
    for j in "${cyc[@]}"; do
        for k in "${fday[@]}"; do
            python aws_batch_plot_icmaq_${i}.py ${i} ${j} ${k} ${beg_date} ${end_date} false
            python aws_batch_plot_icmaq_${i}.py medl ${j} ${k} ${beg_date} ${end_date}
            python aws_batch_plot_icmaq_${i}.py rmsedl ${j} ${k} ${beg_date} ${end_date}
            python aws_batch_plot_icmaq_${i}.py taylor ${j} ${k} ${beg_date} ${end_date}
        done
    done
done
declare -a o3pm_var=( ozmax8 pmave )
for i in "${o3pm_var[@]}"; do
    for j in "${cyc[@]}"; do
        for k in "${fday[@]}"; do
            python aws_batch_plot_icmaq_${i}.py ${i} ${j} ${k} ${beg_date} ${end_date} false
            python aws_batch_plot_icmaq_${i}.py csi ${j} ${k} ${beg_date} ${end_date}
            python aws_batch_plot_icmaq_${i}.py taylor ${j} ${k} ${beg_date} ${end_date}
            python aws_batch_plot_icmaq_${i}.py performance ${j} ${k} ${beg_date} ${end_date}
        done
    done
done
