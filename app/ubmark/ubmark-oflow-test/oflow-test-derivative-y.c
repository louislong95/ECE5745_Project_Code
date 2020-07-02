#include <stdio.h>
#include <stdlib.h>
#include "stdint.h"
#include "assert.h"
#include "time.h"

#include "../ubmark-oflow-function/image_parameters.h"
#include "../ubmark-oflow-function/oflow-derivative-y.c"

void derivative_y_basic_test () {

     int32_t corner_x = 3;
     int32_t corner_y = 3;  // 13 is in the center

     int32_t image_out[num_rows][num_cols];
     int32_t image_1[image_in_rows][image_in_cols] = {

                                          1, 2, 3, 4, 5,
                                          6, 7, 8, 9, 10,
                                          11,12,13,14,15,
                                          16,17,18,19,20,
                                          21,22,23,24,25    };

     image_sptial_derivate_y(image_1, image_out, corner_x, corner_y);

     assert( image_out[0][0] == 10 );
     assert( image_out[0][1] == 10 );
     assert( image_out[0][2] == 10 );
     assert( image_out[1][0] == 10 );
     assert( image_out[1][1] == 10 );
     assert( image_out[1][2] == 10 );
     assert( image_out[2][0] == 10 );
     assert( image_out[2][1] == 10 );
     assert( image_out[2][2] == 10 );
     printf("======== passed! (derivative_y: basic_test_1) ======== \n");
}

void derivative_y_basic_test_corner_1 () {

     int32_t corner_x = 2;
     int32_t corner_y = 4;  // 17 is in the center

     int32_t image_out[num_rows][num_cols];
     int32_t image_1[image_in_rows][image_in_cols] = {

                                          1, 2, 3, 4, 5,
                                          6, 7, 8, 9, 10,
                                          11,12,13,14,15,
                                          16,17,18,19,20,
                                          21,22,23,24,25    };

     image_sptial_derivate_y(image_1, image_out, corner_x, corner_y);

     assert( image_out[0][0] == 10 );
     assert( image_out[0][1] == 10 );
     assert( image_out[0][2] == 10 );
     assert( image_out[1][0] == 10 );
     assert( image_out[1][1] == 10 );
     assert( image_out[1][2] == 10 );
     assert( image_out[2][0] == -16 );
     assert( image_out[2][1] == -17 );
     assert( image_out[2][2] == -18 );
     printf("======== passed! (derivative_y: basic_test_corner_1) ======== \n");

}

void derivative_y_basic_test_corner_2 () {

     int32_t corner_x = 4;
     int32_t corner_y = 2;  // 14 is in the center

     int32_t image_out[num_rows][num_cols];
     int32_t image_1[image_in_rows][image_in_cols] = {

                                          1, 2, 3, 4, 5,
                                          6, 7, 8, 9, 10,
                                          11,12,13,14,15,
                                          16,17,18,19,20,
                                          21,22,23,24,25    };

     image_sptial_derivate_y(image_1, image_out, corner_x, corner_y);

     assert( image_out[0][0] == 8 );
     assert( image_out[0][1] == 9 );
     assert( image_out[0][2] == 10 );
     assert( image_out[1][0] == 10 );
     assert( image_out[1][1] == 10 );
     assert( image_out[1][2] == 10 );
     assert( image_out[2][0] == 10 );
     assert( image_out[2][1] == 10 );
     assert( image_out[2][2] == 10 );
     printf("======== passed! (derivative_y: basic_test_corner_2) ======== \n");

}

void derivative_y_basic_test_large () {

     int32_t corner_x = 3;
     int32_t corner_y = 3;  // 476945 is in the center

     int32_t image_out[num_rows][num_cols];
     int32_t image_1[image_in_rows][image_in_cols] = {

                                          114287, 231247, 346657, 435774, 592376,
                                          659876, 745657, 898127, 448635, 100903,
                                          486502, 572349, 476945, 697346, 154562,
                                          580593, 697235, 597345, 596735, 209762,
                                          560735, 604167, 926495, 720957, 103305    };

     image_sptial_derivate_y(image_1, image_out, corner_x, corner_y);

     assert( image_out[0][0] == (572349 - 231247));
     assert( image_out[0][1] == (476945 - 346657) );
     assert( image_out[0][2] == (697346 - 435774) );
     assert( image_out[1][0] == (697235 - 745657) );
     assert( image_out[1][1] == (597345 - 898127) );
     assert( image_out[1][2] == (596735 - 448635) );
     assert( image_out[2][0] == (604167 - 572349) );
     assert( image_out[2][1] == (926495 - 476945) );
     assert( image_out[2][2] == (720957 - 697346) );
     printf("======== passed! (derivative_y: basic_test_corner_large) ======== \n");

}

void derivative_y_basic_test_negative () {

     int32_t corner_x = 3;
     int32_t corner_y = 3;  // 476945 is in the center

     int32_t image_out[num_rows][num_cols];
     int32_t image_1[image_in_rows][image_in_cols] = {

                                          -114287, -231247, -346657, -435774, -592376,
                                          -659876, -745657, -898127, -448635, -100903,
                                          -486502, -572349, -476945, -697346, -154562,
                                          -580593, -697235, -597345, -596735, -209762,
                                          -560735, -604167, -926495, -720957, -103305    };

     image_sptial_derivate_y(image_1, image_out, corner_x, corner_y);

     assert( image_out[0][0] == -(572349 - 231247));
     assert( image_out[0][1] == -(476945 - 346657) );
     assert( image_out[0][2] == -(697346 - 435774) );
     assert( image_out[1][0] == -(697235 - 745657) );
     assert( image_out[1][1] == -(597345 - 898127) );
     assert( image_out[1][2] == -(596735 - 448635) );
     assert( image_out[2][0] == -(604167 - 572349) );
     assert( image_out[2][1] == -(926495 - 476945) );
     assert( image_out[2][2] == -(720957 - 697346) );
     printf("======== passed! (derivative_y: basic_test_corner_negative) ======== \n");

}

void derivative_y_random_test () {
     
     int i, j;
     int32_t image_1[image_in_rows][image_in_cols];
     int32_t corner_x = 3;
     int32_t corner_y = 3;  // locate in the center of 5x5 matrix
     int32_t image_out[num_rows][num_cols];
     srand(time(NULL));

     for (i=0; i<image_in_rows; i++) {
         for (j=0; j<image_in_cols; j++) {
             image_1[i][j] = rand() % 10000;
         }
     }

     image_sptial_derivate_y(image_1, image_out, corner_x, corner_y);

     assert( image_out[0][0] == (image_1[2][1] - image_1[0][1]));
     assert( image_out[0][1] == (image_1[2][2] - image_1[0][2]) );
     assert( image_out[0][2] == (image_1[2][3] - image_1[0][3]) );
     assert( image_out[1][0] == (image_1[3][1] - image_1[1][1]) );
     assert( image_out[1][1] == (image_1[3][2] - image_1[1][2]) );
     assert( image_out[1][2] == (image_1[3][3] - image_1[1][3]) );
     assert( image_out[2][0] == (image_1[4][1] - image_1[2][1]) );
     assert( image_out[2][1] == (image_1[4][2] - image_1[2][2]) );
     assert( image_out[2][2] == (image_1[4][3] - image_1[2][3]) );
     printf("======== passed! (derivative_y: basic_test_random) ======== \n");

}


void derivative_y_test_collection () {

    derivative_y_basic_test();
    derivative_y_basic_test_corner_1();
    derivative_y_basic_test_corner_2();
    derivative_y_basic_test_large();
    derivative_y_basic_test_negative();
    derivative_y_random_test();

}