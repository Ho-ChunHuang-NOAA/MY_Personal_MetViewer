#!/bin/bash
#
# This script is intended for the restrospective daily addition tot he database by month
# For the near-real-time daily addition tot he database by month, use
#    cron_load_g2o_met_verf_o3pm.sh
#
module load prod_util
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

## set -x

## EXP=`echo ${envir} | tr a-z A-Z`
capexp=`echo ${envir} | tr '[:lower:]' '[:upper:]'`
echo "Processing experiment ${envir} verification database addition"

flag_same_month=yes
TIME_ID1=`echo ${FIRSTDAY} | cut -c1-6`
TIME_ID2=`echo ${LASTDAY} | cut -c1-6`
if [ "${TIME_ID1}" != "${TIME_ID2}" ]; then
    echo "WARNING =================================================================================="
    echo "WARNING :; First day = ${FIRSTDAY} and last day = ${LASTDAY} is a cross-month upload"
    echo "WARNING :; will split into two upload for each months"
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
    echo "WARNING :; The 1st upload will be from ${FIRSTDAY} to ${LASTDAY}"
    echo "WARNING :; The 2nd upload will be from ${FIRSTDAY2} to ${LASTDAY2}"
    echo "WARNING =================================================================================="
else
    echo " Process load_aws_database for ${envir} from ${FIRSTDAY} to ${LASTDAY}"
fi

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

database=meteor
database=chem
if [ "${database}" == "chem" ]; then
    verif_var="o3pm"
    DATA_DIR=/lfs/h2/emc/physics/noscrub/${USER}/metplus_aq/stat/aqm
elif [ "${database}" == "meteor" ]; then
    verif_var="cam"
    DATA_DIR=/lfs/h2/emc/physics/noscrub/${USER}/metplus_cam/stat/cam
fi

SCRIPT=/lfs/h2/emc/physics/noscrub/${USER}/METviewer_AWS/script
XML=/lfs/h2/emc/physics/noscrub/${USER}/METviewer_AWS/XML

verif_type=g2o_met
load_datbase_template=load_${verif_type}.base
if [ ! -s ${XML}/${load_datbase_template} ]; then
    echo "Can not find ${XML}/${load_datbase_template}"
    exit
fi

BASE_DIR=/lfs/h2/emc/stmp/${USER}/load_to_aws_${verif_var}_${envir}
mkdir -p ${BASE_DIR}

TMP_DIR=${BASE_DIR}/tmp
if [ -d ${TMP_DIR} ]; then /bin/rm -rf ${TMP_DIR}/* ; fi
mkdir -p ${TMP_DIR}

sub_dir=verif_${verif_var}_${envir}
LOAD_DIR=${BASE_DIR}/${sub_dir}
if [ -d ${LOAD_DIR} ]; then /bin/rm -rf ${LOAD_DIR}/* ; fi
mkdir -p ${LOAD_DIR}
cd ${LOAD_DIR}

YM0=`echo ${FIRSTDAY} | cut -c1-6`
met_datbase=mv_${verif_type}_${verif_var}_b_${envir}_${YM0}
load_datbase_xml=load_${verif_type}_${verif_var}_${envir}_${YM0}.xml
NOW=${FIRSTDAY}
while [ ${NOW} -le ${LASTDAY} ]; do
    if [ "${database}" == "chem" ]; then
        cp ${DATA_DIR}/${NOW}/${capexp}_AQ* .
        cp ${DATA_DIR}/${NOW}/${capexp}_PM* .
        if [ "${capexp}" == "PROD" ] || [ "${capexp}" == "V70C55" ]; then
        ## if [ "${capexp}" == "PROD" ]; then
            cp ${DATA_DIR}/${NOW}/${capexp}_BC_AQ* .
            cp ${DATA_DIR}/${NOW}/${capexp}_BC_PM* .
        fi
    elif [ "${database}" == "meteor" ]; then
        cp ${DATA_DIR}/${NOW}/${capexp}_CAM_* .
    fi
    cdate=${NOW}"00"
    NOW=$(${NDATE} +24 ${cdate}| cut -c1-8)
done 

sed -e "s!xxTYPExx!${sub_dir}!" -e "s!xxdatabasexx!${met_datbase}!" -e "s!xxnewaddxx!${NEW_ADD}!" ${XML}/${load_datbase_template} > ${XML}/${load_datbase_xml}
if [ "${flag_new}" == "new" ]; then  
   $SCRIPT/mv_create_db_on_aws.sh ho-chun.huang ${met_datbase}
   echo "Create database done!"
fi

$SCRIPT/mv_load_to_aws.sh ho-chun.huang ${BASE_DIR} ${XML}/${load_datbase_xml}
echo "run_scrpt = ${XML}/${load_datbase_xml}"

if [ "${flag_same_month}" == "no" ]; then
    echo " Process 2nd load_aws_database for ${envir} from ${FIRSTDAY2} to ${LASTDAY2}"
    FIRSTDAY=${FIRSTDAY2}
    LASTDAY=${LASTDAY2}
    ##
    YM0=`echo ${FIRSTDAY} | cut -c1-6`
    DY0=`echo ${FIRSTDAY} | cut -c7-8`

    if [ "${DY0}" == "01" ]; then
        NEW_ADD="true"
    else   
        NEW_ADD="false"
    fi
    if [ "${NEW_ADD}" == "true" ]; then
        $SCRIPT/mv_create_db_on_aws.sh ho-chun.huang ${met_datbase}
        echo "Create new database ${met_datbase}"
    fi
    
    if [ -d ${LOAD_DIR} ]; then /bin/rm -rf ${LOAD_DIR}/* ; fi
    mkdir -p ${LOAD_DIR}
    cd ${LOAD_DIR}
    
    met_datbase=mv_${verif_type}_${verif_var}_b_${envir}_${YM0}
    load_datbase_xml=load_${verif_type}_${verif_var}_${envir}_${YM0}.xml
    NOW=${FIRSTDAY}
    while [ ${NOW} -le ${LASTDAY} ]; do
        if [ "${database}" == "chem" ]; then
            cp ${DATA_DIR}/${NOW}/${capexp}_AQ* .
            cp ${DATA_DIR}/${NOW}/${capexp}_PM* .
            if [ "${capexp}" == "PROD" ]; then
                cp ${DATA_DIR}/${NOW}/${capexp}_BC_AQ* .
                cp ${DATA_DIR}/${NOW}/${capexp}_BC_PM* .
            fi
        elif [ "${database}" == "meteor" ]; then
            cp ${DATA_DIR}/${NOW}/${capexp}_CAM_* .
        fi
        cdate=${NOW}"00"
        NOW=$(${NDATE} +24 ${cdate}| cut -c1-8)
    done 
    
    sed -e "s!xxTYPExx!${sub_dir}!" -e "s!xxdatabasexx!${met_datbase}!" -e "s!xxnewaddxx!${NEW_ADD}!" ${XML}/${load_datbase_template} > ${XML}/${load_datbase_xml}
    
    $SCRIPT/mv_load_to_aws.sh ho-chun.huang ${BASE_DIR} ${XML}/${load_datbase_xml}
    echo "run_scrpt = ${XML}/${load_datbase_xml}"
fi
exit
