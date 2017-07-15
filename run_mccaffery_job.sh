#!/bin/bash

let numjobs=$1
echo "Spawning ${numjobs} jobs"

SINGULARITY_IMG=/home/taritree/larbys/images/dllee_unified/singularity-dllee-unified-071017.img
WORKDIR=/home/taritree/dllee_integration/taggermetrics-singularity-scripts/
TAGGER_CFG=${WORKDIR}/pixana.cfg
INPUTLISTS=${WORKDIR}/inputlists
JOBIDLIST=${WORKDIR}/rerunlist.txt

#OUTDIR=/home/taritree/larbys/data/mcc8.1/corsika_mc/out_week0626/tagger/
OUTDIR=/home/taritree/larbys/data/mcc8.1/numu_1muNpfiltered/out_week071017/pixana/

rm -f log_mccaffery_job.txt
for (( i=0; i<$numjobs; i++ ))
do
    #SLURM_PROCID=$i ./mccaffe_test.sh &
    echo "launching job=$i" && singularity exec $SINGULARITY_IMG bash -c "export SLURM_PROCID=$i && cd ${WORKDIR} && source run_separate_pixana.sh ${WORKDIR} ${OUTDIR} ${JOBIDLIST}" >> log_mccaffery_job.txt 2>&1 &
done
