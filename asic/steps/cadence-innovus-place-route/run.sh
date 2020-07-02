rm    -rf inputs/libs
mkdir -p  inputs/libs

rm    -rf inputs/lefs
mkdir -p  inputs/lefs

# LIB vector file

is_exist=$(find ./inputs -name '*-lib.list')

if [ -n "${is_exist}" ]; then

  for list in inputs/*-lib.list; do
    for lib in $(cat ${list}); do
      ln -sf ../../${lib} inputs/libs
    done
  done

fi

# LEF vector file

is_exist=$(find ./inputs -name '*-lef.list')

if [ -n "${is_exist}" ]; then

  for list in inputs/*-lef.list; do
    for lef in $(cat ${list}); do
      ln -sf ../../${lef} inputs/lefs
    done
  done

fi

# Flow

ln -sf inputs/innovus-foundation-flow
innovus -overwrite -64 -nowin -init START.tcl -log logs/run.log

# Outputs

cd outputs
ln -sf ../checkpoints/design.checkpoint
ln -sf ../typical.spef.gz      design.spef.gz
ln -sf ../results/*.gds.gz     design.gds.gz
ln -sf ../results/*.lvs.v      design.lvs.v
ln -sf ../results/*.vcs.v      design.vcs.v
ln -sf ../results/*.lef        design.lef
ln -sf ../results/*.pt.sdc     design.pt.sdc
ln -sf ../results/*.sdf        design.sdf
ln -sf ../results/*.virtuoso.v design.virtuoso.v

# Reports

ln -sf ../reports/signoff.summaryReport.rpt signoff.summaryReport.rpt
ln -sf ../reports/signoff.summary signoff.summary
