#!/bin/sh
#
# This script is intended for the restrospective daily addition tot he database by month
# For the near-real-time daily addition tot he database by month, use
#    cron_load_g2o_met_verf_o3pm.sh
#
module load prod_util/1.1.6
## set -x
flag_realtime=no
MSG="$0 [new/add] envir [prod|...] start_date end_date"
if [ $# -lt 1 ]; then
    echo ${MSG}
    exit
elif [ $# -lt 2 ]; then
    flag_new=$1
    envir=prod
    TODAY=`date +%Y%m%d`
    FIRSTDAY=${TODAY}
    LASTDAY=${TODAY}
    echo "echo near-realtime ${envir} addition to the database"
    flag_realtime=yes
elif [ $# -lt 3 ]; then
    flag_new=$1
    envir=$2
    TODAY=`date +%Y%m%d`
    FIRSTDAY=${TODAY}
    LASTDAY=${TODAY}
    echo "echo near-realtime ${envir} addition to the database"
    flag_realtime=yes
elif [ $# -lt 4 ]; then
    flag_new=$1
    envir=$2
    FIRSTDAY=$3
    LASTDAY=$3
    echo "echo selected date ${FIRSTDAY} ${envir} addition to the database"
else
    flag_new=$1
    envir=$2
    FIRSTDAY=$3
    LASTDAY=$4
    echo "echo selected date ${FIRSTDAY} to ${LASTDAY} ${envir} addition to the database"
fi
EXP=`echo ${envir} | tr a-z A-Z`
echo "Processing experiment ${envir} verification database addition"

flag_same_month=yes
TIME_ID1=`echo ${FIRSTDAY} | cut -c1-6`
TIME_ID2=`echo ${LASTDAY} | cut -c1-6`
if [ "${TIME_ID1}" != "${TIME_ID2}" ]; then
    echo "WARNING =================================================================================="
    echo "WARNING :; First day ${FIRSTDAY} and last day ${LASTDAY} are not belong to the same month"
    echo "WARNING :; New database need to be generated on the first day of each month"
    echo "WARNING :; The Last Day will be rolled back to the last day of ${TIME_ID1}" for 1st load
    echo "WARNING =================================================================================="
    flag_same_month=no
    LASTDAY2=${LASTDAY}
    ID3=`echo ${LASTDAY} | cut -c1-6`
    FIRSTDAY2=${ID3}"01"
    while [ ${ID3} -gt ${TIME_ID1} ]; do
        cdate=${LASTDAY}"00"
        LASTDAY=$( ${NDATE} -24 ${cdate} | cut -c1-8 )
        ID3=`echo ${LASTDAY} | cut -c1-6`
        echo " ${LASTDAY} ${ID3} "
    done
fi
echo " Process load_aws_database for ${envir} from ${FIRSTDAY} to ${LASTDAY}"

SCRIPT=/gpfs/dell2/emc/modeling/noscrub/Ho-Chun.Huang/METviewer_AWS/script
XML=/gpfs/dell2/emc/modeling/noscrub/Ho-Chun.Huang/METviewer_AWS/XML
BASE_DIR=/gpfs/dell2/stmp/Ho-Chun.Huang/load_to_aws
LOAD_DIR=${BASE_DIR}/verif
verif_type=g2o_met_verf_o3pm

DY0=`echo ${FIRSTDAY} | cut -c7-8`
if [ "${flag_realtime}" == "yes" ]; then
    if [ "${DY0}" == "01" ]; then
        NEW_ADD="true"
    else   
        NEW_ADD="false"
    fi
else
    if [ "${flag_new}" == "new" ]; then
        NEW_ADD="true"
    elif [ "${flag_new}" == "add" ]; then
        NEW_ADD="false"
    else
        echo "input ${flag_new} not recognized"
        echo ${MSG}
        exit
    fi
fi
##
if [ -d ${LOAD_DIR} ]; then /bin/rm -rf ${LOAD_DIR}; fi
mkdir -p ${LOAD_DIR}
##
YM0=`echo ${FIRSTDAY} | cut -c1-6`
met_datbase=mv_${verif_type}_${envir}_${YM0}
load_datbase_template=load_${verif_type}.base
load_datbase_xml=load_${verif_type}.xml
if [ "${NEW_ADD}" == "true" ]; then  
    $SCRIPT/mv_create_db_on_aws.sh ho-chun.huang ${met_datbase}
    echo "Create new database ${met_datbase}"
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
if [ "${flag_same_month}" == "no" ]; then
    echo " Process 2nd load_aws_database for ${envir} from ${FIRSTDAY2} to ${LASTDAY2}"
    FIRSTDAY=${FIRSTDAY2}
    LASTDAY=${LASTDAY2}
    ##
    if [ -d ${LOAD_DIR} ]; then /bin/rm -rf ${LOAD_DIR}; fi
    mkdir -p ${LOAD_DIR}
    ##
    YM0=`echo ${FIRSTDAY} | cut -c1-6`
    met_datbase=mv_${verif_type}_${envir}_${YM0}
    load_datbase_template=load_${verif_type}.base
    load_datbase_xml=load_${verif_type}.xml
    if [ "${NEW_ADD}" == "true" ]; then  
        $SCRIPT/mv_create_db_on_aws.sh ho-chun.huang ${met_datbase}
        echo "Create new database ${met_datbase}"
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
fi
exit
