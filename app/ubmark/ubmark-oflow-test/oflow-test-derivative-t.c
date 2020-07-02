#include <stdio.h>
#include <stdlib.h>
#include "stdint.h"
#include "assert.h"
#include "time.h"

#include "../ubmark-oflow-function/image_parameters.h"
#include "../ubmark-oflow-function/oflow-derivative-t.c"

void derivative_t_basic_test () {

     int32_t image_out[num_rows][num_cols];
     int32_t image_1[num_rows][num_cols] = {

                                          1,2,3,
                                          4,5,6,
                                          7,8,9     };
                                    
     int32_t image_2 [num_rows][num_cols] = {

                                          10,20,30,
                                          40,50,60,
                                          70,80,90     };

     image_sptial_derivate_t(image_1, image_2, image_out);   // image_2 - image_1

     assert( image_out[0][0] == 9 );
     assert( image_out[0][1] == 18 );
     assert( image_out[0][2] == 27 );
     assert( image_out[1][0] == 36 );
     assert( image_out[1][1] == 45 );
     assert( image_out[1][2] == 54 );
     assert( image_out[2][0] == 63 );
     assert( image_out[2][1] == 72 );
     assert( image_out[2][2] == 81 );
     printf("======== passed! (derivative_t: basic_test_1) ======== \n");
}

void derivative_t_basic_test_negative () {

     int32_t image_out[num_rows][num_cols];
     int32_t image_1[num_rows][num_cols] = {

                                          325,34,153,
                                          411,565,806,
                                          87,81,99     };
                                    
     int32_t image_2 [num_rows][num_cols] = {

                                          10,20,30,
                                          40,50,60,
                                          70,80,90     };

     image_sptial_derivate_t(image_1, image_2, image_out);   // image_2 - image_1

     assert( image_out[0][0] == -315 );
     assert( image_out[0][1] == -14  );
     assert( image_out[0][2] == -123 );
     assert( image_out[1][0] == -371 );
     assert( image_out[1][1] == -515 );
     assert( image_out[1][2] == -746 );
     assert( image_out[2][0] == -17  );
     assert( image_out[2][1] == -1   );
     assert( image_out[2][2] == -9   );
     printf("======== passed! (derivative_t: basic_test_negative) ======== \n");
}

void derivative_t_basic_test_same () {

     int32_t image_out[num_rows][num_cols];
     int32_t image_1[num_rows][num_cols] = {

                                          325,34 ,153,
                                          411,565,806,
                                          87, 81, 99     };
                                    
     int32_t image_2 [num_rows][num_cols] = {

                                          325, 34 , 153,
                                          411, 565, 806,
                                          87,  81,  99     };

     image_sptial_derivate_t(image_1, image_2, image_out);   // image_2 - image_1

     assert( image_out[0][0] == 0 );
     assert( image_out[0][1] == 0 );
     assert( image_out[0][2] == 0 );
     assert( image_out[1][0] == 0 );
     assert( image_out[1][1] == 0 );
     assert( image_out[1][2] == 0 );
     assert( image_out[2][0] == 0 );
     assert( image_out[2][1] == 0 );
     assert( image_out[2][2] == 0 );
     printf("======== passed! (derivative_t: basic_test_same) ======== \n");
}

void derivative_t_basic_test_large_pos () {

     int32_t image_out[num_rows][num_cols];
     int32_t image_2[num_rows][num_cols] = {

                                          4265324,476444,897636,
                                          7691608,565071,806543,
                                          5135334,475135,475183     };
                                    
     int32_t image_1[num_rows][num_cols] = {

                                          126353,59316 , 581653,
                                          411235,94435 , 801245,
                                          873949,103765, 108600     };

     image_sptial_derivate_t(image_1, image_2, image_out);   // image_2 - image_1

     assert( image_out[0][0] == 4138971 );
     assert( image_out[0][1] == 417128  );
     assert( image_out[0][2] == 315983  );
     assert( image_out[1][0] == 7280373 );
     assert( image_out[1][1] == 470636  );
     assert( image_out[1][2] == 5298    );
     assert( image_out[2][0] == 4261385 );
     assert( image_out[2][1] == 371370  );
     assert( image_out[2][2] == 366583  );
     printf("======== passed! (derivative_t: basic_test_large_pos) ======== \n");
}

void derivative_t_basic_test_large_neg () {

     int32_t image_out[num_rows][num_cols];
     int32_t image_1[num_rows][num_cols] = {

                                          4265324,476444,897636,
                                          7691608,565071,806543,
                                          5135334,475135,475183     };
                                    
     int32_t image_2 [num_rows][num_cols] = {

                                          126353,59316 , 581653,
                                          411235,94435 , 801245,
                                          873949,103765, 108600     };

     image_sptial_derivate_t(image_1, image_2, image_out);   // image_2 - image_1

     assert( image_out[0][0] == -4138971 );
     assert( image_out[0][1] == -417128  );
     assert( image_out[0][2] == -315983  );
     assert( image_out[1][0] == -7280373 );
     assert( image_out[1][1] == -470636  );
     assert( image_out[1][2] == -5298    );
     assert( image_out[2][0] == -4261385 );
     assert( image_out[2][1] == -371370  );
     assert( image_out[2][2] == -366583  );
     printf("======== passed! (derivative_t: basic_test_large_neg) ======== \n");
}

void derivative_t_basic_test_random () {

     int i, j;
     int32_t image_1  [num_rows][num_cols];
     int32_t image_2  [num_rows][num_cols];
     int32_t image_out[num_rows][num_cols];

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

     image_sptial_derivate_t(image_1, image_2, image_out);   // image_2 - image_1

     assert( image_out[0][0] == image_2[0][0] - image_1[0][0] );
     assert( image_out[0][1] == image_2[0][1] - image_1[0][1] );
     assert( image_out[0][2] == image_2[0][2] - image_1[0][2] );
     assert( image_out[1][0] == image_2[1][0] - image_1[1][0] );
     assert( image_out[1][1] == image_2[1][1] - image_1[1][1] );
     assert( image_out[1][2] == image_2[1][2] - image_1[1][2] );
     assert( image_out[2][0] == image_2[2][0] - image_1[2][0] );
     assert( image_out[2][1] == image_2[2][1] - image_1[2][1] );
     assert( image_out[2][2] == image_2[2][2] - image_1[2][2] );
     printf("======== passed! (derivative_t: basic_test_random) ======== \n");
}

void derivative_t_test_collection () {

     derivative_t_basic_test();
     derivative_t_basic_test_negative();
     derivative_t_basic_test_same();
     derivative_t_basic_test_large_pos();
     derivative_t_basic_test_large_neg();
     derivative_t_basic_test_random();

}