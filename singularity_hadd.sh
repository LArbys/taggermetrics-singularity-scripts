#!/bin/bash

# TUFTS
#LARBYSDIR=/cluster/kappa/90-days-archive/wongjiradlab/larbys

# MCCAFFREY
LARBYSDIR=/home/taritree/larbys

# MCCAFFREY
CONTAINER=${LARBYSDIR}/images/dllee_unified/singularity-dllee-unified-071017.img

#OUTPUTDIR=${LARBYSDIR}/data/mcc8.1/nue_1eNpfiltered/out_week071017/pixana
OUTPUTDIR=${LARBYSDIR}/data/mcc8.1/numu_1muNpfiltered/out_week071017/pixana

MERGEDFILE=${LARBYSDIR}/data/mcc8.1/numu_1muNpfiltered/out_week071017/pixana_merged.root

module load singularity
singularity exec ${CONTAINER} bash -c "source /usr/local/bin/thisroot.sh && hadd -f ${MERGEDFILE} ${OUTPUTDIR}/*.root"

