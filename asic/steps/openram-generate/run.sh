rm -f openram-sp.list
rm -f openram-gds.list
rm -f openram-v.list
rm -f openram-lib.list
rm -f openram-lef.list

rm -f outputs/openram-sp.list
rm -f outputs/openram-gds.list
rm -f outputs/openram-v.list
rm -f outputs/openram-lib.list
rm -f outputs/openram-lef.list

touch openram-sp.list
touch openram-gds.list
touch openram-v.list
touch openram-lib.list
touch openram-lef.list

_cur_dir=$(readlink -f $(pwd))
_top_dir=$(readlink -f $(pwd)/..)
_ref_dir=$(readlink -f ${_top_dir}/dummy)

for cfg in $(cat inputs/openram-cfg.list); do
  echo "Running OpenRAM for the configuration file \"${cfg}\""
  log="$(openram -v ${cfg} 2>&1)"
  echo "${log}"

  _out_dir=$(echo "${log}" | grep "Output saved in" | sed -e 's/^.*Output saved in\s\+\(\S\+\)\/$/\1/g')

  _base_name=$(cat ${cfg} | grep "^output_name" | sed -e 's/^output_name\s*=\s*"\(.*\)"$/\1/g')
  if [ -z "${_base_name}" ]; then
    _base_name=$(basename ${cfg} | sed -e 's/^\(.*\)\.py/\1/g')
  fi

  mv ${_out_dir}/${_base_name}*.lib ${_out_dir}/${_base_name}.lib

  sed -ie 's/^\(\s*library\s*(\s*'${_base_name}'\).*\(_lib\s*).*\)$/\1\2/g' ${_out_dir}/${_base_name}.lib

  filename=$(find ${_out_dir} -name '*.sp' | head -n1)
  if [ -f ${filename} ]; then
    _abs_dir=$(realpath ${filename})
    _rel_dir=$(realpath --relative-to=${_ref_dir} ${_abs_dir})
    echo ${_rel_dir} >> openram-sp.list
  fi

  filename=$(find ${_out_dir} -name '*.gds' | head -n1)
  if [ -f ${filename} ]; then
    _abs_dir=$(realpath ${filename})
    _rel_dir=$(realpath --relative-to=${_ref_dir} ${_abs_dir})
    echo ${_rel_dir} >> openram-gds.list
  fi

  filename=$(find ${_out_dir} -name '*.v' | head -n1)
  if [ -f ${filename} ]; then
    _abs_dir=$(realpath ${filename})
    _rel_dir=$(realpath --relative-to=${_ref_dir} ${_abs_dir})
    echo ${_rel_dir} >> openram-v.list
  fi

  filename=$(find ${_out_dir} -name '*.lib' | head -n1)
  if [ -f ${filename} ]; then
    _abs_dir=$(realpath ${filename})
    _rel_dir=$(realpath --relative-to=${_ref_dir} ${_abs_dir})
    echo ${_rel_dir} >> openram-lib.list
  fi

  filename=$(find ${_out_dir} -name '*.lef' | head -n1)
  if [ -f ${filename} ]; then
    _abs_dir=$(realpath ${filename})
    _rel_dir=$(realpath --relative-to=${_ref_dir} ${_abs_dir})
    echo ${_rel_dir} >> openram-lef.list
  fi
done

(cd outputs && ln -sf ../openram-sp.list  openram-sp.list)
(cd outputs && ln -sf ../openram-gds.list openram-gds.list)
(cd outputs && ln -sf ../openram-v.list   openram-v.list)
(cd outputs && ln -sf ../openram-lib.list openram-lib.list)
(cd outputs && ln -sf ../openram-lef.list openram-lef.list)
