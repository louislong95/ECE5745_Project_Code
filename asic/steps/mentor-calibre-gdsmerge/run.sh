#!/bin/sh
#======================================================================
# run.sh
#======================================================================
#
#  Bash script to execute the mentor-calibre-gdsmerge step
#

# For some reason, Calibre requires this directory to exist
mkdir -p $HOME/.calibrewb_workspace/tmp

# GDS Vector file

is_exist=$(find ./inputs -name '*-gds.list')

if [ -n "${is_exist}" ]; then

  for list in inputs/*-gds.list; do
    for file in $(cat ${list}); do
      ln -sf ../${file} inputs/
    done
  done

fi

# Use calibredrv to merge gds files
calibredrv -a layout filemerge \
           -indir inputs \
           -in inputs/adk/stdcells.gds \
           -topcell ${design_name} \
           -out design_merged.gds 2>&1 | tee merge.log

mkdir -p outputs && cd outputs

ln -sf ../design_merged.gds
