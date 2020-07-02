#include <stdio.h>
#include "stdint.h"
#include "image_parameters.h"

int image_matrix_inverse_2x2 (int32_t matrix[2][2]) {

     int32_t determinant = (matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]);
     int32_t matrix_copy[2][2];

     matrix_copy[0][0] = matrix[0][0];
     matrix_copy[0][1] = matrix[0][1];
     matrix_copy[1][0] = matrix[1][0];
     matrix_copy[1][1] = matrix[1][1];

     if (determinant == 0) { 
         ;
     } else {
 
       matrix[0][0] = matrix_copy[1][1];
       matrix[1][1] = matrix_copy[0][0];
       matrix[0][1] = (-1) * matrix_copy[0][1];
       matrix[1][0] = (-1) * matrix_copy[1][0];

     }

     

     return determinant;

}