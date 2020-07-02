#=========================================================================
# OPtical-flow XcelRTL_test
#=========================================================================

import pytest

from pymtl3                import *
#from lab2_xcel.SortXcelRTL import SortXcelRTL
from final_project.Optical_flowRTL import Optical_flowVRTL

import pytest
import random
import struct

#random.seed(0xdeadbeef)
random.seed(0xeceebeef)
from pymtl3.stdlib.ifcs.xcel_ifcs import XcelMasterIfcCL
from pymtl3.stdlib.test import TestMasterCL, mk_test_case_table, run_sim, config_model
from pymtl3.stdlib.cl.MemoryCL import MemoryCL

from proc.XcelMsg import *

#-------
#from numpy import genfromtxt
#import numpy as np
#---------

#from .SortXcelFL_test import TestHarness, test_case_table
#from .SortXcelFL_test import run_test, run_test_multiple
#from .SortXcelFL_test import run_test

#-------------------------------------------------------------------------
# TestHarness
#-------------------------------------------------------------------------
class TestHarness( Component ):

  def construct( s, xcel ):

    s.tm   = TestMasterCL( XcelMsgs.req, XcelMsgs.resp, XcelMasterIfcCL )
    s.mem  = MemoryCL( 1 )
    s.xcel = xcel

    s.tm.master  //= s.xcel.xcel
    s.mem.ifc[0] //= s.xcel.mem

  def done( s ):
    return s.tm.done()

  def line_trace( s ):
    return "{}|{} > {}".format(
      s.tm.line_trace(), s.mem.line_trace(), s.xcel.line_trace()
    )

#-------------------------------------------------------------------------
# make messages
#-------------------------------------------------------------------------

def req( type_, raddr, data ):
  return XcelReqMsg(XCEL_TYPE_READ if type_ == 'rd' else XCEL_TYPE_WRITE, raddr, data)

def resp( type_, data ):
  return XcelRespMsg(XCEL_TYPE_READ if type_ == 'rd' else XCEL_TYPE_WRITE, data)

#-------------------------------------------------------------------------
# Xcel Protocol
#-------------------------------------------------------------------------
# These are the source sink messages we need to configure the accelerator
# and wait for it to finish. We use the same messages in all of our
# tests. The difference between the tests is the data to be sorted in the
# test memory.

def gen_xcel_protocol_msgs( ):
  return [
    req( 'wr', 1, 0x5000 ), resp( 'wr', 0 ), # image_base_address
    req( 'wr', 2, 5      ), resp( 'wr', 0 ), # image number
    req( 'wr', 3, 3      ), resp( 'wr', 0 ), # corner number
    req( 'wr', 4, 0x2000 ), resp( 'wr', 0 ), # corner_x
    req( 'wr', 5, 0x2500 ), resp( 'wr', 0 ), # corner_y
    req( 'wr', 6, 0x3000 ), resp( 'wr', 0 ), # Vx
    req( 'wr', 7, 0x3500 ), resp( 'wr', 0 ), # Vy
    req( 'wr', 8, 0x4000 ), resp( 'wr', 0 ), # De
    req( 'wr', 0, 0         ), resp( 'wr', 0 ),
    req( 'rd', 0, 0         ), resp( 'rd', 1 ),
  ]

