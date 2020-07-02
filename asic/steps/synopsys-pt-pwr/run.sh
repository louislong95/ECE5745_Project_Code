rm -f *.pwr.eval

rm -rf logs
rm -rf reports
rm -rf results

mkdir -p logs
mkdir -p reports
mkdir -p results

rm    -rf inputs/dbs
mkdir -p  inputs/dbs

# DB vector file

is_exist=$(find ./inputs -name '*-db.list')

if [ -n "${is_exist}" ]; then

  for list in inputs/*-db.list; do
    for db in $(cat ${list}); do
      ln -sf ../../${db} inputs/dbs
    done
  done

fi

# Getting SAIF files

for saif_file in $(cat inputs/saif.list); do
  saif_fn=$(basename ${saif_file})
  vcd_file=$(echo ${saif_fn} | sed -e 's/^\(.*\)-scaled.saif$/\1.vcd/g')

  export saif_filename="${saif_file}"

  pt_shell -file run.tcl

  ./summarize-results ${clock_period}           \
                      ${design_name}            \
                      ${vcd_file}               \
                      ${saif_file}              \
                      reports/power-summary.rpt \
  >> ${design_name}.pwr.eval
done

if [ -f ${design_name}.pwr.eval ]; then
  (cd outputs && ln -sf ../${design_name}.pwr.eval design.pwr.eval)
fi
