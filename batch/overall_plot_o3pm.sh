#!/bin/bash
declare -a cyc=( all )
declare -a fday=( all )
declare -a fday=( day2 )
declare -a fday=( all )
declare -a fday=( day1 day3 )
declare -a cyc=( 06 )
declare -a fday=( day3 )
select_day=day2
declare -a cyc=( 12 )

declare -a cyc=( 06  12 )
declare -a fday=( day1 day2 day3 )

beg_date=20230601
end_date=20230630
figname_date=202306

##
## note time series is now fixed y-axis, need to adjust pm25 ymax for the fire months >=65
declare -a o3pm_var=( o3 pm25 )
for i in "${o3pm_var[@]}"; do
    for j in "${cyc[@]}"; do
        for k in "${fday[@]}"; do
            python aws_batch_plot_aqm_${i}_raw.py ${i} ${j} ${k} ${beg_date} ${end_date} ${figname_date}
            python aws_batch_plot_aqm_${i}_bc.py ${i} ${j} ${k} ${beg_date} ${end_date} ${figname_date}
            python aws_batch_plot_aqm_${i}.py ${i} ${j} ${k} ${beg_date} ${end_date} ${figname_date}
            python aws_batch_plot_aqm_${i}.py taylor ${j} ${k} ${beg_date} ${end_date} ${figname_date}
        done
        python aws_batch_plot_aqm_${i}.py medl ${j} day3 ${beg_date} ${end_date} ${figname_date}
        python aws_batch_plot_aqm_${i}.py rmsedl ${j} day3 ${beg_date} ${end_date} ${figname_date}
    done
done
declare -a o3pm_var=( ozmax8 pmave )
for i in "${o3pm_var[@]}"; do
    for j in "${cyc[@]}"; do
        for k in "${fday[@]}"; do
            python aws_batch_plot_aqm_${i}_raw.py ${i} ${j} ${k} ${beg_date} ${end_date} ${figname_date}
            python aws_batch_plot_aqm_${i}_bc.py ${i} ${j} ${k} ${beg_date} ${end_date} ${figname_date}
            python aws_batch_plot_aqm_${i}.py ${i} ${j} ${k} ${beg_date} ${end_date} ${figname_date}
            python aws_batch_plot_aqm_${i}.py csi ${j} ${k} ${beg_date} ${end_date} ${figname_date}
            python aws_batch_plot_aqm_${i}.py taylor ${j} ${k} ${beg_date} ${end_date} ${figname_date}
            python aws_batch_plot_aqm_${i}.py performance ${j} ${k} ${beg_date} ${end_date} ${figname_date}
        done
    done
done
exit
