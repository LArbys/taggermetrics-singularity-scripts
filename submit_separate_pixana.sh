#!/bin/bash
#
#SBATCH --job-name=separate_pixana
#SBATCH --output=log_separate_pixana.txt
#
#SBATCH --ntasks=100
#SBATCH --time=60:00
#SBATCH --mem-per-cpu=4000

WORKDIR=/cluster/kappa/90-days-archive/wongjiradlab/grid_jobs/metrics-tuftcluster-scripts
CONTAINER=/cluster/kappa/90-days-archive/wongjiradlab/larbys/images/dllee_unified/singularity-dllee-unified-071017.img
JOBIDLIST=${WORKDIR}/rerunlist.txt

OUTPUTDIR=/cluster/kappa/90-days-archive/wongjiradlab/larbys/data/mcc8.1/nue_1eNpfiltered/out_week071017/pixana
#OUTPUTDIR=/cluster/kappa/90-days-archive/wongjiradlab/larbys/data/mcc8.1/numu_1muNpfiltered/out_week071017/pixana

module load singularity

srun singularity exec ${CONTAINER} bash -c "cd ${WORKDIR} && source run_separate_pixana.sh ${WORKDIR} ${OUTPUTDIR} ${JOBIDLIST}"

