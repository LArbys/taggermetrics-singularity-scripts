#!/bin/bash

# we are in the container

export DLLEE_UNIFIED_BASEDIR=/usr/local/share/dllee_unified

source /usr/local/bin/thisroot.sh
source /usr/local/share/dllee_unified/configure.sh

cd /cluster/home/twongj01/grid_jobs/metrics-tuftcluster-scripts/

which run_pixel_analysis

run_pixel_analysis pixana_combined.cfg > log_pixana_combined.txt 2>&1