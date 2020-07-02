_cur_dir=$(readlink -f $(pwd))
_top_dir=$(readlink -f $(pwd)/..)
_ref_dir=$(readlink -f ${_top_dir}/dummy)

touch design.wrapped.v

cp inputs/design.v design.wrapped.v

for sram in $(cat inputs/openram-cfg.list); do

  echo "Generating wrapper for SRAM \"${sram}\""

  wrapper=$(python ./gen_wrapper.py ${sram})

  echo "${wrapper}"               > design.temp.v
  echo ""                        >> design.temp.v
  echo "$(cat design.wrapped.v)" >> design.temp.v

  # Swamp temp
  rm -f design.wrapped.v
  mv design.temp.v design.wrapped.v

done

(cd outputs && ln -sf ../design.wrapped.v  design.v)