#-------------------------------------------------------------------------
# This section used for reading data (temp)
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
# Test Cases
#-------------------------------------------------------------------------
basic_data = [[    104, 105, 106, 107, 108, 109, 111, 112, 110, 111,
             112, 112, 109, 102, 115, 115, 115, 114, 113, 113,
             109, 105, 96, 98, 105, 114, 126, 135, 143, 150,
             157, 161, 531, 167, 53, 842, 351, 214, 174, 175,
             177, 182, 548, 215, 473, 543, 458, 200, 200, 201,
             202, 43, 231, 902, 621, 300, 650, 643, 543, 201,
             201, 98, 200, 999, 199, 599, 623, 199, 642, 199,
             198, 197, 196, 450, 591, 573, 753, 541, 195, 194,
             193, 192, 191, 201, 193, 163, 165, 161, 179, 164,
             151, 190, 187, 187, 187, 186, 186, 185, 184, 183 ],
            
            [104, 105, 106, 107, 108, 109, 111, 112, 110, 111,
             112, 112, 109, 102, 115, 115, 115, 114, 113, 113,
             109, 105, 96, 98, 105, 114, 126, 135, 143, 150,
             157, 161, 412, 107, 531, 481, 590, 214, 174, 175,
             177, 182, 958, 215, 125, 543, 531, 200, 200, 201,
             202, 43, 582, 952, 423, 801, 85, 243, 543, 201,
             201, 98, 200, 999, 199, 599, 623, 199, 642, 199,
             198, 197, 196, 450, 591, 573, 753, 541, 195, 194,
             193, 192, 191, 201, 193, 163, 165, 161, 179, 164,
             151, 190, 187, 187, 187, 186, 186, 185, 184, 183],
        
            [631, 354, 152, 457, 754, 563, 463, 153, 563, 124,
             351, 845, 465, 654, 904, 463, 738, 541, 43,  563,
             90,  3,   523, 152, 563, 999, 312, 463, 92,  1,
             836, 365, 451, 905, 43 , 124, 524, 512, 44,  455,
             142, 463, 573, 589, 124, 896, 376, 531, 152, 312,
             352, 906, 452, 12,  365, 76,  64,  145, 567, 125,
             748, 475, 342, 523, 541, 803, 914, 565, 351, 135,
             784, 613, 765, 753, 631, 372, 746, 356, 512, 634,
             846, 53,  461, 590, 452, 351, 906, 312, 541, 354,
             86,  76,  461, 541, 251, 573, 891, 346, 632, 348],

             [641, 354, 152, 457, 754, 563, 463, 153, 563, 124,
             351, 875, 465, 654, 904, 463, 738, 541, 43,  563,
             90,  3,   533, 152, 563, 999, 312, 463, 92,  1,
             836, 465, 451, 905, 43 , 124, 524, 512, 44,  455,
             142, 463, 573, 589, 124, 896, 376, 531, 152, 312,
             352, 906, 452, 12,  365, 76,  84,  145, 567, 125,
             748, 485, 352, 523, 541, 803, 924, 565, 351, 145,
             794, 633, 765, 753, 631, 372, 746, 356, 512, 634,
             846, 53,  461, 590, 452, 351, 926, 312, 581, 354,
             96,  76,  461, 541, 251, 573, 891, 346, 632, 348],

             [5, 8, 4, 2, 7, 3, 1, 2, 1, 8,
             3, 4, 2, 4, 9, 7, 7, 7, 6, 8,
             4, 7, 5, 1, 5, 9, 3, 4, 9, 1,
             4, 9, 4, 8, 4 ,1, 5, 5, 4, 4,
             1, 5, 3, 5, 1, 8, 3, 5, 1, 3,
             2, 4, 0, 1, 9, 7, 6, 1, 5, 1,
             1, 3, 8, 5, 5, 8, 9, 5, 3, 2,
             3, 7, 7, 7, 6, 3, 7, 3, 5, 6,
             5, 9, 5, 5, 4, 3, 9, 6, 5, 3,
             7, 4, 4, 5, 2, 5, 8, 3, 6, 3],

             [5, 8, 4, 2, 7, 3, 1, 2, 1, 8,
             6, 9, 7, 8, 9, 7, 7, 7, 6, 8,
             4, 7, 5, 4, 5, 9, 3, 4, 9, 1,
             4, 9, 8, 8, 4 ,1, 5, 5, 4, 4,
             7, 5, 3, 5, 6, 8, 3, 5, 1, 3,
             2, 4, 0, 1, 9, 7, 6, 1, 5, 1,
             1, 3, 8, 1, 5, 9, 9, 9, 7, 2,
             3, 7, 7, 7, 2, 3, 4, 3, 5, 6,
             5, 9, 5, 9, 4, 4, 9, 8, 5, 5,
             7, 4, 4, 5, 2, 5, 8, 2, 6, 3],
        
            [5,7,6, 4,6,7, 3,8,3, 7,6,5, 8,3,6], [5,7,6, 5,5,7, 3,8,8, 7,5,5, 8,5,7]]

small_data = [[  1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                 1, 1, 1, 1, 3, 2, 1, 2, 1, 1,
                 1, 1, 1, 1, 1, 2, 1, 0, 0, 0,
                 2, 3, 1, 2, 1, 0, 0, 3, 3, 1,
                 1, 2, 2, 9, 1, 5, 3, 1, 6, 1,
                 1, 1, 1, 4, 5, 3, 3, 4, 1, 4,
                 1, 2, 1, 2, 1, 3, 1, 1, 1, 4,
                 1, 1, 1, 1, 7, 1, 6, 1, 1, 1 ],
            
                [1, 2, 1, 1, 4, 1, 2, 1, 1, 3,
                 1, 1, 1, 1, 4, 1, 1, 3, 4, 1,
                 1, 2, 4, 1, 2, 1, 4, 1, 1, 1,
                 1, 1, 1, 1, 3, 2, 1, 2, 1, 1,
                 1, 2, 3, 1, 1, 2, 2, 0, 0, 0,
                 2, 3, 1, 2, 1, 3, 0, 3, 3, 5,
                 1, 2, 2, 9, 1, 5, 3, 1, 6, 1,
                 1, 1, 1, 4, 5, 3, 3, 4, 1, 4,
                 2, 2, 1, 2, 1, 3, 1, 1, 3, 4,
                 1, 3, 1, 1, 7, 1, 6, 3, 1, 1 ],
        
                [1, 1, 1, 1, 3, 1, 0, 1, 0, 1,
                 1, 5, 1, 3, 1, 1, 1, 1, 1, 1,
                 1, 1, 1, 5, 1, 1, 1, 1, 1, 0,
                 1, 1, 1, 1, 3, 2, 1, 2, 1, 1,
                 1, 3, 1, 3, 1, 5, 1, 0, 0, 0,
                 2, 4, 1, 2, 1, 0, 0, 3, 3, 1,
                 1, 2, 2, 9, 1, 5, 3, 1, 6, 4,
                 1, 0, 1, 4, 5, 3, 0, 4, 1, 4,
                 1, 2, 0, 2, 1, 3, 1, 1, 1, 4,
                 1, 1, 1, 1, 0, 1, 6, 1, 1, 1 ],

                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],

                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
                
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],

                [3,4,5, 6,7,8, 4,5,8, 5,5,5, 7,7,7], [3,4,5, 6,7,8, 4,5,8, 5,5,5, 6,6,6]]

