#!/bin/sh
module load prod_util/1.1.4
RUN=cmaqo3pm
declare -a exp=( prod para6a )
declare -a verf_var=( oz ozbc pm pmbc )
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
verif_type=cmaqv5v6a
met_datbase=mv_${verif_type}_o3pm_grid2obs_metplus
load_datbase_template=load_grid2obs_met_verf_${RUN}.base
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

SCRIPT=/lfs/h2/emc/physics/noscrub/${USER}/METviewer_AWS/script
XML=/lfs/h2/emc/physics/noscrub/${USER}/METviewer_AWS/XML
DATA_DIR=/lfs/h2/emc/physics/noscrub/${USER}/com/verif
BASE_DIR=/lfs/h2/emc/stmp/${USER}/load_to_aws
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
      idir=${DATA_DIR}/${i}/aqmstat.${NOW}
      if [ -d ${idir} ]; then
         ## for j in "${verf_var[@]}"; do
         ##    capmdl=`echo ${i} | tr '[:lower:]' '[:upper:]'`
         ##    capvar=`echo ${j} | tr '[:lower:]' '[:upper:]'`
         ##    cp -p ${idir}/${capvar}${capmdl}* .
         ## done 
         cp -p ${idir}/* .
      fi
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

