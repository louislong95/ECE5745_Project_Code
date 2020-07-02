#include <stdio.h>
#include "stdint.h"
#include "image_parameters.h"


void image_multiplication (
   int32_t image_1[num_rows][num_cols],
   int32_t image_2[num_rows][num_cols],
   int32_t image_out[num_rows][num_cols])
{
    int i, j;
    
    for (i=0; i<num_rows; i++) {
        for (j=0; j<num_cols; j++) {
            image_out[i][j] = image_1[i][j] * image_2[i][j];
         }
    }
    

}