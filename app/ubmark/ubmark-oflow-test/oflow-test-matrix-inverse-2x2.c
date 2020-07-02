#include <stdio.h>
#include <stdlib.h>
#include "stdint.h"
#include "assert.h"
#include "time.h"

#include "../ubmark-oflow-function/image_parameters.h"
#include "../ubmark-oflow-function/oflow-matrix-inverse-2x2.c"

void matrix_inverse_2x2_basic_test () {
  
     int determinant;

     int32_t image_1[2][2] = {
                           
                                 1,2,
                                 3,4  };

     determinant = image_matrix_inverse_2x2(image_1);

     assert( determinant   == -2 );
     assert( image_1[0][0] ==  4 );
     assert( image_1[0][1] == -2 );
     assert( image_1[1][0] == -3 );
     assert( image_1[1][1] ==  1 );

     printf("======== passed! (matrix_inverse_2x2: basic_test) ======== \n");
}

void matrix_inverse_2x2_basic_test_large () {
  
     int determinant;

     int32_t image_1[2][2] = {
                           
                                 8521,2423,
                                 3124,8610  };

     determinant = image_matrix_inverse_2x2(image_1);

     assert( determinant   == 65796358 );
     assert( image_1[0][0] ==  8610 );
     assert( image_1[0][1] == -2423 );
     assert( image_1[1][0] == -3124 );
     assert( image_1[1][1] ==  8521 );

     printf("======== passed! (matrix_inverse_2x2: basic_test_large) ======== \n");
}

void matrix_inverse_2x2_basic_test_large_neg () {
  
     int determinant;

     int32_t image_1[2][2] = {
                           
                                 -8521,-2423,
                                 -3124,-8610  };

     determinant = image_matrix_inverse_2x2(image_1);

     assert( determinant   == 65796358 );
     assert( image_1[0][0] == -8610 );
     assert( image_1[0][1] == 2423 );
     assert( image_1[1][0] == 3124 );
     assert( image_1[1][1] == -8521 );

     printf("======== passed! (matrix_inverse_2x2: basic_test_large_neg) ======== \n");
}

void matrix_inverse_2x2_basic_test_zero () {
  
     int determinant;

     int32_t image_1[2][2] = {
                           
                                 3,6,
                                 2,4  };

     determinant = image_matrix_inverse_2x2(image_1);

     assert( determinant   == 0 );
     assert( image_1[0][0] == 3 );   // if determinant is 0, do not do the inverse
     assert( image_1[0][1] == 6 );
     assert( image_1[1][0] == 2 );
     assert( image_1[1][1] == 4 );

     printf("======== passed! (matrix_inverse_2x2: basic_test_zero) ======== \n");
}

void matrix_inverse_2x2_basic_test_random () {
  
     int32_t determinant;
     int32_t i, j, test_n;
     int32_t image_1[2][2];
     int32_t image_ref[2][2];

     for (test_n=0; test_n<random_case_num; test_n++) {

        srand(time(NULL));

        for (i=0; i<2; i++) {
            for (j=0; j<2; j++) {
                image_1[i][j] = rand() % 10000;
            }
        }

        for (i=0; i<2; i++) {   // copy the orginal matrix for the following assertion test
            for (j=0; j<2; j++) {
                image_ref[i][j] = image_1[i][j];
            }
        }

        determinant = image_matrix_inverse_2x2(image_1);

        assert( determinant   == image_1[0][0]*image_1[1][1] -  image_1[0][1]*image_1[1][0]);
        assert( image_1[0][0] == image_ref[1][1]        );
        assert( image_1[0][1] == image_ref[0][1] * (-1) );
        assert( image_1[1][0] == image_ref[1][0] * (-1) );
        assert( image_1[1][1] == image_ref[0][0]        );
     }

     printf("======== passed! (matrix_inverse_2x2: basic_test_random) ======== \n");
}



void matrix_inverse_2x2_test_collection () {

     matrix_inverse_2x2_basic_test();
     matrix_inverse_2x2_basic_test_large();
     matrix_inverse_2x2_basic_test_large_neg();
     matrix_inverse_2x2_basic_test_zero();
     matrix_inverse_2x2_basic_test_random();

};