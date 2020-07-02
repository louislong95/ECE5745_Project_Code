#include <stdio.h>
#include "stdint.h"
#include "image_parameters.h"

void image_sptial_derivate_y (
  int32_t image[image_in_rows][image_in_cols],
  int32_t image_out[num_rows][num_cols],
  int32_t corner_x, int corner_y )
{

  int i, j;
  int ii, jj;

  jj = 0;
  for (j=corner_x-2; j<corner_x+1; j++) {
      ii=0;
      for (i=corner_y-2; i<corner_y+1; i++) {
          if (i==0) {
             image_out[ii][jj] = image[i+1][j] - 0;
          } //border handling
          else if (i==(image_in_rows-1)) {
             image_out[ii][jj] = 0 - image[i-1][j];
          }
          else if (i>(image_in_rows-1)) {
             image_out[ii][jj] = 0;
          }
          else {
             image_out[ii][jj] = image[i+1][j] - image[i-1][j];
          }
          ii++;
      }
      jj++;
  }
}