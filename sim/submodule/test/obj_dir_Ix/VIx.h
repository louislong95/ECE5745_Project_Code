// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Primary design header
//
// This header should be included by all source files instantiating the design.
// The class here is then constructed to instantiate the design.
// See the Verilator manual for examples.

#ifndef _VIx_H_
#define _VIx_H_

#include "verilated.h"

class VIx__Syms;

//----------

VL_MODULE(VIx) {
  public:
    
    // PORTS
    // The application code writes and reads these signals to
    // propagate new values into/out from the Verilated model.
    VL_IN8(reset,0,0);
    VL_IN8(clk,0,0);
    VL_IN(image_in[15],31,0);
    VL_OUT(image_out[9],31,0);
    
    // LOCAL SIGNALS
    // Internals; generally not touched by application code
    
    // LOCAL VARIABLES
    // Internals; generally not touched by application code
    IData/*31:0*/ Ix__DOT__v__DOT____Vlvbound1;
    IData/*31:0*/ Ix__DOT____Vcellout__v__image_out[9];
    IData/*31:0*/ Ix__DOT____Vcellinp__v__image_in[15];
    
    // INTERNAL VARIABLES
    // Internals; generally not touched by application code
    VIx__Syms* __VlSymsp;  // Symbol table
    
    // PARAMETERS
    // Parameters marked /*verilator public*/ for use by application code
    
    // CONSTRUCTORS
  private:
    VL_UNCOPYABLE(VIx);  ///< Copying not allowed
  public:
    /// Construct the model; called by application code
    /// The special name  may be used to make a wrapper with a
    /// single model invisible with respect to DPI scope names.
    VIx(const char* name = "TOP");
    /// Destroy the model; called (often implicitly) by application code
    ~VIx();
    
    // API METHODS
    /// Evaluate the model.  Application must call when inputs change.
    void eval();
    /// Simulation complete, run final blocks.  Application must call on completion.
    void final();
    
    // INTERNAL METHODS
  private:
    static void _eval_initial_loop(VIx__Syms* __restrict vlSymsp);
  public:
    void __Vconfigure(VIx__Syms* symsp, bool first);
  private:
    static QData _change_request(VIx__Syms* __restrict vlSymsp);
  public:
    static void _combo__TOP__1(VIx__Syms* __restrict vlSymsp);
  private:
    void _ctor_var_reset() VL_ATTR_COLD;
  public:
    static void _eval(VIx__Syms* __restrict vlSymsp);
  private:
#ifdef VL_DEBUG
    void _eval_debug_assertions();
#endif // VL_DEBUG
  public:
    static void _eval_initial(VIx__Syms* __restrict vlSymsp) VL_ATTR_COLD;
    static void _eval_settle(VIx__Syms* __restrict vlSymsp) VL_ATTR_COLD;
} VL_ATTR_ALIGNED(128);

#endif // guard
