#!/bin/bash

# we are in the container

workdir=$1
output_folder=$2
jobid_list=$3

export DLLEE_UNIFIED_BASEDIR=/usr/local/share/dllee_unified

source /usr/local/bin/thisroot.sh
source /usr/local/share/dllee_unified/configure.sh

cd $workdir


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

# prepare jobdir
jobdir=`printf slurm_pixana_fileid%04d ${jobid}`
mkdir -p $jobdir
cp pixana_separate.cfg $jobdir/
cp $input_src_larcv $jobdir/input_src_larcv.txt
cp $input_src_larlite $jobdir/input_src_larlite.txt
cp $input_tagger_larcv $jobdir/input_tagger_larcv.txt
cp $input_tagger_larlite $jobdir/input_tagger_larlite.txt

# go to the jobdir and run the program
cd $jobdir
run_pixel_analysis pixana_separate.cfg >& log.txt 2>&1
mv output_pixel_analysis_test.root $outfile

cp $outfile $output_folder/