large_data = [[  995, 996, 991, 992, 990, 993, 998, 995, 990, 990,
                 998, 999, 997, 995, 994, 995, 990, 999, 998, 998,
                 998, 997, 995, 999, 999, 993, 995, 996, 998, 998,
                 997, 993, 990, 999, 998, 991, 993, 996, 998, 999,
                 999, 994, 990, 993, 995, 992, 990, 990, 993, 994,
                 991, 993, 991, 991, 996, 999, 990, 995, 999, 991,
                 995, 998, 991, 993, 994, 997, 997, 999, 993, 996,
                 990, 996, 999, 995, 992, 999, 997, 993, 994, 996,
                 993, 994, 990, 997, 995, 995, 998, 996, 996, 997,
                 991, 997, 991, 998, 999, 993, 996, 994, 998, 996],
            
              [  997, 996, 964, 992, 990, 993, 998, 995, 990, 990,
                 945, 845, 997, 995, 994, 995, 990, 999, 998, 998,
                 898, 997, 995, 999, 999, 993, 995, 986, 998, 998,
                 977, 993, 933, 999, 998, 991, 993, 996, 998, 899,
                 999, 874, 990, 983, 985, 992, 990, 990, 993, 994,
                 991, 993, 895, 991, 996, 999, 976, 995, 899, 991,
                 995, 998, 981, 993, 994, 897, 997, 999, 993, 996,
                 990, 896, 999, 555, 992, 999, 997, 890, 994, 996,
                 993, 994, 990, 997, 888, 995, 878, 996, 997, 997,
                 991, 997, 991, 998, 999, 993, 996, 994, 998, 999],
        
              [  897, 996, 964, 992, 990, 993, 968, 795, 890, 890,
                 945, 845, 997, 995, 694, 995, 990, 999, 998, 998,
                 898, 977, 695, 899, 999, 993, 995, 986, 998, 798,
                 977, 793, 933, 699, 968, 991, 963, 696, 998, 899,
                 999, 874, 790, 683, 985, 992, 990, 990, 993, 984,
                 991, 693, 895, 961, 996, 999, 976, 995, 899, 991,
                 695, 998, 781, 993, 894, 897, 997, 799, 993, 996,
                 990, 896, 999, 555, 992, 799, 997, 890, 994, 996,
                 993, 994, 790, 997, 888, 995, 878, 996, 997, 997,
                 991, 997, 991, 998, 999, 793, 996, 994, 998, 999],

              [  497, 996, 964, 992, 990, 993, 968, 795, 890, 890,
                945, 845, 997, 995, 694, 995, 990, 999, 998, 998,
                898, 977, 695, 899, 999, 793, 985, 976, 978, 798,
                877, 693, 933, 699, 968, 991, 863, 696, 998, 899,
                989, 874, 790, 683, 785, 892, 990, 990, 993, 984,
                991, 693, 895, 761, 996, 999, 976, 995, 899, 891,
                695, 998, 781, 893, 894, 897, 997, 799, 993, 896,
                890, 896, 989, 555, 992, 799, 987, 890, 994, 896,
                893, 794, 790, 997, 888, 995, 878, 996, 997, 997,
                991, 997, 991, 998, 999, 793, 996, 994, 998, 999],

              [  497, 996, 964, 992, 990, 993, 968, 795, 890, 890,
                945, 845, 997, 995, 694, 995, 990, 999, 998, 998,
                898, 977, 695, 899, 999, 793, 985, 976, 978, 798,
                877, 693, 933, 699, 968, 991, 863, 696, 998, 899,
                989, 874, 790, 683, 785, 892, 990, 990, 993, 984,
                991, 693, 895, 761, 996, 999, 976, 995, 899, 891,
                695, 998, 781, 893, 894, 897, 997, 799, 993, 896,
                890, 896, 989, 555, 992, 799, 987, 890, 994, 896,
                893, 794, 790, 997, 888, 995, 878, 996, 997, 997,
                991, 997, 991, 998, 999, 793, 996, 994, 998, 999],

              [  497, 996, 964, 992, 990, 993, 968, 795, 890, 890,
                945, 845, 997, 995, 694, 995, 990, 999, 998, 998,
                898, 977, 695, 899, 999, 793, 985, 976, 978, 798,
                877, 693, 933, 699, 968, 991, 863, 696, 998, 899,
                989, 874, 790, 683, 785, 892, 990, 990, 993, 984,
                991, 693, 895, 761, 996, 999, 976, 995, 899, 891,
                695, 998, 781, 893, 894, 897, 997, 799, 993, 896,
                890, 896, 989, 555, 992, 799, 987, 890, 994, 896,
                893, 794, 790, 997, 888, 995, 878, 996, 997, 997,
                991, 997, 991, 998, 999, 793, 996, 994, 998, 999],

              [4,4,6, 6,8,8, 6,5,8, 6,6,6, 7,7,7], [3,4,5, 6,7,8, 4,5,7, 6,6,6, 7,7,7]]

