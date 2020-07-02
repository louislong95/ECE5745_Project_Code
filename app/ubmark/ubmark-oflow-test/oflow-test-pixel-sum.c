#include <stdio.h>
#include <stdlib.h>
#include "stdint.h"
#include "assert.h"
#include "time.h"

#include "../ubmark-oflow-function/image_parameters.h"
#include "../ubmark-oflow-function/oflow-pixel-sum.c"

void pixel_sum_basic_test () {

     int32_t shifted_sum;
     int32_t image_1[num_rows][num_cols] = {

                                          1, 2, 3,
                                          4, 5, 6,
                                          7, 8, 9   };

     shifted_sum = image_pixel_sum(image_1);

     assert( shifted_sum == 1  );

     printf("======== passed! (pixel_sum: basic_test) ======== \n");

}

void pixel_sum_basic_test_small () {

     int32_t shifted_sum;
     int32_t image_1[num_rows][num_cols] = {

                                          1, 1, 0,
                                          0, 2, 0,
                                          0, 3, 2   };

     shifted_sum = image_pixel_sum(image_1);

     assert( shifted_sum == 0  );

     printf("======== passed! (pixel_sum: basic_test_small) ======== \n");

}

void pixel_sum_basic_test_large () {

     int32_t shifted_sum;
     int32_t image_1[num_rows][num_cols] = {

                                          2186234, 2323457, 1243531,
                                          4671340, 4436582, 5334673,
                                          5733216, 1206357, 8345126   };

     shifted_sum = image_pixel_sum(image_1);

     assert( shifted_sum == 1108766  );

     printf("======== passed! (pixel_sum: basic_test_large) ======== \n");

}

void pixel_sum_basic_test_large_neg () {

     int32_t shifted_sum;
     int32_t image_1[num_rows][num_cols] = {

                                          -2186234, -2323457, -1243531,
                                          -4671340, -4436582, -5334673,
                                          -5733216, -1206357, -8345126   };

     shifted_sum = image_pixel_sum(image_1);

     assert( shifted_sum == -1108767  );

     printf("======== passed! (pixel_sum: basic_test_large_neg) ======== \n");

}

void pixel_sum_basic_test_random () {

     int32_t shifted_sum;
     int32_t i, j, test_n;
     int32_t image_1[num_rows][num_cols];

     for (test_n=0; test_n<random_case_num; test_n++) {

        srand(time(NULL));

        for (i=0; i<num_rows; i++) {
            for (j=0; j<num_cols; j++) {
                image_1[i][j] = rand() % 10000;
            }
        }

        shifted_sum = image_pixel_sum(image_1);

        assert( shifted_sum == (image_1[0][0]+image_1[0][1]+image_1[0][2]+image_1[1][0]
                             +  image_1[1][1]+image_1[1][2]+image_1[2][0]+image_1[2][1]
                             +  image_1[2][2]) >> 5 );
     }

     printf("======== passed! (pixel_sum: basic_test_random) ======== \n");

}



void pixel_sum_test_collection () {

     pixel_sum_basic_test();
     pixel_sum_basic_test_small();
     pixel_sum_basic_test_large();
     pixel_sum_basic_test_large_neg();
     pixel_sum_basic_test_random();

}