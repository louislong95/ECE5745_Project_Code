#include <stdio.h>
#include "stdint.h"
#include "image_parameters.h"

void image_2x2_multi_2x1 (int32_t matrix_2x2[2][2], int32_t matrix_2x1[2], int32_t big_part[2]) {

     big_part[0] = matrix_2x2[0][0] * matrix_2x1[0] + matrix_2x2[0][1] * matrix_2x1[1];
     big_part[1] = matrix_2x2[1][0] * matrix_2x1[0] + matrix_2x2[1][1] * matrix_2x1[1];

}