static_data = [[  647, 987, 751, 778, 286, 299, 74, 175, 622,570,
                  95, 554, 262, 98, 389, 869, 179, 133, 595, 350,
                  970, 559, 554, 885, 563, 265, 674, 503, 769,32,
                  244, 244, 707, 309, 564, 968, 56, 496, 144, 141,
                  6, 122, 700, 435, 41, 846, 204, 460, 512, 34,
                  861, 957, 49, 594, 705, 95, 926, 782, 622, 210,
                  307, 956, 554, 246, 898, 12, 750, 670, 86, 446,
                  622, 772, 400, 238, 619, 676, 267, 676, 239,262,
                  343, 896, 978, 356, 51, 461, 280, 150, 722, 206,
                  777, 160, 953, 886, 81, 449, 601, 153, 394, 671],

              [  647, 987, 751, 778, 286, 299, 74, 175, 622,570,
                  95, 554, 262, 98, 389, 869, 179, 133, 595, 350,
                  970, 559, 554, 885, 563, 265, 674, 503, 769,32,
                  244, 244, 707, 309, 564, 968, 56, 496, 144, 141,
                  6, 122, 700, 435, 41, 846, 204, 460, 512, 34,
                  861, 957, 49, 594, 705, 95, 926, 782, 622, 210,
                  307, 956, 554, 246, 898, 12, 750, 670, 86, 446,
                  622, 772, 400, 238, 619, 676, 267, 676, 239,262,
                  343, 896, 978, 356, 51, 461, 280, 150, 722, 206,
                  777, 160, 953, 886, 81, 449, 601, 153, 394, 671],

              [  647, 987, 751, 778, 286, 299, 74, 175, 622,570,
                  95, 554, 262, 98, 389, 869, 179, 133, 595, 350,
                  970, 559, 554, 885, 563, 265, 674, 503, 769,32,
                  244, 244, 707, 309, 564, 968, 56, 496, 144, 141,
                  6, 122, 700, 435, 41, 846, 204, 460, 512, 34,
                  861, 957, 49, 594, 705, 95, 926, 782, 622, 210,
                  307, 956, 554, 246, 898, 12, 750, 670, 86, 446,
                  622, 772, 400, 238, 619, 676, 267, 676, 239,262,
                  343, 896, 978, 356, 51, 461, 280, 150, 722, 206,
                  777, 160, 953, 886, 81, 449, 601, 153, 394, 671],

              [  647, 987, 751, 778, 286, 299, 74, 175, 622,570,
                  95, 554, 262, 98, 389, 869, 179, 133, 595, 350,
                  970, 559, 554, 885, 563, 265, 674, 503, 769,32,
                  244, 244, 707, 309, 564, 968, 56, 496, 144, 141,
                  6, 122, 700, 435, 41, 846, 204, 460, 512, 34,
                  861, 957, 49, 594, 705, 95, 926, 782, 622, 210,
                  307, 956, 554, 246, 898, 12, 750, 670, 86, 446,
                  622, 772, 400, 238, 619, 676, 267, 676, 239,262,
                  343, 896, 978, 356, 51, 461, 280, 150, 722, 206,
                  777, 160, 953, 886, 81, 449, 601, 153, 394, 671],

              [  647, 987, 751, 778, 286, 299, 74, 175, 622,570,
                  95, 554, 262, 98, 389, 869, 179, 133, 595, 350,
                  970, 559, 554, 885, 563, 265, 674, 503, 769,32,
                  244, 244, 707, 309, 564, 968, 56, 496, 144, 141,
                  6, 122, 700, 435, 41, 846, 204, 460, 512, 34,
                  861, 957, 49, 594, 705, 95, 926, 782, 622, 210,
                  307, 956, 554, 246, 898, 12, 750, 670, 86, 446,
                  622, 772, 400, 238, 619, 676, 267, 676, 239,262,
                  343, 896, 978, 356, 51, 461, 280, 150, 722, 206,
                  777, 160, 953, 886, 81, 449, 601, 153, 394, 671],

              [  647, 987, 751, 778, 286, 299, 74, 175, 622,570,
                  95, 554, 262, 98, 389, 869, 179, 133, 595, 350,
                  970, 559, 554, 885, 563, 265, 674, 503, 769,32,
                  244, 244, 707, 309, 564, 968, 56, 496, 144, 141,
                  6, 122, 700, 435, 41, 846, 204, 460, 512, 34,
                  861, 957, 49, 594, 705, 95, 926, 782, 622, 210,
                  307, 956, 554, 246, 898, 12, 750, 670, 86, 446,
                  622, 772, 400, 238, 619, 676, 267, 676, 239,262,
                  343, 896, 978, 356, 51, 461, 280, 150, 722, 206,
                  777, 160, 953, 886, 81, 449, 601, 153, 394, 671],

              [4,4,6, 6,8,8, 6,5,8, 6,6,6, 7,7,7], [3,4,5, 6,7,8, 4,5,7, 6,6,6, 7,7,7]]

#-------------------------------------------------------------------------
# Test Case Table
#-------------------------------------------------------------------------

test_case_table = mk_test_case_table([
                         #                delays   test mem
                         #                -------- ---------
  (                      "basic_data            src sink stall lat"),
  [ "data",                basic_data,           0,  0,   0,    0  ],
  [ "data_delay1",         basic_data,           3,  3,   0.5,  2  ],
  [ "data_delay2",         basic_data,           3,  14,  0.5,  4  ],
  [ "data_delay3",         basic_data,           3,  10,  0.6,  4  ],
])

test_case_table_small = mk_test_case_table([
                         #                delays   test mem
                         #                -------- ---------
  (                      "small_data            src sink stall lat"),
  [ "small_data",          small_data,          0,  0,   0,    0   ],
  [ "small_data_delay",    small_data,          3,  3,   0,    0   ],
  [ "small_data_delay2",   small_data,          3,  3,   0.5,  0   ],
  [ "small_data_delay2",   small_data,          3,  10,  0.5,  0   ],
])

test_case_table_large = mk_test_case_table([
                         #                delays   test mem
                         #                -------- ---------
  (                      "large_data            src sink stall lat"),
  [ "large_data",          large_data,          0,  0,   0,    0   ],
  [ "large_data_delay",    large_data,          3,  3,   0,    0   ],
  [ "large_data_delay2",   large_data,          3,  3,   0.5,  0   ],
  [ "large_data_delay2",   large_data,          3,  10,  0.5,  0   ],
])

test_case_table_static = mk_test_case_table([
                         #                delays   test mem
                         #                -------- ---------
  (                      "static_data            src sink stall lat"),
  [ "static_data",          static_data,          0,  0,   0,    0   ],
  [ "static_data_delay",    static_data,          3,  3,   0,    0   ],
  [ "static_data_delay2",   static_data,          3,  3,   0.5,  0   ],
  [ "static_data_delay2",   static_data,          3,  10,  0.5,  0   ],
])

#-------------------------------------------------------------------------
# run_test
#-------------------------------------------------------------------------
# random test result(including the boundary point test, random value test, large number of moving points test)
Vx_test1 = [3635596964, 64180750, 101350340, 1414048758, 4092279258, 3899826252, 7865118, 4293905072, 2490388, 
           4092744757, 338598203, 3822128840, 0, 5, 0]
