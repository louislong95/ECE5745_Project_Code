#include <stdio.h>
#include <stdlib.h>
#include "stdint.h"
#include "assert.h"
#include "time.h"

#include "../ubmark-oflow-function/image_parameters.h"
#include "../ubmark-oflow-function/oflow-corner-decoder.c"


void corner_decoder_basic_test_1 ( ) {

  int32_t corner_x = 3;
  int32_t corner_y = 3;  // the center point is 13

  int32_t image_1[image_in_rows][image_in_cols] = {

                                          1, 2, 3, 4, 5,
                                          6, 7, 8, 9, 10,
                                          11,12,13,14,15,
                                          16,17,18,19,20,
                                          21,22,23,24,25    };

  int32_t image_2[image_in_rows][image_in_cols] = {

                                          10, 20, 30, 40, 50,
                                          60, 70, 80, 90, 100,
                                          110,120,130,140,150,
                                          160,170,180,190,200,
                                          210,220,230,240,250    };

  int32_t window_1[num_rows][num_cols];
  int32_t window_2[num_rows][num_cols];

  corner_decoder(corner_x, corner_y, image_1, image_2, window_1, window_2);

  assert ( window_1[0][0] == 7 );
  assert ( window_1[0][1] == 8 );
  assert ( window_1[0][2] == 9 );
  assert ( window_1[1][0] == 12 );
  assert ( window_1[1][1] == 13 );
  assert ( window_1[1][2] == 14 );
  assert ( window_1[2][0] == 17 );
  assert ( window_1[2][1] == 18 );
  assert ( window_1[2][2] == 19 );

  assert ( window_2[0][0] == 70 );
  assert ( window_2[0][1] == 80 );
  assert ( window_2[0][2] == 90 );
  assert ( window_2[1][0] == 120 );
  assert ( window_2[1][1] == 130 );
  assert ( window_2[1][2] == 140 );
  assert ( window_2[2][0] == 170 );
  assert ( window_2[2][1] == 180 );
  assert ( window_2[2][2] == 190 );
  printf("======== passed! (corner_decoder: 1) ======== \n");
}

void corner_decoder_basic_test_edge ( ) {

  int32_t corner_x;
  int32_t corner_y;  // the center point is 13
  corner_x = 2;
  corner_y = 4;

  int32_t image_1[image_in_rows][image_in_cols] = {

                                          1, 2, 3, 4, 5,
                                          6, 7, 8, 9, 10,
                                          11,12,13,14,15,
                                          16,17,18,19,20,
                                          21,22,23,24,25    };

  int32_t image_2[image_in_rows][image_in_cols] = {

                                          10, 20, 30, 40, 50,
                                          60, 70, 80, 90, 100,
                                          110,120,130,140,150,
                                          160,170,180,190,200,
                                          210,220,230,240,250    };

  int32_t window_1[num_rows][num_cols];
  int32_t window_2[num_rows][num_cols];

  corner_decoder(corner_x, corner_y, image_1, image_2, window_1, window_2);

  assert ( window_1[0][0] == 11 );
  assert ( window_1[0][1] == 12 );
  assert ( window_1[0][2] == 13 );
  assert ( window_1[1][0] == 16 );
  assert ( window_1[1][1] == 17 );
  assert ( window_1[1][2] == 18 );
  assert ( window_1[2][0] == 21 );
  assert ( window_1[2][1] == 22 );
  assert ( window_1[2][2] == 23 );

  assert ( window_2[0][0] == 110 );
  assert ( window_2[0][1] == 120 );
  assert ( window_2[0][2] == 130 );
  assert ( window_2[1][0] == 160 );
  assert ( window_2[1][1] == 170 );
  assert ( window_2[1][2] == 180 );
  assert ( window_2[2][0] == 210 );
  assert ( window_2[2][1] == 220 );
  assert ( window_2[2][2] == 230 );
  printf("======== passed! (corner_decoder: edge) ======== \n");
}

void corner_decoder_basic_test_large ( ) {

  int32_t corner_x;
  int32_t corner_y;  // the center point is 13
  corner_x = 2;
  corner_y = 4;

  int32_t image_1[image_in_rows][image_in_cols] = {

                                          2434643, 86759483, 6983623, 4629023, 55472653,
                                          6981534, 82650125, 5763514, 9087531, 14357831,
                                          9667324, 16535458, 8763420, 1038239, 90816245,
                                          1606864, 51938243, 9176240, 8586234, 84619107,
                                          6749856, 48765823, 5687368, 9686134, 59736450    };

  int32_t image_2[image_in_rows][image_in_cols] = {

                                          976234345, 48635413, 836516543, 974657134, 435678424,
                                          765134012, 37515643, 915347658, 412349074, 751234090,
                                          975123034, 95715202, 962651341, 769869900, 999999999,
                                          979687209, 35414325, 457454567, 890980769, 970681242,
                                          987808006, 75898246, 634192574, 585237491, 998851234    };

  int32_t window_1[num_rows][num_cols];
  int32_t window_2[num_rows][num_cols];

  corner_decoder(corner_x, corner_y, image_1, image_2, window_1, window_2);

  assert ( window_1[0][0] == 9667324 );
  assert ( window_1[0][1] == 16535458 );
  assert ( window_1[0][2] == 8763420 );
  assert ( window_1[1][0] == 1606864 );
  assert ( window_1[1][1] == 51938243 );
  assert ( window_1[1][2] == 9176240 );
  assert ( window_1[2][0] == 6749856 );
  assert ( window_1[2][1] == 48765823 );
  assert ( window_1[2][2] == 5687368 );

  assert ( window_2[0][0] == 975123034 );
  assert ( window_2[0][1] == 95715202 );
  assert ( window_2[0][2] == 962651341 );
  assert ( window_2[1][0] == 979687209 );
  assert ( window_2[1][1] == 35414325 );
  assert ( window_2[1][2] == 457454567 );
  assert ( window_2[2][0] == 987808006 );
  assert ( window_2[2][1] == 75898246 );
  assert ( window_2[2][2] == 634192574 );
  printf("======== passed! (corner_decoder: large) ======== \n");
}

void corner_decoder_test_collection () {

     corner_decoder_basic_test_1();
     corner_decoder_basic_test_edge();
     corner_decoder_basic_test_large();

}
