// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See VIx.h for the primary calling header

#include "VIx.h"
#include "VIx__Syms.h"


//--------------------
// STATIC VARIABLES


//--------------------

VL_CTOR_IMP(VIx) {
    VIx__Syms* __restrict vlSymsp = __VlSymsp = new VIx__Syms(this, name());
    VIx* __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    // Reset internal values
    
    // Reset structure values
    _ctor_var_reset();
}

void VIx::__Vconfigure(VIx__Syms* vlSymsp, bool first) {
    if (0 && first) {}  // Prevent unused
    this->__VlSymsp = vlSymsp;
}

VIx::~VIx() {
    delete __VlSymsp; __VlSymsp=NULL;
}

//--------------------


void VIx::eval() {
    VL_DEBUG_IF(VL_DBG_MSGF("+++++TOP Evaluate VIx::eval\n"); );
    VIx__Syms* __restrict vlSymsp = this->__VlSymsp;  // Setup global symbol table
    VIx* __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
#ifdef VL_DEBUG
    // Debug assertions
    _eval_debug_assertions();
#endif  // VL_DEBUG
    // Initialize
    if (VL_UNLIKELY(!vlSymsp->__Vm_didInit)) _eval_initial_loop(vlSymsp);
    // Evaluate till stable
    int __VclockLoop = 0;
    QData __Vchange = 1;
    do {
        VL_DEBUG_IF(VL_DBG_MSGF("+ Clock loop\n"););
        _eval(vlSymsp);
        if (VL_UNLIKELY(++__VclockLoop > 100)) {
            // About to fail, so enable debug to see what's not settling.
            // Note you must run make with OPT=-DVL_DEBUG for debug prints.
            int __Vsaved_debug = Verilated::debug();
            Verilated::debug(1);
            __Vchange = _change_request(vlSymsp);
            Verilated::debug(__Vsaved_debug);
            VL_FATAL_MT("submodule/IxVRTL.v", 23, "",
                "Verilated model didn't converge\n"
                "- See DIDNOTCONVERGE in the Verilator manual");
        } else {
            __Vchange = _change_request(vlSymsp);
        }
    } while (VL_UNLIKELY(__Vchange));
}

void VIx::_eval_initial_loop(VIx__Syms* __restrict vlSymsp) {
    vlSymsp->__Vm_didInit = true;
    _eval_initial(vlSymsp);
    // Evaluate till stable
    int __VclockLoop = 0;
    QData __Vchange = 1;
    do {
        _eval_settle(vlSymsp);
        _eval(vlSymsp);
        if (VL_UNLIKELY(++__VclockLoop > 100)) {
            // About to fail, so enable debug to see what's not settling.
            // Note you must run make with OPT=-DVL_DEBUG for debug prints.
            int __Vsaved_debug = Verilated::debug();
            Verilated::debug(1);
            __Vchange = _change_request(vlSymsp);
            Verilated::debug(__Vsaved_debug);
            VL_FATAL_MT("submodule/IxVRTL.v", 23, "",
                "Verilated model didn't DC converge\n"
                "- See DIDNOTCONVERGE in the Verilator manual");
        } else {
            __Vchange = _change_request(vlSymsp);
        }
    } while (VL_UNLIKELY(__Vchange));
}

//--------------------
// Internal Methods