Vy_test1 = [342452558, 38359475, 141859744, 1070908858, 76299066, 3776469641, 4283770924, 4283464896, 4165782,
           650355333, 4089797211, 186767780, 2, 4, 0]
det_test1 = [2139453885, 407326175, 899340548, 2397465019, 743501714, 1073200221, 505675174, 504031824, 787204689,
            1022771771, 904539173, 1686436445, 4294967295, 11, 8]

# small pixel value test result
Vx_test2 = [0, 0, 2, 1, 1, 1, 0, 3, 2, 0, 0, 0, 0, 0, 0]
Vy_test2 = [0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]
det_test2 = [0, 4294967295, 4294967295, 0, 4294967295, 0, 4294967295, 4294967295, 1, 0, 0, 0, 0, 0, 0]

# large pixel value test result
Vx_test3 = [67, 36, 4294967293, 4294875688, 279177, 539106, 2252184, 13310749, 123649, 0, 0, 0, 0, 0, 0]
Vy_test3 = [4294967284, 4294967260, 18, 34728, 4294169467, 4294011100, 307697, 9227490, 4294863071, 0, 0, 0, 0, 0, 0 ]
det_test3 = [47, 33, 39, 176360, 1123269, 1352826, 19821976, 46137752, 7516129, 10570565, 10570565, 10570565, 4852936, 4852936, 4852936]

# static pixel value test result
Vx_test4 = [0,          0,       0,           0,         0,       0,       0,        0,        0,       0,        0,        0,        0,       0,       0]
Vy_test4 = [0,          0,       0,           0,         0,       0,       0,        0,        0,       0,        0,        0,        0,       0,       0]
det_test4 =[1540839359, 1303541, 2699386934,  815565238, 1123269, 1352826, 19821976, 46137752, 505675174, 10570565, 10570565, 787204689, 4852936, 4852936, 4852936]


def run_test( pytestconfig,xcel, test_params, dump_vcd=False, test_verilog=False ):

  # Convert test data into byte array

  of_data = test_params.basic_data
  image1  = of_data[::8]
  image2  = of_data[1::8]
  image3  = of_data[2::8]
  image4  = of_data[3::8]
  image5  = of_data[4::8]
  image6  = of_data[5::8]
  cornerx = of_data[6::8]
  cornery = of_data[7::8]
  #data_src0 = current_frame
  #data_src1 = next_frame
  image1_bytes = [0]*len(image1)
  image2_bytes = [0]*len(image2)
  image3_bytes = [0]*len(image3)
  image4_bytes = [0]*len(image4)
  image5_bytes = [0]*len(image5)
  image6_bytes = [0]*len(image6)
  cornerx_bytes = [0]*len(cornerx)
  cornery_bytes = [0]*len(cornery)

  for i in range( len(image1) ):
    image1_bytes[i] = struct.pack("<{}I".format(len(image1[i])),*image1[i])
    image2_bytes[i] = struct.pack("<{}I".format(len(image2[i])),*image2[i])
    image3_bytes[i] = struct.pack("<{}I".format(len(image3[i])),*image3[i])
    image4_bytes[i] = struct.pack("<{}I".format(len(image4[i])),*image4[i])
    image5_bytes[i] = struct.pack("<{}I".format(len(image5[i])),*image5[i])
    image6_bytes[i] = struct.pack("<{}I".format(len(image6[i])),*image6[i])

  for i in range( len(cornerx) ):
    cornerx_bytes[i] = struct.pack("<{}I".format(len(cornerx[i])),*cornerx[i])
    cornery_bytes[i] = struct.pack("<{}I".format(len(cornery[i])),*cornery[i])
  # Protocol messages

  xcel_protocol_msgs = []
  for i in range( 1 ): # cooment
    xcel_protocol_msgs = xcel_protocol_msgs + gen_xcel_protocol_msgs()
  xreqs  = xcel_protocol_msgs[::2]
  xresps = xcel_protocol_msgs[1::2]

  # Create test harness with protocol messagse

  th = TestHarness( xcel )

  th.set_param( "top.tm.src.construct", msgs=xcel_protocol_msgs[::2],
    initial_delay=test_params.src+3, interval_delay=test_params.src )

  th.set_param( "top.tm.sink.construct", msgs=xcel_protocol_msgs[1::2],
    initial_delay=test_params.sink+3, interval_delay=test_params.sink )

  th.set_param( "top.mem.construct",
    stall_prob=test_params.stall, latency=test_params.lat+1 )

  # Load the data into the test memory

  th.elaborate()

  for i in range( len(image1) ):
    th.mem.write_mem( 0x5000 + 4 * i,         image1_bytes[i] )
    th.mem.write_mem( 0x5000 + 4 * (i + 100), image2_bytes[i] )
    th.mem.write_mem( 0x5000 + 4 * (i + 200), image3_bytes[i] )
    th.mem.write_mem( 0x5000 + 4 * (i + 300), image4_bytes[i] )
    th.mem.write_mem( 0x5000 + 4 * (i + 400), image5_bytes[i] )
    th.mem.write_mem( 0x5000 + 4 * (i + 500), image6_bytes[i] )

  for i in range( len(cornerx) ):
    th.mem.write_mem( 0x2000 + 4 * i,         cornerx_bytes[i] )
    th.mem.write_mem( 0x2500 + 4 * i,         cornery_bytes[i] )
    #th.mem.write_mem( 0x5000 + 4 * i, image_set[1][i] )
  # Run the test

  config_model( th, dump_vcd, test_verilog, ['xcel'] )

  run_sim( th, max_cycles=20000 )

  # Retrieve data from test memory

  result_vx_bytes = [0]*len(cornerx)
  result_vy_bytes = [0]*len(cornery)
  result_de_bytes = [0]*len(cornerx)

  for i in range( 1 ):
    result_vx_bytes[i] = th.mem.read_mem( 0x3000+ 4*i, len(cornerx_bytes[i]) )
    result_vy_bytes[i] = th.mem.read_mem( 0x3500+ 4*i, len(cornerx_bytes[i]) )
    result_de_bytes[i] = th.mem.read_mem( 0x4000+ 4*i, len(cornerx_bytes[i]) )
  
  for i in range( len(result_vx_bytes) ):

    # Convert result bytes into list of ints
    result_vx = list(struct.unpack("<{}I".format(len(cornerx[i])),result_vx_bytes[i]))
    result_vy = list(struct.unpack("<{}I".format(len(cornery[i])),result_vy_bytes[i]))
    result_de = list(struct.unpack("<{}I".format(len(cornerx[i])),result_de_bytes[i]))

    # Compare result
    #for j in range( len(result) ):

  for i in range (15):
    assert result_vx[i] == Vx_test1[i]
    assert result_vy[i] == Vy_test1[i]
    assert result_de[i] == det_test1[i]

