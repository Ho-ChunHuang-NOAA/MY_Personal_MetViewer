#!/bin/sh
module load prod_util/1.1.6
declare -a exp=( pm_prod pm_para6d pm_v150a)
declare -a exp=( aqm_prod aqm_para6d aqm_v150a pm_prod pm_para6d pm_v150a)
declare -a exp=( V160A )
declare -a exp=( PROD PARA6D V150A )
FIRSTDAY=$2
LASTDAY=$3
FIRSTDAY=20200901
LASTDAY=20200930
TIME_ID1=`echo ${FIRSTDAY} | cut -c1-6`
TIME_ID2=`echo ${LASTDAY} | cut -c1-6`
# if [ "${TIME_ID1}" != "${TIME_ID2}" ]; then
#    echo "First day ${TIME_ID1} and last day ${TIME_ID2} are not belong to the same month"
#    exit
# fi
TIME_ID1=sep20
verif_type=g2o_met_icmaq
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

SCRIPT=/gpfs/dell2/emc/modeling/noscrub/Ho-Chun.Huang/METviewer_AWS/script
XML=/gpfs/dell2/emc/modeling/noscrub/Ho-Chun.Huang/METviewer_AWS/XML
## DATA_DIR=/gpfs/${phase12_id}p2/ptmp/Ho-Chun.Huang/verif
## DATA_DIR=/gpfs/${phase12_id}d3/emc/meso/noscrub/Ho-Chun.Huang/com2/aqm
DATA_DIR=/gpfs/dell2/emc/verification/noscrub/Ho-Chun.Huang/metplus_aq/stat/aqm
BASE_DIR=/gpfs/dell2/stmp/Ho-Chun.Huang/load_to_aws
LOAD_DIR=${BASE_DIR}/verif_icmaq
##
## verif need to be consistent for "type" defined in XML/load_g2g_met_verf_aod.xml
##
TMP_DIR=${BASE_DIR}/verif
if [ -d ${TMP_DIR} ]; then /bin/rm -rf ${TMP_DIR}/* ; fi
mkdir -p ${TMP_DIR}

if [ -d ${LOAD_DIR} ]; then /bin/rm -rf ${LOAD_DIR}/* ; fi
mkdir -p ${LOAD_DIR}

cd ${LOAD_DIR}
NOW=${FIRSTDAY}
while [ ${NOW} -le ${LASTDAY} ]; do
   for i in "${exp[@]}"; do
       cp ${DATA_DIR}/${NOW}/${i}_AQ_* .
       cp ${DATA_DIR}/${NOW}/${i}_PM_* .
       if [ "${i}" != "V150A" ]; then
           cp ${DATA_DIR}/${NOW}/${i}_BC_AQ_* .
           cp ${DATA_DIR}/${NOW}/${i}_BC_PM_* .
       fi
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

