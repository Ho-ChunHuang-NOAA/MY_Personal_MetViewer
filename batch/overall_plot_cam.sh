#!/bin/bash
declare -a cam_var=( dpt gust hpbl rh tcdc tmp )
declare -a cam_var=( gust rh tcdc tmp )
select_day=day2
beg_date=20220601 
end_date=20220630
for i in "${cam_var[@]}"; do
    python aws_batch_plot_cam_${i}.py ${i} ${select_day} ${beg_date} ${end_date}
    python aws_batch_plot_cam_${i}.py medl ${select_day} ${beg_date} ${end_date}
    python aws_batch_plot_cam_${i}.py rmsedl ${select_day} ${beg_date} ${end_date}
    python aws_batch_plot_cam_${i}.py taylor ${select_day} ${beg_date} ${end_date}
done
python aws_batch_plot_cam_vwind.py bias ${select_day} ${beg_date} ${end_date}
python aws_batch_plot_cam_vwind.py vcnt_rmsve ${select_day} ${beg_date} ${end_date}
