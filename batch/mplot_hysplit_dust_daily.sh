#!/bin/sh
module load prod_util/1.1.4
module load python/2.7.14
MSG="$0 Start_Mon [yyyymm] End_Mon [yyyymm] "
if [ $# -lt 2 ]; then
   echo ${MSG}
   exit
else
   FIRSTMON=$1
   LASTMON=$2
fi
if [ ${FIRSTMON} -gt 999999 ] || [ ${LASTMON} -gt 999999 ]; then
   echo ${MSG}
   exit
fi
declare -a dayofmon=( 31 28 31 30 31 30 31 31 30 31 30 31 )
logdir=/lfs/h2/emc/ptmp/"+os.environ['USER']+"/batch.logs
NOW=${FIRSTMON}
script_dir=/lfs/h2/emc/vpppg/save/"+os.environ['USER']+"/METviewer_AWS/batch
script_name=aws_batch_plot_hysplit_dust.py
cd ${script_dir}
script_name=aws_batch_plot_hysplit_dust_daily.py
while [ ${NOW} -le ${LASTMON} ]; do
   YY=`echo ${NOW} | cut -c1-4`
   Mx=`echo ${NOW} | cut -c5-5`
   if [ "${Mx}" == "0" ]; then
      MM=`echo ${NOW} | cut -c6-6`
   else
      MM=`echo ${NOW} | cut -c5-6`
   fi
   if [ ${MM} -eq 2 ]; then
      let x=$((${YY}%400))
      if [ ${x} -eq 0 ]; then
        let leap=1
      else
        let y=$((${YY}%100))
        if [ ${y} -ne 0 ]; then
          let z=$((${YY}%4))
          if [ ${z} -eq 0 ]; then
            let leap=1
          fi
        fi
      fi
      if [ "${leap}" == "1" ]; then dayofmon[1]=29; fi
   fi
   let M1=${MM}-1
   echo "python ${script_name} csi all ${NOW}01 ${NOW}${dayofmon[${M1}]}"
   python ${script_name} csi all ${NOW}01 ${NOW}${dayofmon[${M1}]} > ${logdir}/${script_name}_${NOW}01_${NOW}${dayofmon[${M1}]}.log 2>&1
   if [ "${MM}" == "12" ]; then
      let yynew=${YY}+1
      NOW=${yynew}"01"
   else
      ((NOW++))
   fi
   echo "day_of_mon is ${dayofmon[${M1}]}, next NOW is ${NOW}"
done
exit

