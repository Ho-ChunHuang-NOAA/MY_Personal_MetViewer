#!/bin/sh
module load prod_util
declare -a exp=( PROD V70A1 V70B1 )
MSG="$0 new/add beg_date end_date"
TODAY=`date +%Y%m%d`
if [ $# -eq 0 ]; then
    echo ${MSG}
   exit
elif [ $# -eq 1 ]; then
    FIRSTDAY=${TODAY}
    LASTDAY=${TODAY}
elif [ $# -eq 2 ]; then
    FIRSTDAY=$2
    LASTDAY=$2
else
    FIRSTDAY=$2
    LASTDAY=$3
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

TIME_ID1=`echo ${FIRSTDAY} | cut -c1-6`
TIME_ID2=`echo ${LASTDAY} | cut -c1-6`
if [ "${TIME_ID1}" != "${TIME_ID2}" ]; then
    echo "First day ${TIME_ID1} and last day ${TIME_ID2} are not belong to the same month"
    exit
fi
## TIME_ID1=sep20
database=chem
database=meteor
if [ "${database}" == "chem" ]; then
    verif_var="o3pm"
    DATA_DIR=/lfs/h2/emc/physics/noscrub/${USER}/metplus_aq/stat/aqm
elif [ "${database}" == "meteor" ]; then
    verif_var="cam"
    DATA_DIR=/lfs/h2/emc/physics/noscrub/${USER}/metplus_cam/stat/cam
fi
verif_type=g2o_met
load_datbase_template=load_${verif_type}.base
MSG="$0 new or add database [new|add]"
if [ $# -lt 1 ]; then
   echo ${MSG}
   exit
fi
hl=`hostname | cut -c1`

SCRIPT=/lfs/h2/emc/physics/noscrub/${USER}/METviewer_AWS/script
XML=/lfs/h2/emc/physics/noscrub/${USER}/METviewer_AWS/XML
BASE_DIR=/lfs/h2/emc/stmp/${USER}/load_to_aws
LOAD_DIR=${BASE_DIR}/verif
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
for i in "${exp[@]}"; do
    capexp=`echo ${i} | tr '[:lower:]' '[:upper:]'`
    met_datbase=mv_${verif_type}_${verif_var}_${i}_${TIME_ID1}
    load_datbase_xml=load_${verif_type}_${verif_var}_${i}_${TIME_ID1}.xml
    while [ ${NOW} -le ${LASTDAY} ]; do
        if [ "${database}" == "chem" ]; then
            cp ${DATA_DIR}/${NOW}/${capexp}_AQ* .
            cp ${DATA_DIR}/${NOW}/${capexp}_PM* .
            if [ "${capexp}" == "V150A" ]; then
                cp ${DATA_DIR}/${NOW}/${capexp}_BC_AQ* .
                cp ${DATA_DIR}/${NOW}/${capexp}_BC_PM* .
            fi
        elif [ "${database}" == "meteor" ]; then
            cp ${DATA_DIR}/${NOW}/${capexp}_CAM_* .
        fi
        cdate=${NOW}"00"
        NOW=$(${NDATE} +24 ${cdate}| cut -c1-8)
    done 

## username need to be in smaller case for met database scipts
    sed -e "s!xxdatabasexx!${met_datbase}!" -e "s!xxnewaddxx!${NEW_ADD}!" ${XML}/${load_datbase_template} > ${XML}/${load_datbase_xml}
    nameis=`echo ${USER} | tr '[:upper:]' '[:lower:]'`
    if [ "${flag_new}" == "new" ]; then  
       $SCRIPT/mv_create_db_on_aws.sh ${nameis} ${met_datbase}
       echo "Create database done!"
    fi

    $SCRIPT/mv_load_to_aws.sh ${nameis} ${BASE_DIR} ${XML}/${load_datbase_xml}
done
