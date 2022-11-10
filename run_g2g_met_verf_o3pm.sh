#!/bin/bash
module load prod_util/1.1.4
declare -a exp=( prod para12 para87h)
FIRSTDAY=20190801
LASTDAY=20190831
FIRSTDAY=$2
LASTDAY=$3
TIME_ID1=`echo ${FIRSTDAY} | cut -c1-6`
TIME_ID2=`echo ${LASTDAY} | cut -c1-6`
if [ "${TIME_ID1}" != "${TIME_ID2}" ]; then
   echo "First day ${TIME_ID1} and last day ${TIME_ID2} are not belong to the same month"
   exit
fi
verif_type=grid2grid_met_verf_aod
met_datbase=mv_${verif_type}_${TIME_ID1}
load_datbase_template=load_${verif_type}.base
load_datbase_xml=load_${verif_type}.xml
MSG="$0 new or add database [new|add]"
if [ $# -lt 1 ]; then
   echo ${MSG}
   exit
fi
flag_new=$1
if [ "${flag_new}" == "new" ]; then  
   NEW_ADD="false"
elif [ "${flag_new}" == "add" ]; then
   NEW_ADD="true"
else
   echo "input ${flag_new} not recognized"
   echo ${MSG}
   exit
fi

hl=`hostname | cut -c1`

SCRIPT=/lfs/h2/emc/physics/noscrub/${USER}/METviewer_AWS/script
XML=/lfs/h2/emc/physics/noscrub/${USER}/METviewer_AWS/XML
## DATA_DIR=/lfs/h2/emc/ptmp/${USER}/verif
DATA_DIR=/lfs/h2/emc/physics/noscrub/${USER}/com/aqm
BASE_DIR=/lfs/h2/emc/stmp/${USER}/load_to_aws
LOAD_DIR=${BASE_DIR}/verif
##
## verif need to be consistent for "type" defined in XML/load_g2g_met_verf_aod.xml
##
mkdir -p ${LOAD_DIR}

cd ${LOAD_DIR}
NOW=${FIRSTDAY}
while [ ${NOW} -le ${LASTDAY} ]; do
   for i in "${exp[@]}"; do
      tarfile=${DATA_DIR}/${i}/verif_cmaqaod.${NOW}/cmaqaod_${i}_CMAQAOD_${NOW}.stat.tar
      if [ -e ${tarfile} ]; then tar -xf ${tarfile}; fi
   done 
   cdate=${NOW}"00"
   NOW=$(${NDATE} +24 ${cdate}| cut -c1-8)
done

## $SCRIPT/mv_create_db_on_aws.sh ho-chun.huang mv_grid2grid_met_verf_aod
sed -e "s!xxdatabasexx!${met_datbase}!" -e "s!xxnewaddxx!${NEW_ADD}!" ${XML}/${load_datbase_template} > ${XML}/${load_datbase_xml}
if [ "${flag_new}" == "new" ]; then  
   $SCRIPT/mv_create_db_on_aws.sh ho-chun.huang ${met_datbase}
   echo "Create database done!"
fi

$SCRIPT/mv_load_to_aws.sh ho-chun.huang ${BASE_DIR} ${XML}/${load_datbase_xml}

