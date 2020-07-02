#include <stdio.h>
#include <stdlib.h>
#include "stdint.h"
#include "assert.h"
#include "time.h"

#include "../ubmark-oflow-function/image_parameters.h"
#include "../ubmark-oflow-function/oflow-matrix-2x2-multi-2x1.c"

void matrix_2x2_multi_2x1_basic_test () {

     int32_t image_out[2];

     int32_t image_1[2][2] = {
                           
                                 1,2,
                                 3,4  };

     int32_t image_2[2]    = {

                                 7,
                                 8  };

     image_2x2_multi_2x1(image_1, image_2, image_out);

     assert( image_out[0] == 23 );
     assert( image_out[1] == 53 );

     printf("======== passed! (matrix_2x2_multi_2x1: basic_test) ======== \n");

}

void matrix_2x2_multi_2x1_basic_test_large () {

     int32_t image_out[2];

     int32_t image_1[2][2] = {
                           
                                 9612,1073,
                                 9046,6535  };

     int32_t image_2[2]    = {

                                 353,
                                 245  };

     image_2x2_multi_2x1(image_1, image_2, image_out);

     assert( image_out[0] == 3655921 );
     assert( image_out[1] == 4794313 );

     printf("======== passed! (matrix_2x2_multi_2x1: basic_test_large) ======== \n");

}

void matrix_2x2_multi_2x1_basic_test_large_neg () {

     int32_t image_out[2];

     int32_t image_1[2][2] = {
                           
                                 -9612,1073,
                                 9046,-6535  };

     int32_t image_2[2]    = {

                                 -353,
                                 245  };

     image_2x2_multi_2x1(image_1, image_2, image_out);

     assert( image_out[0] ==  3655921 );
     assert( image_out[1] == -4794313 );

     printf("======== passed! (matrix_2x2_multi_2x1: basic_test_large_neg) ======== \n");

}

void matrix_2x2_multi_2x1_basic_test_zero () {

     int32_t image_out[2];

     int32_t image_1[2][2] = {
                           
                                 -9612,0,
                                 26423,0  };

     int32_t image_2[2]    = {

                                 0,
                                 245  };

     image_2x2_multi_2x1(image_1, image_2, image_out);

     assert( image_out[0] ==  0 );
     assert( image_out[1] ==  0 );

     printf("======== passed! (matrix_2x2_multi_2x1: basic_test_zero) ======== \n");

}

void matrix_2x2_multi_2x1_basic_test_random () {

     int32_t image_out[2];
     int32_t i, j, test_n;
     int32_t image_1[2][2];
     int32_t image_2[2];

     for (test_n=0; test_n<random_case_num; test_n++) {

        srand(time(NULL));

        for (i=0; i<2; i++) {
            for (j=0; j<2; j++) {
                image_1[i][j] = rand() % 10000;
            }
        }

        for (i=0; i<2; i++) {
            image_2[i] = rand() % 10000;
        }

        image_2x2_multi_2x1(image_1, image_2, image_out);

        assert( image_out[0] ==  image_1[0][0]*image_2[0] + image_1[0][1]*image_2[1] );
        assert( image_out[1] ==  image_1[1][0]*image_2[0] + image_1[1][1]*image_2[1] );
     }

     printf("======== passed! (matrix_2x2_multi_2x1: basic_test_random) ======== \n");

}


void matrix_2x2_multi_2x1_test_collection () {

     matrix_2x2_multi_2x1_basic_test();
     matrix_2x2_multi_2x1_basic_test_large();
     matrix_2x2_multi_2x1_basic_test_large_neg();
     matrix_2x2_multi_2x1_basic_test_zero();
     matrix_2x2_multi_2x1_basic_test_random();

}