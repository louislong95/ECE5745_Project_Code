#include <stdio.h>
#include "stdint.h"
#include "image_parameters.h"

void image_sptial_derivate_x (
  int32_t image[image_in_rows][image_in_cols],
  int32_t image_out[num_rows][num_cols],
  int32_t corner_x, int32_t corner_y )
{

    int i, j;
    int ii, jj;

    ii = 0; 
    for (i=corner_y-2; i<corner_y+1; i++) {
        jj=0;
        for (j=corner_x-2; j<corner_x+1; j++) {
            if (j==0) {
               image_out[ii][jj] = image[i][j+1] - 0;
            } //left border handling, zero-padding
            else if (j==(image_in_cols-1)) {
               image_out[ii][jj] = 0 - image[i][j-1];
            } //right border handling, zero-padding
            else if (j>(image_in_cols-1)) {
               image_out[ii][jj] = 0;
            }
            else {
               image_out[ii][jj] = image[i][j+1] - image[i][j-1];
            }
            jj++;
        }
        ii++;
    }

}