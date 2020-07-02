#include <stdio.h>
#include <stdlib.h>
#include "stdint.h"
#include "assert.h"
#include "time.h"

#include "../ubmark-oflow-function/image_parameters.h"
#include "../ubmark-oflow-function/oflow-derivative-x.c"

void derivative_x_basic_test () {

     int32_t corner_x = 3;
     int32_t corner_y = 3;  // 13 is in the center

     int32_t image_out[num_rows][num_cols];
     int32_t image_1[image_in_rows][image_in_cols] = {

                                          1, 2, 3, 4, 5,
                                          6, 7, 8, 9, 10,
                                          11,12,13,14,15,
                                          16,17,18,19,20,
                                          21,22,23,24,25    };

     image_sptial_derivate_x(image_1, image_out, corner_x, corner_y);

     assert( image_out[0][0] == 2 );
     assert( image_out[0][1] == 2 );
     assert( image_out[0][2] == 2 );
     assert( image_out[1][0] == 2 );
     assert( image_out[1][1] == 2 );
     assert( image_out[1][2] == 2 );
     assert( image_out[2][0] == 2 );
     assert( image_out[2][1] == 2 );
     assert( image_out[2][2] == 2 );
     printf("======== passed! (derivative_x: basic_test_1) ======== \n");
}

void derivative_x_basic_test_corner_1 () {

     int32_t corner_x = 2;
     int32_t corner_y = 4;  // 17 is in the center

     int32_t image_out[num_rows][num_cols];
     int32_t image_1[image_in_rows][image_in_cols] = {

                                          1, 2, 3, 4, 5,
                                          6, 7, 8, 9, 10,
                                          11,12,13,14,15,
                                          16,17,18,19,20,
                                          21,22,23,24,25    };

     image_sptial_derivate_x(image_1, image_out, corner_x, corner_y);

     assert( image_out[0][0] == 12 );
     assert( image_out[0][1] == 2 );
     assert( image_out[0][2] == 2 );
     assert( image_out[1][0] == 17 );
     assert( image_out[1][1] == 2 );
     assert( image_out[1][2] == 2 );
     assert( image_out[2][0] == 22 );
     assert( image_out[2][1] == 2 );
     assert( image_out[2][2] == 2 );
     printf("======== passed! (derivative_x: basic_test_corner_1) ======== \n");

}

void derivative_x_basic_test_corner_2 () {

     int32_t corner_x = 4;
     int32_t corner_y = 3;  // 14 is in the center

     int32_t image_out[num_rows][num_cols];
     int32_t image_1[image_in_rows][image_in_cols] = {

                                          1, 2, 3, 4, 5,
                                          6, 7, 8, 9, 10,
                                          11,12,13,14,15,
                                          16,17,18,19,20,
                                          21,22,23,24,25    };

     image_sptial_derivate_x(image_1, image_out, corner_x, corner_y);

     assert( image_out[0][0] == 2 );
     assert( image_out[0][1] == 2 );
     assert( image_out[0][2] == -9 );
     assert( image_out[1][0] == 2 );
     assert( image_out[1][1] == 2 );
     assert( image_out[1][2] == -14 );
     assert( image_out[2][0] == 2 );
     assert( image_out[2][1] == 2 );
     assert( image_out[2][2] == -19 );
     printf("======== passed! (derivative_x: basic_test_corner_2) ======== \n");

}

void derivative_x_basic_test_large () {

     int32_t corner_x = 3;
     int32_t corner_y = 3;  // 476945 is in the center

     int32_t image_out[num_rows][num_cols];
     int32_t image_1[image_in_rows][image_in_cols] = {

                                          114287, 231247, 346657, 435774, 592376,
                                          659876, 745657, 898127, 448635, 100903,
                                          486502, 572349, 476945, 697346, 154562,
                                          580593, 697235, 597345, 596735, 209762,
                                          560735, 604167, 926495, 720957, 103305    };

     image_sptial_derivate_x(image_1, image_out, corner_x, corner_y);

     assert( image_out[0][0] == (898127 - 659876));
     assert( image_out[0][1] == (448635 - 745657) );
     assert( image_out[0][2] == (100903 - 898127) );
     assert( image_out[1][0] == (476945 - 486502) );
     assert( image_out[1][1] == (697346 - 572349) );
     assert( image_out[1][2] == (154562 - 476945) );
     assert( image_out[2][0] == (597345 - 580593) );
     assert( image_out[2][1] == (596735 - 697235) );
     assert( image_out[2][2] == (209762 - 597345) );
     printf("======== passed! (derivative_x: basic_test_corner_large) ======== \n");

}

void derivative_x_basic_test_negtive () {

     int32_t corner_x = 3;
     int32_t corner_y = 3;  // 476945 is in the center

     int32_t image_out[num_rows][num_cols];
     int32_t image_1[image_in_rows][image_in_cols] = {

                                          -114287, -231247, -346657, -435774, -592376,
                                          -659876, -745657, -898127, -448635, -100903,
                                          -486502, -572349, -476945, -697346, -154562,
                                          -580593, -697235, -597345, -596735, -209762,
                                          -560735, -604167, -926495, -720957, -103305    };

     image_sptial_derivate_x(image_1, image_out, corner_x, corner_y);

     assert( image_out[0][0] == -(898127 - 659876));
     assert( image_out[0][1] == -(448635 - 745657) );
     assert( image_out[0][2] == -(100903 - 898127) );
     assert( image_out[1][0] == -(476945 - 486502) );
     assert( image_out[1][1] == -(697346 - 572349) );
     assert( image_out[1][2] == -(154562 - 476945) );
     assert( image_out[2][0] == -(597345 - 580593) );
     assert( image_out[2][1] == -(596735 - 697235) );
     assert( image_out[2][2] == -(209762 - 597345) );
     printf("======== passed! (derivative_x: basic_test_corner_negative) ======== \n");

}

void derivative_x_random_test () {
     
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

     image_sptial_derivate_x(image_1, image_out, corner_x, corner_y);

     assert( image_out[0][0] == (image_1[1][2] - image_1[1][0]));
     assert( image_out[0][1] == (image_1[1][3] - image_1[1][1]) );
     assert( image_out[0][2] == (image_1[1][4] - image_1[1][2]) );
     assert( image_out[1][0] == (image_1[2][2] - image_1[2][0]) );
     assert( image_out[1][1] == (image_1[2][3] - image_1[2][1]) );
     assert( image_out[1][2] == (image_1[2][4] - image_1[2][2]) );
     assert( image_out[2][0] == (image_1[3][2] - image_1[3][0]) );
     assert( image_out[2][1] == (image_1[3][3] - image_1[3][1]) );
     assert( image_out[2][2] == (image_1[3][4] - image_1[3][2]) );
     printf("======== passed! (derivative_x: basic_test_random) ======== \n");

}


void derivative_x_test_collection () {

    derivative_x_basic_test();
    derivative_x_basic_test_corner_1();
    derivative_x_basic_test_corner_2();
    derivative_x_basic_test_large();
    derivative_x_basic_test_negtive();
    derivative_x_random_test();

}