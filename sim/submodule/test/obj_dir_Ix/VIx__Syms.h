// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table internal header
//
// Internal details; most calling programs do not need this header,
// unless using verilator public meta comments.

#ifndef _VIx__Syms_H_
#define _VIx__Syms_H_

#include "verilated.h"

// INCLUDE MODULE CLASSES
#include "VIx.h"

// SYMS CLASS
class VIx__Syms : public VerilatedSyms {
  public:
    
    // LOCAL STATE
    const char* __Vm_namep;
    bool __Vm_didInit;
    
    // SUBCELL STATE
    VIx*                           TOPp;
    
    // CREATORS
    VIx__Syms(VIx* topp, const char* namep);
    ~VIx__Syms() {}
    
    // METHODS
    inline const char* name() { return __Vm_namep; }
    
} VL_ATTR_ALIGNED(64);

#endif  // guard