VL_INLINE_OPT void VIx::_combo__TOP__1(VIx__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VIx::_combo__TOP__1\n"); );
    VIx* __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    // Body
    vlTOPp->Ix__DOT____Vcellinp__v__image_in[0U] = 
        vlTOPp->image_in[0U];
    vlTOPp->Ix__DOT____Vcellinp__v__image_in[1U] = 
        vlTOPp->image_in[1U];
    vlTOPp->Ix__DOT____Vcellinp__v__image_in[2U] = 
        vlTOPp->image_in[2U];
    vlTOPp->Ix__DOT____Vcellinp__v__image_in[3U] = 
        vlTOPp->image_in[3U];
    vlTOPp->Ix__DOT____Vcellinp__v__image_in[4U] = 
        vlTOPp->image_in[4U];
    vlTOPp->Ix__DOT____Vcellinp__v__image_in[5U] = 
        vlTOPp->image_in[5U];
    vlTOPp->Ix__DOT____Vcellinp__v__image_in[6U] = 
        vlTOPp->image_in[6U];
    vlTOPp->Ix__DOT____Vcellinp__v__image_in[7U] = 
        vlTOPp->image_in[7U];
    vlTOPp->Ix__DOT____Vcellinp__v__image_in[8U] = 
        vlTOPp->image_in[8U];
    vlTOPp->Ix__DOT____Vcellinp__v__image_in[9U] = 
        vlTOPp->image_in[9U];
    vlTOPp->Ix__DOT____Vcellinp__v__image_in[0xaU] 
        = vlTOPp->image_in[0xaU];
    vlTOPp->Ix__DOT____Vcellinp__v__image_in[0xbU] 
        = vlTOPp->image_in[0xbU];
    vlTOPp->Ix__DOT____Vcellinp__v__image_in[0xcU] 
        = vlTOPp->image_in[0xcU];
    vlTOPp->Ix__DOT____Vcellinp__v__image_in[0xdU] 
        = vlTOPp->image_in[0xdU];
    vlTOPp->Ix__DOT____Vcellinp__v__image_in[0xeU] 
        = vlTOPp->image_in[0xeU];
    vlTOPp->Ix__DOT__v__DOT____Vlvbound1 = (vlTOPp->Ix__DOT____Vcellinp__v__image_in
                                            [2U] - 
                                            vlTOPp->Ix__DOT____Vcellinp__v__image_in
                                            [0U]);
    vlTOPp->Ix__DOT____Vcellout__v__image_out[0U] = vlTOPp->Ix__DOT__v__DOT____Vlvbound1;
    vlTOPp->Ix__DOT__v__DOT____Vlvbound1 = (vlTOPp->Ix__DOT____Vcellinp__v__image_in
                                            [3U] - 
                                            vlTOPp->Ix__DOT____Vcellinp__v__image_in
                                            [1U]);
    vlTOPp->Ix__DOT____Vcellout__v__image_out[1U] = vlTOPp->Ix__DOT__v__DOT____Vlvbound1;
    vlTOPp->Ix__DOT__v__DOT____Vlvbound1 = (vlTOPp->Ix__DOT____Vcellinp__v__image_in
                                            [4U] - 
                                            vlTOPp->Ix__DOT____Vcellinp__v__image_in
                                            [2U]);
    vlTOPp->Ix__DOT____Vcellout__v__image_out[2U] = vlTOPp->Ix__DOT__v__DOT____Vlvbound1;
    vlTOPp->Ix__DOT__v__DOT____Vlvbound1 = (vlTOPp->Ix__DOT____Vcellinp__v__image_in
                                            [7U] - 
                                            vlTOPp->Ix__DOT____Vcellinp__v__image_in
                                            [5U]);
    vlTOPp->Ix__DOT____Vcellout__v__image_out[3U] = vlTOPp->Ix__DOT__v__DOT____Vlvbound1;
    vlTOPp->Ix__DOT__v__DOT____Vlvbound1 = (vlTOPp->Ix__DOT____Vcellinp__v__image_in
                                            [8U] - 
                                            vlTOPp->Ix__DOT____Vcellinp__v__image_in
                                            [6U]);
    vlTOPp->Ix__DOT____Vcellout__v__image_out[4U] = vlTOPp->Ix__DOT__v__DOT____Vlvbound1;
    vlTOPp->Ix__DOT__v__DOT____Vlvbound1 = (vlTOPp->Ix__DOT____Vcellinp__v__image_in
                                            [9U] - 
                                            vlTOPp->Ix__DOT____Vcellinp__v__image_in
                                            [7U]);
    vlTOPp->Ix__DOT____Vcellout__v__image_out[5U] = vlTOPp->Ix__DOT__v__DOT____Vlvbound1;
    vlTOPp->Ix__DOT__v__DOT____Vlvbound1 = (vlTOPp->Ix__DOT____Vcellinp__v__image_in
                                            [0xcU] 
                                            - vlTOPp->Ix__DOT____Vcellinp__v__image_in
                                            [0xaU]);
    vlTOPp->Ix__DOT____Vcellout__v__image_out[6U] = vlTOPp->Ix__DOT__v__DOT____Vlvbound1;
    vlTOPp->Ix__DOT__v__DOT____Vlvbound1 = (vlTOPp->Ix__DOT____Vcellinp__v__image_in
                                            [0xdU] 
                                            - vlTOPp->Ix__DOT____Vcellinp__v__image_in
                                            [0xbU]);
    vlTOPp->Ix__DOT____Vcellout__v__image_out[7U] = vlTOPp->Ix__DOT__v__DOT____Vlvbound1;
    vlTOPp->Ix__DOT__v__DOT____Vlvbound1 = (vlTOPp->Ix__DOT____Vcellinp__v__image_in
                                            [0xeU] 
                                            - vlTOPp->Ix__DOT____Vcellinp__v__image_in
                                            [0xcU]);
    vlTOPp->Ix__DOT____Vcellout__v__image_out[8U] = vlTOPp->Ix__DOT__v__DOT____Vlvbound1;
    vlTOPp->image_out[0U] = vlTOPp->Ix__DOT____Vcellout__v__image_out
        [0U];
    vlTOPp->image_out[1U] = vlTOPp->Ix__DOT____Vcellout__v__image_out
        [1U];
    vlTOPp->image_out[2U] = vlTOPp->Ix__DOT____Vcellout__v__image_out
        [2U];
    vlTOPp->image_out[3U] = vlTOPp->Ix__DOT____Vcellout__v__image_out
        [3U];
    vlTOPp->image_out[4U] = vlTOPp->Ix__DOT____Vcellout__v__image_out
        [4U];
    vlTOPp->image_out[5U] = vlTOPp->Ix__DOT____Vcellout__v__image_out
        [5U];
    vlTOPp->image_out[6U] = vlTOPp->Ix__DOT____Vcellout__v__image_out
        [6U];
    vlTOPp->image_out[7U] = vlTOPp->Ix__DOT____Vcellout__v__image_out
        [7U];
    vlTOPp->image_out[8U] = vlTOPp->Ix__DOT____Vcellout__v__image_out
        [8U];
}

