#!/bin/bash

# we are in the container

output_folder=$1

export DLLEE_UNIFIED_BASEDIR=/usr/local/share/dllee_unified

source /usr/local/bin/thisroot.sh
source /usr/local/share/dllee_unified/configure.sh

cd /cluster/home/twongj01/grid_jobs/metrics-tuftcluster-scripts/

jobid_list=good_jobidlist.txt

let NUM_PROCS=`cat ${jobid_list} | wc -l`
echo "number of processes: $NUM_PROCS"
if [ "$NUM_PROCS" -lt "${SLURM_PROCID}" ]; then
    echo "No Procces ID to run."
    return
fi

let "proc_line=${SLURM_PROCID}+1"
echo "sed -n ${proc_line}p ${jobid_list}"
let jobid=`sed -n ${proc_line}p ${jobid_list}`
echo "JOBID ${jobid}"

# input lists
input_src_larcv=`printf inputlists/input_src_larcv_%04d.txt ${jobid}`
input_src_larlite=`printf inputlists/input_src_larlite_%04d.txt ${jobid}`
input_tagger_larcv=`printf inputlists/input_tagger_larcv_%04d.txt ${jobid}`
input_tagger_larlite=`printf inputlists/input_tagger_larlite_%04d.txt ${jobid}`

# output file
outfile=`printf output_pixana_%04d.root ${jobid}`

# prepare workdir
workdir=`printf slurm_pixana_fileid%04d ${jobid}`
mkdir -p $workdir
cp pixana_separate.cfg $workdir/
cp $input_src_larcv $workdir/input_src_larcv.txt
cp $input_src_larlite $workdir/input_src_larlite.txt
cp $input_tagger_larcv $workdir/input_tagger_larcv.txt
cp $input_tagger_larlite $workdir/input_tagger_larlite.txt

# go to the workdir and run the program
cd $workdir
run_pixel_analysis pixana_separate.cfg >& log.txt 2>&1
mv output_pixel_analysis_test.root $outfile

cp $outfile $output_folder/