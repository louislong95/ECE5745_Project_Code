#include <stdio.h>
#include "stdint.h"
#include "image_parameters.h"

int image_pixel_sum (int32_t image[num_rows][num_cols]) {

    int i, j;
    int32_t sum = 0;

    for (i=0; i<num_rows; i++) {
        for (j=0; j<num_cols; j++) {
            sum = image[i][j] + sum;
        }
    }
    //return sum;
    return sum >> 5;

}