void VIx::_eval(VIx__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VIx::_eval\n"); );
    VIx* __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    // Body
    vlTOPp->_combo__TOP__1(vlSymsp);
}

void VIx::_eval_initial(VIx__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VIx::_eval_initial\n"); );
    VIx* __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
}

void VIx::final() {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VIx::final\n"); );
    // Variables
    VIx__Syms* __restrict vlSymsp = this->__VlSymsp;
    VIx* __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
}

void VIx::_eval_settle(VIx__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VIx::_eval_settle\n"); );
    VIx* __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    // Body
    vlTOPp->_combo__TOP__1(vlSymsp);
}

VL_INLINE_OPT QData VIx::_change_request(VIx__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VIx::_change_request\n"); );
    VIx* __restrict vlTOPp VL_ATTR_UNUSED = vlSymsp->TOPp;
    // Body
    // Change detection
    QData __req = false;  // Logically a bool
    return __req;
}

#ifdef VL_DEBUG
void VIx::_eval_debug_assertions() {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VIx::_eval_debug_assertions\n"); );
    // Body
    if (VL_UNLIKELY((reset & 0xfeU))) {
        Verilated::overWidthError("reset");}
    if (VL_UNLIKELY((clk & 0xfeU))) {
        Verilated::overWidthError("clk");}
}
#endif // VL_DEBUG

void VIx::_ctor_var_reset() {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VIx::_ctor_var_reset\n"); );
    // Body
    reset = VL_RAND_RESET_I(1);
    clk = VL_RAND_RESET_I(1);
    { int __Vi0=0; for (; __Vi0<15; ++__Vi0) {
            image_in[__Vi0] = VL_RAND_RESET_I(32);
    }}
    { int __Vi0=0; for (; __Vi0<9; ++__Vi0) {
            image_out[__Vi0] = VL_RAND_RESET_I(32);
    }}
    { int __Vi0=0; for (; __Vi0<9; ++__Vi0) {
            Ix__DOT____Vcellout__v__image_out[__Vi0] = VL_RAND_RESET_I(32);
    }}
    { int __Vi0=0; for (; __Vi0<15; ++__Vi0) {
            Ix__DOT____Vcellinp__v__image_in[__Vi0] = VL_RAND_RESET_I(32);
    }}
    Ix__DOT__v__DOT____Vlvbound1 = VL_RAND_RESET_I(32);
}