def run_test_small( pytestconfig,xcel, test_params, dump_vcd=False, test_verilog=False ):

  # Convert test data into byte array
  of_data = test_params.small_data
  image1  = of_data[::8]
  image2  = of_data[1::8]
  image3  = of_data[2::8]
  image4  = of_data[3::8]
  image5  = of_data[4::8]
  image6  = of_data[5::8]
  cornerx = of_data[6::8]
  cornery = of_data[7::8]
  #data_src0 = current_frame
  #data_src1 = next_frame
  image1_bytes = [0]*len(image1)
  image2_bytes = [0]*len(image2)
  image3_bytes = [0]*len(image3)
  image4_bytes = [0]*len(image4)
  image5_bytes = [0]*len(image5)
  image6_bytes = [0]*len(image6)
  cornerx_bytes = [0]*len(cornerx)
  cornery_bytes = [0]*len(cornery)

  for i in range( len(image1) ):
    image1_bytes[i] = struct.pack("<{}I".format(len(image1[i])),*image1[i])
    image2_bytes[i] = struct.pack("<{}I".format(len(image2[i])),*image2[i])
    image3_bytes[i] = struct.pack("<{}I".format(len(image3[i])),*image3[i])
    image4_bytes[i] = struct.pack("<{}I".format(len(image4[i])),*image4[i])
    image5_bytes[i] = struct.pack("<{}I".format(len(image5[i])),*image5[i])
    image6_bytes[i] = struct.pack("<{}I".format(len(image6[i])),*image6[i])

  for i in range( len(cornerx) ):
    cornerx_bytes[i] = struct.pack("<{}I".format(len(cornerx[i])),*cornerx[i])
    cornery_bytes[i] = struct.pack("<{}I".format(len(cornery[i])),*cornery[i])
  # Protocol messages

  xcel_protocol_msgs = []
  for i in range( 1 ): # cooment
    xcel_protocol_msgs = xcel_protocol_msgs + gen_xcel_protocol_msgs()
  xreqs  = xcel_protocol_msgs[::2]
  xresps = xcel_protocol_msgs[1::2]

  # Create test harness with protocol messagse

  th = TestHarness( xcel )

  th.set_param( "top.tm.src.construct", msgs=xcel_protocol_msgs[::2],
    initial_delay=test_params.src+3, interval_delay=test_params.src )

  th.set_param( "top.tm.sink.construct", msgs=xcel_protocol_msgs[1::2],
    initial_delay=test_params.sink+3, interval_delay=test_params.sink )

  th.set_param( "top.mem.construct",
    stall_prob=test_params.stall, latency=test_params.lat+1 )

  # Load the data into the test memory

  th.elaborate()

  for i in range( len(image1) ):
    th.mem.write_mem( 0x5000 + 4 * i,         image1_bytes[i] )
    th.mem.write_mem( 0x5000 + 4 * (i + 100), image2_bytes[i] )
    th.mem.write_mem( 0x5000 + 4 * (i + 200), image3_bytes[i] )
    th.mem.write_mem( 0x5000 + 4 * (i + 300), image4_bytes[i] )
    th.mem.write_mem( 0x5000 + 4 * (i + 400), image5_bytes[i] )
    th.mem.write_mem( 0x5000 + 4 * (i + 500), image6_bytes[i] )

  for i in range( len(cornerx) ):
    th.mem.write_mem( 0x2000 + 4 * i,         cornerx_bytes[i] )
    th.mem.write_mem( 0x2500 + 4 * i,         cornery_bytes[i] )
    #th.mem.write_mem( 0x5000 + 4 * i, image_set[1][i] )
  # Run the test

  config_model( th, dump_vcd, test_verilog, ['xcel'] )

  run_sim( th, max_cycles=20000 )

  # Retrieve data from test memory

  result_vx_bytes = [0]*len(cornerx)
  result_vy_bytes = [0]*len(cornery)
  result_de_bytes = [0]*len(cornerx)

  for i in range( 1 ):
    result_vx_bytes[i] = th.mem.read_mem( 0x3000+ 4*i, len(cornerx_bytes[i]) )
    result_vy_bytes[i] = th.mem.read_mem( 0x3500+ 4*i, len(cornerx_bytes[i]) )
    result_de_bytes[i] = th.mem.read_mem( 0x4000+ 4*i, len(cornerx_bytes[i]) )
  
  for i in range( len(result_vx_bytes) ):

    # Convert result bytes into list of ints
    result_vx = list(struct.unpack("<{}I".format(len(cornerx[i])),result_vx_bytes[i]))
    result_vy = list(struct.unpack("<{}I".format(len(cornery[i])),result_vy_bytes[i]))
    result_de = list(struct.unpack("<{}I".format(len(cornerx[i])),result_de_bytes[i]))

    # Compare result
    #for j in range( len(result) ):

  for i in range (15):
    assert result_vx[i] == Vx_test2[i]
    assert result_vy[i] == Vy_test2[i]
    assert result_de[i] == det_test2[i]

