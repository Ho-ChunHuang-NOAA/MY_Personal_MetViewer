#!/bin/sh
module load prod_util/1.1.4
RUN=cmaqaod
declare -a exp=( prod para8 )
declare -a qc=( high medium low )
MSG="$0 new/add BEG_DATE END_DATE"
if [ $# -lt 3 ]; then
   echo ${MSG}
   exit
fi
flag_new=$1
FIRSTDAY=$2
LASTDAY=$3
if [ 1 -eq 2 ]; then
TIME_ID1=`echo ${FIRSTDAY} | cut -c1-6`
TIME_ID2=`echo ${LASTDAY} | cut -c1-6`
if [ "${TIME_ID1}" != "${TIME_ID2}" ]; then
   echo "First day ${TIME_ID1} and last day ${TIME_ID2} are not belong to the same month"
   exit
fi
fi
verif_type=cmaqv5${exp[1]}
met_datbase=mv_${verif_type}_aod_grid2grid_metplus
load_datbase_template=load_grid2grid_met_verf_cmaqaod.base
load_datbase_xml=load_${verif_type}.xml
if [ "${flag_new}" == "new" ]; then  
   NEW_ADD="false"
elif [ "${flag_new}" == "add" ]; then
   NEW_ADD="true"
else
   echo "input ${flag_new} not recognized"
   echo ${MSG}
   exit
fi

SCRIPT=/gpfs/dell2/emc/modeling/noscrub/Ho-Chun.Huang/METviewer_AWS/script
XML=/gpfs/dell2/emc/modeling/noscrub/Ho-Chun.Huang/METviewer_AWS/XML
DATA_DIR=/gpfs/dell2/emc/modeling/noscrub/Ho-Chun.Huang/com/verif
BASE_DIR=/gpfs/dell2/stmp/Ho-Chun.Huang/load_to_aws
LOAD_DIR=${BASE_DIR}/verif
##
## verif need to be consistent for "type" defined in XML/load_g2g_met_verf_${RUN}.xml
##
if [ -d ${LOAD_DIR} ]; then
   /bin/rm -rf ${LOAD_DIR}
fi
mkdir -p ${LOAD_DIR}
cd ${LOAD_DIR}

NOW=${FIRSTDAY}
while [ ${NOW} -le ${LASTDAY} ]; do
   for i in "${exp[@]}"; do
      for j in "${qc[@]}"; do
         tarfile=${DATA_DIR}/${i}/${RUN}.${NOW}/${RUN}_${i}_${j}_${NOW}.stat.tar
         if [ -e ${tarfile} ]; then tar -xf ${tarfile}; fi
      done
   done 
   cdate=${NOW}"00"
   NOW=$(${NDATE} +24 ${cdate}| cut -c1-8)
done

## $SCRIPT/mv_create_db_on_aws.sh ho-chun.huang mv_grid2grid_met_verf_${RUN}
sed -e "s!xxdatabasexx!${met_datbase}!" -e "s!xxnewaddxx!${NEW_ADD}!" ${XML}/${load_datbase_template} > ${XML}/${load_datbase_xml}
if [ "${flag_new}" == "new" ]; then  
   $SCRIPT/mv_create_db_on_aws.sh ho-chun.huang ${met_datbase}
   echo "Create database done!"
fi

$SCRIPT/mv_load_to_aws.sh ho-chun.huang ${BASE_DIR} ${XML}/${load_datbase_xml}

