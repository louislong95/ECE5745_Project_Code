rm -f openram-db.list

rm -f outputs/openram-db.list

touch openram-db.list

_cur_dir=$(readlink -f $(pwd))
_top_dir=$(readlink -f $(pwd)/..)
_ref_dir=$(readlink -f ${_top_dir}/dummy)

for lib in $(cat inputs/openram-lib.list); do
  echo "Generating DB for LIB \"${lib}\""

  _base_name=$(basename ${lib} | sed -e 's/^\(.*\)\.lib/\1/g')

  db=$(echo "${_base_name}".db)
  _name="${_base_name}_lib"

  lib_name=${_name} lib_filename=${lib} db_filename=${db} lc_shell -f run.tcl

  if [ -f ${db} ]; then
    _abs_dir=$(realpath ${db})
    _rel_dir=$(realpath --relative-to=${_ref_dir} ${db})
    echo ${_rel_dir} >> openram-db.list
  fi
done

(cd outputs && ln -sf ../openram-db.list  openram-db.list)