def run_test_large( pytestconfig,xcel, test_params, dump_vcd=False, test_verilog=False ):

  # Convert test data into byte array
  of_data = test_params.large_data
  image1  = of_data[::8]
  image2  = of_data[1::8]
  image3  = of_data[2::8]
  image4  = of_data[3::8]
  image5  = of_data[4::8]
  image6  = of_data[5::8]
  cornerx = of_data[6::8]
  cornery = of_data[7::8]
  #data_src0 = current_frame
  #data_src1 = next_frame
  image1_bytes = [0]*len(image1)
  image2_bytes = [0]*len(image2)
  image3_bytes = [0]*len(image3)
  image4_bytes = [0]*len(image4)
  image5_bytes = [0]*len(image5)
  image6_bytes = [0]*len(image6)
  cornerx_bytes = [0]*len(cornerx)
  cornery_bytes = [0]*len(cornery)


  for i in range( len(image1) ):
    image1_bytes[i] = struct.pack("<{}I".format(len(image1[i])),*image1[i])
    image2_bytes[i] = struct.pack("<{}I".format(len(image2[i])),*image2[i])
    image3_bytes[i] = struct.pack("<{}I".format(len(image3[i])),*image3[i])
    image4_bytes[i] = struct.pack("<{}I".format(len(image4[i])),*image4[i])
    image5_bytes[i] = struct.pack("<{}I".format(len(image5[i])),*image5[i])
    image6_bytes[i] = struct.pack("<{}I".format(len(image6[i])),*image6[i])
    
  for i in range( len(cornerx) ):
    cornerx_bytes[i] = struct.pack("<{}I".format(len(cornerx[i])),*cornerx[i])
    cornery_bytes[i] = struct.pack("<{}I".format(len(cornery[i])),*cornery[i])
  # Protocol messages

  xcel_protocol_msgs = []
  for i in range( 1 ): # cooment
    xcel_protocol_msgs = xcel_protocol_msgs + gen_xcel_protocol_msgs()
  xreqs  = xcel_protocol_msgs[::2]
  xresps = xcel_protocol_msgs[1::2]

  # Create test harness with protocol messagse

  th = TestHarness( xcel )

  th.set_param( "top.tm.src.construct", msgs=xcel_protocol_msgs[::2],
    initial_delay=test_params.src+3, interval_delay=test_params.src )

  th.set_param( "top.tm.sink.construct", msgs=xcel_protocol_msgs[1::2],
    initial_delay=test_params.sink+3, interval_delay=test_params.sink )

  th.set_param( "top.mem.construct",
    stall_prob=test_params.stall, latency=test_params.lat+1 )

  # Load the data into the test memory

  th.elaborate()

  for i in range( len(image1) ):
    th.mem.write_mem( 0x5000 + 4 * i,         image1_bytes[i] )
    th.mem.write_mem( 0x5000 + 4 * (i + 100), image2_bytes[i] )
    th.mem.write_mem( 0x5000 + 4 * (i + 200), image3_bytes[i] )
    th.mem.write_mem( 0x5000 + 4 * (i + 300), image4_bytes[i] )
    th.mem.write_mem( 0x5000 + 4 * (i + 400), image5_bytes[i] )
    th.mem.write_mem( 0x5000 + 4 * (i + 500), image6_bytes[i] )

  for i in range( len(cornerx) ):
    th.mem.write_mem( 0x2000 + 4 * i,         cornerx_bytes[i] )
    th.mem.write_mem( 0x2500 + 4 * i,         cornery_bytes[i] )
    #th.mem.write_mem( 0x5000 + 4 * i, image_set[1][i] )
  # Run the test

  config_model( th, dump_vcd, test_verilog, ['xcel'] )

  run_sim( th, max_cycles=20000 )

  # Retrieve data from test memory

  result_vx_bytes = [0]*len(cornerx)
  result_vy_bytes = [0]*len(cornery)
  result_de_bytes = [0]*len(cornerx)

  for i in range( 1 ):
    result_vx_bytes[i] = th.mem.read_mem( 0x3000+ 4*i, len(cornerx_bytes[i]) )
    result_vy_bytes[i] = th.mem.read_mem( 0x3500+ 4*i, len(cornerx_bytes[i]) )
    result_de_bytes[i] = th.mem.read_mem( 0x4000+ 4*i, len(cornerx_bytes[i]) )
  
  for i in range( len(result_vx_bytes) ):

    # Convert result bytes into list of ints
    result_vx = list(struct.unpack("<{}I".format(len(cornerx[i])),result_vx_bytes[i]))
    result_vy = list(struct.unpack("<{}I".format(len(cornery[i])),result_vy_bytes[i]))
    result_de = list(struct.unpack("<{}I".format(len(cornerx[i])),result_de_bytes[i]))

    # Compare result
    #for j in range( len(result) ):

  for i in range (15):
    assert result_vx[i] == Vx_test3[i]
    assert result_vy[i] == Vy_test3[i]
    assert result_de[i] == det_test3[i]

