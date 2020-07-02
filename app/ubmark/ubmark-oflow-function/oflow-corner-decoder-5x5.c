#include <stdio.h>
#include "stdint.h"
#include "image_parameters.h"
#include "common.h"

 
void corner_decoder_5x5 (
  int32_t corner_x,
  int32_t corner_y,
  int32_t image_1[image_in_rows][image_in_cols],
  int32_t image_2[image_in_rows][image_in_cols],
  int32_t window_1[5][5],
  int32_t window_2[5][5] ) {

     int i, j, k, h;
     int ii, jj, kk, hh; 

     ii = 0;
     for (i=corner_y-3; i<corner_y+2; i++) {
         jj = 0;
         for (j=corner_x-3; j<corner_x+2; j++) {
             window_1[ii][jj] = image_1[i][j];
             jj++;
         }
         ii++;
     }

     kk = 0;
     for (k=corner_y-3; k<corner_y+2; k++) {
         hh = 0;
         for (h=corner_x-3; h<corner_x+2; h++) {
             window_2[kk][hh] = image_2[k][h];
             hh++;
         }
         kk++;
     }
}