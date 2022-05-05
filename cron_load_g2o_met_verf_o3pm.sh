#!/bin/sh
#
# This script is intended for the near-real-time daily addition tot he database by month
#
module load prod_util/1.1.6
flag_realtime=no
MSG="$0 envir [prod|...] start_date end_date"
if [ $# -lt 1 ]; then
    echo ${MSG}
    exit
else
    envir=$1
fi
EXP=`echo ${envir} | tr a-z A-Z`
echo "Processing experiment ${envir} verification database addition"

if [ $# -lt 2 ]; then
    TODAY=`date +%Y%m%d`
    FIRSTDAY=${TODAY}
    LASTDAY=${TODAY}
    echo "echo near-realtime addition to the database"
else
    FIRSTDAY=$2
    LASTDAY=$2
    echo "echo selected date ${FIRSTDAY} addition to the database"
fi
if [ $# -eq 3 ]; then LASTDAY=$3; fi

DY0=`echo ${FIRSTDAY} | cut -c7-8`
if [ "${DY0}" == "01" ]; then
    NEW_ADD="true"
else   
    NEW_ADD="false"
fi

##
SCRIPT=/gpfs/dell2/emc/modeling/noscrub/Ho-Chun.Huang/METviewer_AWS/script
XML=/gpfs/dell2/emc/modeling/noscrub/Ho-Chun.Huang/METviewer_AWS/XML
BASE_DIR=/gpfs/dell2/stmp/Ho-Chun.Huang/load_to_aws
LOAD_DIR=${BASE_DIR}/verif
if [ -d ${LOAD_DIR} ]; then /bin/rm -rf ${LOAD_DIR}; fi
mkdir -p ${LOAD_DIR}
##
YM0=`echo ${FIRSTDAY} | cut -c1-6`
verif_type=g2o_met_verf_o3pm
met_datbase=mv_${verif_type}_${envir}_${YM0}
load_datbase_template=load_${verif_type}.base
load_datbase_xml=load_${verif_type}.xml
if [ "${NEW_ADD}" == "true" ]; then  
    $SCRIPT/mv_create_db_on_aws.sh ho-chun.huang ${met_datbase}
    echo "Create new database done!"
fi 
cd ${LOAD_DIR}
NOW=${FIRSTDAY}
while [ ${NOW} -le ${LASTDAY} ]; do
    YM=`echo ${NOW} | cut -c1-6`
    if [ "${YM}" != "${YM0}" ]; then break; fi
    DATA_DIR=/gpfs/dell2/emc/verification/noscrub/Ho-Chun.Huang/metplus_aq/stat/aqm/${NOW}
    cp ${DATA_DIR}/${EXP}* .
    cdate=${NOW}"00"
    NOW=$(${NDATE} +24 ${cdate}| cut -c1-8)
done
    
sed -e "s!xxdatabasexx!${met_datbase}!" -e "s!xxnewaddxx!${NEW_ADD}!" ${XML}/${load_datbase_template} > ${XML}/${load_datbase_xml}
$SCRIPT/mv_load_to_aws.sh ho-chun.huang ${BASE_DIR} ${XML}/${load_datbase_xml}
echo "run_scrpt = ${XML}/${load_datbase_xml}"
exit