def run_test_static( pytestconfig,xcel, test_params, dump_vcd=False, test_verilog=False ):

  # Convert test data into byte array
  of_data = test_params.static_data
  image1  = of_data[::8]
  image2  = of_data[1::8]
  image3  = of_data[2::8]
  image4  = of_data[3::8]
  image5  = of_data[4::8]
  image6  = of_data[5::8]
  cornerx = of_data[6::8]
  cornery = of_data[7::8]
  #data_src0 = current_frame
  #data_src1 = next_frame
  image1_bytes = [0]*len(image1)
  image2_bytes = [0]*len(image2)
  image3_bytes = [0]*len(image3)
  image4_bytes = [0]*len(image4)
  image5_bytes = [0]*len(image5)
  image6_bytes = [0]*len(image6)
  cornerx_bytes = [0]*len(cornerx)
  cornery_bytes = [0]*len(cornery)


  for i in range( len(image1) ):
    image1_bytes[i] = struct.pack("<{}I".format(len(image1[i])),*image1[i])
    image2_bytes[i] = struct.pack("<{}I".format(len(image2[i])),*image2[i])
    image3_bytes[i] = struct.pack("<{}I".format(len(image3[i])),*image3[i])
    image4_bytes[i] = struct.pack("<{}I".format(len(image4[i])),*image4[i])
    image5_bytes[i] = struct.pack("<{}I".format(len(image5[i])),*image5[i])
    image6_bytes[i] = struct.pack("<{}I".format(len(image6[i])),*image6[i])
    
  for i in range( len(cornerx) ):
    cornerx_bytes[i] = struct.pack("<{}I".format(len(cornerx[i])),*cornerx[i])
    cornery_bytes[i] = struct.pack("<{}I".format(len(cornery[i])),*cornery[i])
  # Protocol messages

  xcel_protocol_msgs = []
  for i in range( 1 ): # cooment
    xcel_protocol_msgs = xcel_protocol_msgs + gen_xcel_protocol_msgs()
  xreqs  = xcel_protocol_msgs[::2]
  xresps = xcel_protocol_msgs[1::2]

  # Create test harness with protocol messagse

  th = TestHarness( xcel )

  th.set_param( "top.tm.src.construct", msgs=xcel_protocol_msgs[::2],
    initial_delay=test_params.src+3, interval_delay=test_params.src )

  th.set_param( "top.tm.sink.construct", msgs=xcel_protocol_msgs[1::2],
    initial_delay=test_params.sink+3, interval_delay=test_params.sink )

  th.set_param( "top.mem.construct",
    stall_prob=test_params.stall, latency=test_params.lat+1 )

  # Load the data into the test memory

  th.elaborate()

  for i in range( len(image1) ):
    th.mem.write_mem( 0x5000 + 4 * i,         image1_bytes[i] )
    th.mem.write_mem( 0x5000 + 4 * (i + 100), image2_bytes[i] )
    th.mem.write_mem( 0x5000 + 4 * (i + 200), image3_bytes[i] )
    th.mem.write_mem( 0x5000 + 4 * (i + 300), image4_bytes[i] )
    th.mem.write_mem( 0x5000 + 4 * (i + 400), image5_bytes[i] )
    th.mem.write_mem( 0x5000 + 4 * (i + 500), image6_bytes[i] )

  for i in range( len(cornerx) ):
    th.mem.write_mem( 0x2000 + 4 * i,         cornerx_bytes[i] )
    th.mem.write_mem( 0x2500 + 4 * i,         cornery_bytes[i] )
    #th.mem.write_mem( 0x5000 + 4 * i, image_set[1][i] )
  # Run the test

  config_model( th, dump_vcd, test_verilog, ['xcel'] )

  run_sim( th, max_cycles=20000 )

  # Retrieve data from test memory

  result_vx_bytes = [0]*len(cornerx)
  result_vy_bytes = [0]*len(cornery)
  result_de_bytes = [0]*len(cornerx)

  for i in range( 1 ):
    result_vx_bytes[i] = th.mem.read_mem( 0x3000+ 4*i, len(cornerx_bytes[i]) )
    result_vy_bytes[i] = th.mem.read_mem( 0x3500+ 4*i, len(cornerx_bytes[i]) )
    result_de_bytes[i] = th.mem.read_mem( 0x4000+ 4*i, len(cornerx_bytes[i]) )
  
  for i in range( len(result_vx_bytes) ):

    # Convert result bytes into list of ints
    result_vx = list(struct.unpack("<{}I".format(len(cornerx[i])),result_vx_bytes[i]))
    result_vy = list(struct.unpack("<{}I".format(len(cornery[i])),result_vy_bytes[i]))
    result_de = list(struct.unpack("<{}I".format(len(cornerx[i])),result_de_bytes[i]))

    # Compare result
    #for j in range( len(result) ):

#-------------------------------------------------------------------------
# Test cases
#-------------------------------------------------------------------------

@pytest.mark.parametrize( **test_case_table )
def test( pytestconfig,test_params, dump_vcd, test_verilog ):
  run_test( pytestconfig,Optical_flowVRTL(10,10,3,5), test_params, dump_vcd, test_verilog )

@pytest.mark.parametrize( **test_case_table_small )
def test_small( pytestconfig,test_params, dump_vcd, test_verilog ):
  run_test_small( pytestconfig,Optical_flowVRTL(10,10,3,5), test_params, dump_vcd, test_verilog )

@pytest.mark.parametrize( **test_case_table_large )
def test_large( pytestconfig,test_params, dump_vcd, test_verilog ):
  run_test_large( pytestconfig,Optical_flowVRTL(10,10,3,5), test_params, dump_vcd, test_verilog )

@pytest.mark.parametrize( **test_case_table_static)
def test_static( pytestconfig,test_params, dump_vcd, test_verilog ):
  run_test_static( pytestconfig,Optical_flowVRTL(10,10,3,5), test_params, dump_vcd, test_verilog )
