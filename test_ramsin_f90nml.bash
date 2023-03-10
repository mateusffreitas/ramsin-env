#!/bin/bash
RAMSIN_BASIC=${RAMSIN_BASIC:-RAMSIN_BASIC}
RAMSIN_ADV=RAMSIN_ADVANCED
EXPNME=${EXPNME:-'Experiment'}
IMONTH1=${IMONTH1:-09}
IDATE1=${IDATE1:-06}
IYEAR1=${IYEAR1:-2022}
TIMMAX=${TIMMAX:-24}
DTLONG=${DTLONG:-30.}
FRQANL=${FRQANL:-30.}
DATE=${IYEAR1}${IMONTH1}${IDATE1}
JOBNAME=${EXPNME}-${DATE}-${TIMMAX}h
SUBMIT_DIR=${EXPNME}/${DATE}-${TIMMAX}h
SCRATCH=./
PRE_SUBMIT_DIR=$PWD

# For dataout only
OUTPREFIX=./${EXPNME}/${DATE}-${TIMMAX}h-dataout
#OUTPREFIX=${SCRATCH}/mateusff/furnas/${EXPNME}/${DATE}-${TIMMAX}h-dataout
# For datain, datafix, tables
INPREFIX=${SCRATCH}/CEMPA

mkdir -p $OUTPREFIX

f90nml -g MODEL_ADV_RAMSIN \
    -v ADVANCED_RAMSIN=\""${OUTPREFIX}"/RAMSIN_ADV_"$JOBNAME"\" \
    ${PRE_SUBMIT_DIR}/$RAMSIN_BASIC "${OUTPREFIX}"/RAMSIN_"$JOBNAME"

f90nml -g MODEL_GRIDS \
    -v EXPNME="$EXPNME" \
    -v TIMMAX=$TIMMAX \
    -v IMONTH1=$IMONTH1 \
    -v IDATE1=$IDATE1 \
    -v IYEAR1=$IYEAR1 \
    -v DTLONG=$DTLONG \
    "${OUTPREFIX}"/RAMSIN_"$JOBNAME" "${OUTPREFIX}"/RAMSIN

f90nml -g MODEL_FILE_INFO \
    -v VARFPFX=\'${OUTPREFIX}/IVAR/FRN\' \
    -v HFILOUT=\'${OUTPREFIX}/HIS/FRN\' \
    -v AFILOUT=\'${OUTPREFIX}/ANL/FRN\' \
    -v TOPFILES=\'${OUTPREFIX}/SFC/top_OQ3g_FRN\' \
    -v SFCFILES=\'${OUTPREFIX}/SFC/sfc_OQ3g_FRN\' \
    -v SSTFPFX=\'${OUTPREFIX}/SFC/sst_OQ3g_FRN\' \
    -v NDVIFPFX=\'${OUTPREFIX}/SFC/ndv_OQ3g_FRN\' \
    -v FRQANL=$FRQANL \
    -v IVEGTFN=\"/home/oper/prevtempo/datafix/MapBiomas/Bio+LU\" \
    -v ISSTFN=\"/home/oper/prevtempo/datain/sst_week/W\" \
    -v ISOILFN=\"${INPREFIX}/datafix_model/GL_FAO_INPE/FAO\" \
    -v NDVIFN=\"${INPREFIX}/datafix_model/NDVI-MODIS_GRADS/N\" \
    -v ITOPTFN=\"${INPREFIX}/datafix_model/topo1km/EL\" \
    ${OUTPREFIX}/RAMSIN ${OUTPREFIX}/RAMSIN_TMP

mv ${OUTPREFIX}/RAMSIN_TMP ${OUTPREFIX}/RAMSIN

f90nml -g MODEL_OPTIONS \
    -v USMODEL_IN=\"\" \
    -v USDATA_IN=\"${INPREFIX}/dados/SOIL_MOISTURE/dados_JULES/${IYEAR1}${IMONTH1}/AM.YYYYMMDD.nc\" \
    ${OUTPREFIX}/RAMSIN ${OUTPREFIX}/RAMSIN_TMP

mv ${OUTPREFIX}/RAMSIN_TMP ${OUTPREFIX}/RAMSIN
 
f90nml -g ISAN_CONTROL \
    -v VARPFX=\"${OUTPREFIX}/IVAR/FRN\" \
    ${OUTPREFIX}/RAMSIN ${OUTPREFIX}/RAMSIN_TMP

mv ${OUTPREFIX}/RAMSIN_TMP ${OUTPREFIX}/RAMSIN

f90nml -g ISAN_ISENTROPIC \
    -v ICFILETYPE=4 \
    -v ICPREFIX=\"${SCRATCH}/mateusff/GRADS/${DATE}00/IC\" \
    ${OUTPREFIX}/RAMSIN ${OUTPREFIX}/RAMSIN_TMP

mv ${OUTPREFIX}/RAMSIN_TMP ${OUTPREFIX}/RAMSIN

f90nml -g POST \
    -v GPREFIX=\"${OUTPREFIX}/POST/FRN25KM\" \
    ${OUTPREFIX}/RAMSIN ${OUTPREFIX}/RAMSIN_TMP

mv ${OUTPREFIX}/RAMSIN_TMP ${OUTPREFIX}/RAMSIN_"$JOBNAME"
rm ${OUTPREFIX}/RAMSIN


## RAMSIN Advanced edit

f90nml -g MODEL_FILE_INFO2 \
    -v COLTABFN=\"${INPREFIX}/tables/micro/ct2.0\" \
    -v MAPAOTFILE=\"${INPREFIX}/tables/rad_carma/infMapAOT.vfm\" \
    -v JULESIN=\"./jules.in\" \
    ${PRE_SUBMIT_DIR}/$RAMSIN_ADV "${OUTPREFIX}"/RAMSIN_ADV_TMP

mv ${OUTPREFIX}/RAMSIN_ADV_TMP ${OUTPREFIX}/RAMSIN_ADV

f90nml -g MODEL_OPTIONS2 \
    -v RADDATFN=\"${INPREFIX}/tables/rad_carma/rad_param.data\" \
    ${OUTPREFIX}/RAMSIN_ADV "${OUTPREFIX}"/RAMSIN_ADV_TMP

mv ${OUTPREFIX}/RAMSIN_ADV_TMP ${OUTPREFIX}/RAMSIN_ADV

f90nml -g ISAN_ISENTROPIC2 \
    -v ICGRADSPREFIX=\"${OUTPREFIX}/IC/icGrads\" \
    ${OUTPREFIX}/RAMSIN_ADV "${OUTPREFIX}"/RAMSIN_ADV_TMP

mv ${OUTPREFIX}/RAMSIN_ADV_TMP ${OUTPREFIX}/RAMSIN_ADV_"$JOBNAME"
rm ${OUTPREFIX}/RAMSIN_ADV
