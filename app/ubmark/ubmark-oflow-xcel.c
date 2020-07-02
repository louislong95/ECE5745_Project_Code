#include "common.h"
#include "stdint.h"
#include "ubmark-oflow-function/image_parameters.h"
#include "MATLAB_app/result_MATLAB/result_data/image_data_3d.dat"
#include "MATLAB_app/result_MATLAB/result_data/corner_x_coordi.dat"
#include "MATLAB_app/result_MATLAB/result_data/corner_y_coordi.dat"
#include "MATLAB_app/result_MATLAB/result_data/corner_nums.dat"

// include the reference arrays to check the result of the baseline
#include "MATLAB_app/result_MATLAB/result_data/vx_ref.dat"
#include "MATLAB_app/result_MATLAB/result_data/vy_ref.dat"
#include "MATLAB_app/result_MATLAB/result_data/de_ref.dat"

__attribute__ ((noinline))

void verify_results (
     int32_t vx[],
     int32_t vy[],
     int32_t de[],
     int32_t vx_ref[],
     int32_t vy_ref[],
     int32_t de_ref[] ) 
{
     int32_t i;

     for (i=0; i< image_number*corner_number; i++) {
         if ( !(vx[i] == vx_ref[i]) ) {
             test_fail( i, vx[i], vx_ref[i] );
         }

         if ( !(vy[i] == vy_ref[i]) ) {
             test_fail( i, vy[i], vy_ref[i] );
         }

         if ( !(de[i] == de_ref[i]) ) {
             test_fail( i, de[i], de_ref[i] );
         }
     }  
 
     test_pass();
}

int main( int argc, char* argv[] )
{
  int32_t vx [image_number * corner_number];
  int32_t vy [image_number * corner_number];
  int32_t de [image_number * corner_number];
  int32_t num_image = image_number;
  

  int i;
  for ( i = 0; i < image_number * corner_number; i++ ) {
    vx[i] = 0;
    vy[i] = 0;
    de[i] = 0;
  }

  test_stats_on();
  asm volatile (
  
         "csrw 0x7E1, %[image_set_3d] ; \n"
         "csrw 0x7E2, %[num_image] ; \n"
         "csrw 0x7E3, %[corner_number]; \n"
         "csrw 0x7E4, %[corner_x]     ; \n"
         "csrw 0x7E5, %[corner_y]     ; \n"
         "csrw 0x7E6, %[vx]           ; \n"
         "csrw 0x7E7, %[vy]           ; \n"
         "csrw 0x7E8, %[de]           ; \n"
         "csrw 0x7E0, x0              ; \n"
         "csrr x0,    0x7E0           ; \n"

         :

         : [image_set_3d]  "r"(image_set_3d),
           [num_image]     "r"(num_image),
           [corner_number] "r"(corner_number),
           [corner_x]      "r"(corner_x),
           [corner_y]      "r"(corner_y),
           [vx]            "r"(vx),
           [vy]            "r"(vy),
           [de]            "r"(de)

         : "memory"

     );
    
  //oflow_xcel( vx, vy, de, &image_set_3d, image_number, c_n, &corner_x, &corner_y );
  
  test_stats_off();
  
  int ii;

  for (ii=0; ii<image_number * corner_number; ii++) {
      wprintf(L"%d # ", vx[ii]);
      wprintf(L"%d # ", vy[ii]);
      wprintf(L"%d \n", de[ii]);
  }

  verify_results(vx, vy, de, vx_ref, vy_ref, de_ref);

  return 0;
}