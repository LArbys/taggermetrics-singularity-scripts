#!/bin/bash
#
#SBATCH --job-name=separate_pixana
#SBATCH --output=slurmlog_separate_pixana.txt
#
#SBATCH --ntasks=146
#SBATCH --time=30:00
#SBATCH --mem-per-cpu=4000


module load singularity

srun singularity exec /cluster/kappa/90-days-archive/wongjiradlab/larbys/images/dllee_unified/singularity-dllee-unified-070517.img bash -c "cd /cluster/home/twongj01/grid_jobs/metrics-tuftcluster-scripts/ && source run_separate_pixana.sh"

