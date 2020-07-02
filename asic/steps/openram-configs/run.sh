_cur_dir=$(readlink -f $(pwd))
_top_dir=$(readlink -f $(pwd)/..)
_ref_dir=$(readlink -f ${_top_dir}/dummy)
_flw_dir=$(dirname $(readlink -f ${construct_path}))
_abs_dir=$(cd $(realpath ${_flw_dir}) && realpath ${openram_cfgs_directory})
_rel_dir=$(realpath --relative-to=${_ref_dir} ${_abs_dir})

for cfg_file in $(cat openram-cfg.input); do
  if [ -f "${_rel_dir}/${cfg_file}" ]; then
    cp ${_rel_dir}/${cfg_file} .

    _dir=$(readlink -f ${cfg_file})
    _path=$(realpath --relative-to=${_ref_dir} ${_dir})
    echo ${_path} >> openram-cfg.list
  else
    echo '[WARNING] Cannot find OpenRAM configuration file "'${cfg_file}'"'
    echo '          in the OpenRAM configurations directory "'${openram_cfgs_directory}'"'
  fi
done

(cd outputs && ln -sf ../openram-cfg.list openram-cfg.list)
