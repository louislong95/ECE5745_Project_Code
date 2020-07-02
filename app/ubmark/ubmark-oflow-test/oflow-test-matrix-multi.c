#include <stdio.h>
#include <stdlib.h>
#include "stdint.h"
#include "assert.h"
#include "time.h"

#include "../ubmark-oflow-function/image_parameters.h"
#include "../ubmark-oflow-function/oflow-matrix-multi.c"

void matrix_multi_type1_basic_test () {

     int32_t image_out[num_rows][num_cols];
     int32_t image_1[num_rows][num_cols] = {

                                          1, 2, 3,
                                          4, 5, 6,
                                          7, 8, 9   };

     int32_t image_2[num_rows][num_cols] = {

                                          10, 20, 30,
                                          40, 50, 60,
                                          70, 80, 90
                                                         };

     image_multiplication(image_1, image_2, image_out);

     assert( image_out[0][0] == 10  );
     assert( image_out[0][1] == 40  );
     assert( image_out[0][2] == 90  );
     assert( image_out[1][0] == 160 );
     assert( image_out[1][1] == 250 );
     assert( image_out[1][2] == 360 );
     assert( image_out[2][0] == 490 );
     assert( image_out[2][1] == 640 );
     assert( image_out[2][2] == 810 );
     printf("======== passed! (matrix_multi: basic_test_type1) ======== \n");
}

void matrix_multi_type1_large_test () {

     int32_t image_out[num_rows][num_cols];
     int32_t image_1[num_rows][num_cols] = {

                                          18243, 37513, 65372,
                                          86334, 53852, 63964,
                                          72435, 18640, 84563   };

     int32_t image_2[num_rows][num_cols] = {

                                          654, 862, 999,
                                          409, 951, 162,
                                          396, 496, 717
                                                         };

     image_multiplication(image_1, image_2, image_out);

     assert( image_out[0][0] == 11930922  );
     assert( image_out[0][1] == 32336206  );
     assert( image_out[0][2] == 65306628  );
     assert( image_out[1][0] == 35310606  );
     assert( image_out[1][1] == 51213252  );
     assert( image_out[1][2] == 10362168  );
     assert( image_out[2][0] == 28684260  );
     assert( image_out[2][1] == 9245440   );
     assert( image_out[2][2] == 60631671  );
     printf("======== passed! (matrix_multi: basic_test_type1_large_pos) ======== \n");
}

void matrix_multi_type1_large_neg_test () {

     int32_t image_out[num_rows][num_cols];
     int32_t image_1[num_rows][num_cols] = {

                                          -18243, -37513, 65372,
                                          -86334, 53852, 63964,
                                          72435, -18640, 84563   };

     int32_t image_2[num_rows][num_cols] = {

                                          654, 862, -999,
                                          409, -951, -162,
                                          -396, 496, -717
                                                         };

     image_multiplication(image_1, image_2, image_out);

     assert( image_out[0][0] == -11930922  );
     assert( image_out[0][1] == -32336206  );
     assert( image_out[0][2] == -65306628  );
     assert( image_out[1][0] == -35310606  );
     assert( image_out[1][1] == -51213252  );
     assert( image_out[1][2] == -10362168  );
     assert( image_out[2][0] == -28684260  );
     assert( image_out[2][1] == -9245440   );
     assert( image_out[2][2] == -60631671  );
     printf("======== passed! (matrix_multi: basic_test_type1_large_neg) ======== \n");
}

void matrix_multi_type1_zero_test () {

     int32_t image_out[num_rows][num_cols];
     int32_t image_1[num_rows][num_cols] = {

                                          -18243, -37513, 65372,
                                          0, 0, 63964,
                                          0, -18640, 0   };

     int32_t image_2[num_rows][num_cols] = {

                                          0, 0, 0,
                                          409, -951, 0,
                                          -396, 0, 0
                                                         };

     image_multiplication(image_1, image_2, image_out);

     assert( image_out[0][0] == 0  );
     assert( image_out[0][1] == 0  );
     assert( image_out[0][2] == 0  );
     assert( image_out[1][0] == 0  );
     assert( image_out[1][1] == 0  );
     assert( image_out[1][2] == 0  );
     assert( image_out[2][0] == 0  );
     assert( image_out[2][1] == 0   );
     assert( image_out[2][2] == 0  );
     printf("======== passed! (matrix_multi: basic_test_type1_zero) ======== \n");
}

void matrix_multi_type1_square_test () {

     int32_t image_out[num_rows][num_cols];
     int32_t image_1[num_rows][num_cols] = {

                                          182, 375, 653,
                                          360, 330, 639,
                                          473, 472, 210   };

     int32_t image_2[num_rows][num_cols] = {

                                          182, 375, 653,
                                          360, 330, 639,
                                          473, 472, 210
                                                         };

     image_multiplication(image_1, image_2, image_out);

     assert( image_out[0][0] == 182 * 182  );
     assert( image_out[0][1] == 375 * 375  );
     assert( image_out[0][2] == 653 * 653  );
     assert( image_out[1][0] == 360 * 360  );
     assert( image_out[1][1] == 330 * 330  );
     assert( image_out[1][2] == 639 * 639  );
     assert( image_out[2][0] == 473 * 473  );
     assert( image_out[2][1] == 472 * 472  );
     assert( image_out[2][2] == 210 * 210  );
     printf("======== passed! (matrix_multi: basic_test_type1_square) ======== \n");
}

void matrix_multi_type1_random_test () {

     int i, j, test_n;
     int32_t image_1  [num_rows][num_cols];
     int32_t image_2  [num_rows][num_cols];
     int32_t image_out[num_rows][num_cols];


     for (test_n=0; test_n<random_case_num; test_n++) {

        srand(time(NULL));

        for (i=0; i<num_rows; i++) {
            for (j=0; j<num_cols; j++) {
                image_1[i][j] = rand() % 10000;
            }
        }

        for (i=0; i<num_rows; i++) {
            for (j=0; j<num_cols; j++) {
                image_2[i][j] = rand() % 10000;
            }
        }

        image_multiplication(image_1, image_2, image_out);   // image_2 - image_1

        assert( image_out[0][0] == image_2[0][0] * image_1[0][0] );
        assert( image_out[0][1] == image_2[0][1] * image_1[0][1] );
        assert( image_out[0][2] == image_2[0][2] * image_1[0][2] );
        assert( image_out[1][0] == image_2[1][0] * image_1[1][0] );
        assert( image_out[1][1] == image_2[1][1] * image_1[1][1] );
        assert( image_out[1][2] == image_2[1][2] * image_1[1][2] );
        assert( image_out[2][0] == image_2[2][0] * image_1[2][0] );
        assert( image_out[2][1] == image_2[2][1] * image_1[2][1] );
        assert( image_out[2][2] == image_2[2][2] * image_1[2][2] );
     }

     printf("======== passed! (derivative_t: basic_test_type1_random) ======== \n");

}



void matrix_multi_test_collection () {

     matrix_multi_type1_basic_test();
     matrix_multi_type1_large_test();
     matrix_multi_type1_large_neg_test();
     matrix_multi_type1_zero_test();
     matrix_multi_type1_square_test();
     matrix_multi_type1_random_test();

}