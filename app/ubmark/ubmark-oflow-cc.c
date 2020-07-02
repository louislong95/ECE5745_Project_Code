#include <stdio.h>
#include "stdint.h"
#include "common.h"
#include "ubmark-oflow-function/image_parameters.h"
//#include "ubmark-oflow-function/oflow-corner-decoder.c"
//#include "ubmark-oflow-function/oflow-derivative-t.c"
//#include "ubmark-oflow-function/oflow-derivative-x.c"
//#include "ubmark-oflow-function/oflow-derivative-y.c"
//#include "ubmark-oflow-function/oflow-matrix-2x2-multi-2x1.c"
//#include "ubmark-oflow-function/oflow-matrix-inverse-2x2.c"
//#include "ubmark-oflow-function/oflow-matrix-multi.c"
//#include "ubmark-oflow-function/oflow-pixel-sum.c"

#include "MATLAB_app/result_MATLAB/result_data/image_data_3d.dat"
#include "MATLAB_app/result_MATLAB/result_data/corner_x_coordi.dat"
#include "MATLAB_app/result_MATLAB/result_data/corner_y_coordi.dat"
#include "MATLAB_app/result_MATLAB/result_data/corner_nums.dat"

// include the reference arrays to check the result of the baseline
#include "MATLAB_app/result_MATLAB/result_data/vx_ref.dat"
#include "MATLAB_app/result_MATLAB/result_data/vy_ref.dat"
#include "MATLAB_app/result_MATLAB/result_data/de_ref.dat"

__attribute__ ((noinline))
void corner_decoder (
  int32_t corner_x,
  int32_t corner_y,
  int32_t image_1[image_in_rows][image_in_cols],
  int32_t image_2[image_in_rows][image_in_cols],
  int32_t window_1[num_rows][num_cols],
  int32_t window_2[num_rows][num_cols] ) {

     int i, j, k, h;
     int ii, jj, kk, hh; 

     ii = 0;
     for (i=corner_y-2; i<corner_y+1; i++) {
         jj = 0;
         for (j=corner_x-2; j<corner_x+1; j++) {
             window_1[ii][jj] = image_1[i][j];
             jj++;
         }
         ii++;
     }

     kk = 0;
     for (k=corner_y-2; k<corner_y+1; k++) {
         hh = 0;
         for (h=corner_x-2; h<corner_x+1; h++) {
             window_2[kk][hh] = image_2[k][h];
             hh++;
         }
         kk++;
     }
}

__attribute__ ((noinline))
void image_sptial_derivate_x (
  int32_t image[image_in_rows][image_in_cols],
  int32_t image_out[num_rows][num_cols],
  int32_t corner_x, int32_t corner_y )
{

    int i, j;
    int ii, jj;

    ii = 0; 
    for (i=corner_y-2; i<corner_y+1; i++) {
        jj=0;
        for (j=corner_x-2; j<corner_x+1; j++) {
            if (j==0) {
               image_out[ii][jj] = image[i][j+1] - 0;
            } //left border handling, zero-padding
            else if (j==(image_in_cols-1)) {
               image_out[ii][jj] = 0 - image[i][j-1];
            } //right border handling, zero-padding
            else if (j>(image_in_cols-1)) {
               image_out[ii][jj] = 0;
            }
            else {
               image_out[ii][jj] = image[i][j+1] - image[i][j-1];
            }
            jj++;
        }
        ii++;
    }

}

__attribute__ ((noinline))
void image_sptial_derivate_y (
  int32_t image[image_in_rows][image_in_cols],
  int32_t image_out[num_rows][num_cols],
  int32_t corner_x, int corner_y )
{

  int i, j;
  int ii, jj;

  jj = 0;
  for (j=corner_x-2; j<corner_x+1; j++) {
      ii=0;
      for (i=corner_y-2; i<corner_y+1; i++) {
          if (i==0) {
             image_out[ii][jj] = image[i+1][j] - 0;
          } //border handling
          else if (i==(image_in_rows-1)) {
             image_out[ii][jj] = 0 - image[i-1][j];
          }
          else if (i>(image_in_rows-1)) {
             image_out[ii][jj] = 0;
          }
          else {
             image_out[ii][jj] = image[i+1][j] - image[i-1][j];
          }
          ii++;
      }
      jj++;
  }
}

__attribute__ ((noinline))
void image_sptial_derivate_t (
   int32_t image_1[num_rows][num_cols],
   int32_t image_2[num_rows][num_cols],
   int32_t image_out[num_rows][num_cols])
{
   int i, j;

   for (i=0; i<num_rows; i++) {
       for (j=0; j<num_cols; j++) {
           image_out[i][j] = image_2[i][j] - image_1[i][j];
       }
   }
}

__attribute__ ((noinline))
void image_multiplication (
   int32_t image_1[num_rows][num_cols],
   int32_t image_2[num_rows][num_cols],
   int32_t image_out[num_rows][num_cols])
{
    int i, j;
    
    for (i=0; i<num_rows; i++) {
        for (j=0; j<num_cols; j++) {
            image_out[i][j] = image_1[i][j] * image_2[i][j];
         }
    } 
    

}

__attribute__ ((noinline))
int32_t image_pixel_sum (int32_t image[num_rows][num_cols]) {

    int i, j;
    int32_t sum = 0;

    for (i=0; i<num_rows; i++) {
        for (j=0; j<num_cols; j++) {
            sum = image[i][j] + sum;
            //wprintf(L"pixel sum is %d -> \n", sum);
        }
    }
    //return sum;
    sum = sum >> 5;

    return sum;

}  

__attribute__ ((noinline))
int32_t image_matrix_inverse_2x2 (int32_t matrix[2][2]) {

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

__attribute__ ((noinline))
void image_2x2_multi_2x1 (int32_t matrix_2x2[2][2], int32_t matrix_2x1[2], int32_t big_part[2]) {

     big_part[0] = matrix_2x2[0][0] * matrix_2x1[0] + matrix_2x2[0][1] * matrix_2x1[1];
     big_part[1] = matrix_2x2[1][0] * matrix_2x1[0] + matrix_2x2[1][1] * matrix_2x1[1];

}

__attribute__ ((noinline))
void verify_results (
     int32_t vx[],
     int32_t vy[],
     int32_t de[],
     int32_t vx_ref[],
     int32_t vy_ref[],
     int32_t de_ref[] ) 
{
     int32_t i;

     for (i=0; i< image_number*corner_number; i++) {
         if ( !(vx[i] == vx_ref[i]) ) {
             test_fail( i, vx[i], vx_ref[i] );
             wprintf(L"vx is wrong! \n");
         }

         if ( !(vy[i] == vy_ref[i]) ) {
             test_fail( i, vy[i], vy_ref[i] );
             wprintf(L"vy is wrong! \n");
         }

         if ( !(de[i] == de_ref[i]) ) {
             test_fail( i, de[i], de_ref[i] );
             wprintf(L"de is wrong! \n");
         }
     }  
 
     test_pass();
}

__attribute__ ((noinline))
int main (int argc, char* argv[]) {

    int i, j, corner_cnt;
    int32_t image_1[image_in_rows][image_in_cols];
    int32_t image_2[image_in_rows][image_in_cols];
    int32_t image_derivate_x[num_rows][num_cols];
    int32_t image_derivate_y[num_rows][num_cols];
    int32_t image_derivate_t[num_rows][num_cols];
    int32_t image_lx_square[num_rows][num_cols];
    int32_t image_ly_square[num_rows][num_cols];
    int32_t image_lx_mul_ly[num_rows][num_cols];
    int32_t image_lx_mul_lt[num_rows][num_cols];
    int32_t image_ly_mul_lt[num_rows][num_cols];
    int32_t image_lx_square_sum = 0;
    int32_t image_ly_square_sum = 0;
    int32_t image_lx_mul_ly_sum = 0;
    int32_t image_lx_mul_lt_sum = 0;
    int32_t image_ly_mul_lt_sum = 0;
    int32_t c_x, c_y;
    int32_t u_v_raw[2];
    int32_t vx[image_number * corner_number];
    int32_t vy[image_number * corner_number];
    int32_t de[image_number * corner_number];

    int32_t image_corner_window1[num_rows][num_cols];
    int32_t image_corner_window2[num_rows][num_cols];

    int32_t determinant;
    int     third_dimension;


    test_stats_on();
    
    for (third_dimension=0; third_dimension<image_number; third_dimension++) {

        wprintf(L"Processing on image # %d \n", third_dimension);
 
        for (i=0; i<image_in_rows; i++) {
            for (j=0; j<image_in_cols; j++) {
                image_1[i][j] = image_set_3d[third_dimension][i][j];
            }
        }

        for (i=0; i<image_in_rows; i++) {
            for (j=0; j<image_in_cols; j++) {
                image_2[i][j] = image_set_3d[third_dimension+1][i][j];
            }
        }

        for (corner_cnt=0; corner_cnt<corner_number; corner_cnt++) {

            c_x = corner_x[third_dimension][corner_cnt];
            c_y = corner_y[third_dimension][corner_cnt];

           // wprintf(L"now the corner number is %d \n", corner_cnt);

            //image_1_num=read_image_data(image_1, "test_small.dat");
            corner_decoder(c_x, c_y, image_1, image_2, image_corner_window1, image_corner_window2);
            /*wprintf(L"corner window 1 is: \n");
            for (i=0; i<num_rows; i++) {
                for (j=0; j<num_cols; j++) {
                    wprintf(L"%d,", image_corner_window1[i][j]);
                }
                wprintf(L"\n");
            };
            wprintf(L"=====================!! \n");  */

            /*wprintf(L"corner window 2 is: \n");
            for (i=0; i<num_rows; i++) {
                for (j=0; j<num_cols; j++) {
                    wprintf(L"%d,", image_corner_window2[i][j]);
                }
                wprintf(L"\n");
            };
            wprintf(L"=====================!! \n");   */

            image_sptial_derivate_x(image_1, image_derivate_x, c_x, c_y);
            /*wprintf(L"Ix is: \n");
            for (i=0; i<num_rows; i++) {
                for (j=0; j<num_cols; j++) {
                    wprintf(L"%d,", image_derivate_x[i][j]);
                }
                wprintf(L"\n");
            };
            wprintf(L"=====================!! \n");    */

            image_sptial_derivate_y(image_1, image_derivate_y, c_x, c_y);
            /*wprintf(L"Iy is: \n");
            for (i=0; i<num_rows; i++) {
                for (j=0; j<num_cols; j++) {
                    wprintf(L"%d,", image_derivate_y[i][j]);
                }
                wprintf(L"\n");
            };
            wprintf(L"=====================!! \n");   */

            image_sptial_derivate_t(image_corner_window1, image_corner_window2, image_derivate_t);
           /* wprintf(L"It is: \n");
            for (i=0; i<num_rows; i++) {
                for (j=0; j<num_cols; j++) {
                    wprintf(L"%d,", image_derivate_t[i][j]);
                }
                wprintf(L"\n");
            };
            wprintf(L"=====================!! \n");    */

            image_multiplication(image_derivate_x, image_derivate_x, image_lx_square);
           /* wprintf(L"Ix square is: \n");
            for (i=0; i<num_rows; i++) {
                for (j=0; j<num_cols; j++) {
                        wprintf(L"%d,", image_lx_square[i][j]);
                }
                wprintf(L"\n");
            };
            wprintf(L"=====================!! \n");   */

            image_multiplication(image_derivate_y, image_derivate_y, image_ly_square);
            /*wprintf(L"Iy square is: \n");
            for (i=0; i<num_rows; i++) {
                for (j=0; j<num_cols; j++) {
                        wprintf(L"%d,", image_ly_square[i][j]);
                }
                wprintf(L"\n");
            };
            wprintf(L"=====================!! \n");    */
            
            image_multiplication(image_derivate_x, image_derivate_y, image_lx_mul_ly);
          /*  wprintf(L"lx * ly square is: \n");
            for (i=0; i<num_rows; i++) {
                for (j=0; j<num_cols; j++) {
                        wprintf(L"%d,", image_lx_mul_ly[i][j]);
                }
                wprintf(L"\n");
            };
            wprintf(L"=====================!! \n");   */ 

            image_multiplication(image_derivate_x, image_derivate_t, image_lx_mul_lt);
         /*  wprintf(L"lx * lt square is: \n");
            for (i=0; i<num_rows; i++) {
                for (j=0; j<num_cols; j++) {
                        wprintf(L"%d,", image_lx_mul_lt[i][j]);
                }
                wprintf(L"\n");
            };
            wprintf(L"=====================!! \n");   */

            image_multiplication(image_derivate_y, image_derivate_t, image_ly_mul_lt);
          /*  wprintf(L"ly * lt square is: \n");
            for (i=0; i<num_rows; i++) {
                for (j=0; j<num_cols; j++) {
                        wprintf(L"%d,", image_ly_mul_lt[i][j]);
                }
                wprintf(L"\n");
            };
            wprintf(L"=====================!! \n");    */

            image_lx_square_sum = image_pixel_sum(image_lx_square);
            image_ly_square_sum = image_pixel_sum(image_ly_square);
            image_lx_mul_ly_sum =image_pixel_sum(image_lx_mul_ly);
            image_lx_mul_lt_sum =image_pixel_sum(image_lx_mul_lt);
            image_ly_mul_lt_sum =image_pixel_sum(image_ly_mul_lt);
             
            //image_pixel_sum(image_lx_square, &image_lx_square_sum);
            //image_pixel_sum(image_ly_square, &image_ly_square_sum);
            //image_pixel_sum(image_lx_mul_ly, &image_lx_mul_ly_sum);
            //image_pixel_sum(image_lx_mul_lt, &image_lx_mul_lt_sum);
            //image_pixel_sum(image_ly_mul_lt, &image_ly_mul_lt_sum);

            image_lx_mul_lt_sum = image_lx_mul_lt_sum * (-1);
            image_ly_mul_lt_sum = image_ly_mul_lt_sum * (-1);
            //wprintf(L"lx_square_sum is %d \n", image_lx_square_sum);
            //wprintf(L"ly_square_sum is %d \n", image_ly_square_sum);
            //wprintf(L"lx X ly sum is %d \n", image_lx_mul_ly);
            //wprintf(L"lx X lt sum is %d \n", image_lx_mul_lt);
            //wprintf(L"ly X lt sum is %d \n", image_ly_mul_lt);
        

            // organize the 2x2 martix
            int32_t matrix_2x2[2][2] = {0,0,0,0};
            matrix_2x2[0][0] = image_lx_square_sum;
            matrix_2x2[0][1] = image_lx_mul_ly_sum;
            matrix_2x2[1][0] = image_lx_mul_ly_sum;
            matrix_2x2[1][1] = image_ly_square_sum;
          /*  wprintf(L"The pre- 2x2 matrix is: \n");
            for (i=0; i<2; i++) {
                for (j=0; j<2; j++) {
                    wprintf(L"%d,", matrix_2x2[i][j]);
                }
                wprintf(L"\n");
            };
            wprintf(L"=====================!! \n");    */

            determinant  = image_matrix_inverse_2x2(matrix_2x2);
           /* wprintf(L"The determinant is %d: \n", determinant);
            wprintf(L"The 2x2 matrix is: \n");
            for (i=0; i<2; i++) {
                for (j=0; j<2; j++) {
                    wprintf(L"%d,", matrix_2x2[i][j]);
                }
                wprintf(L"\n");
            };
            wprintf(L"=====================!! \n");   */

            int32_t matrix_2x1[2] = {0,0};
            matrix_2x1[0] = image_lx_mul_lt_sum;
            matrix_2x1[1] = image_ly_mul_lt_sum;
            image_2x2_multi_2x1(matrix_2x2, matrix_2x1, u_v_raw);

            vx[third_dimension*corner_number+corner_cnt] = u_v_raw[0];
            vy[third_dimension*corner_number+corner_cnt] = u_v_raw[1];
            de[third_dimension*corner_number+corner_cnt] = determinant;

          /*  wprintf(L"raw u is %d \n", u_v_raw[0]);
            wprintf(L"raw v is %d \n", u_v_raw[1]);
            wprintf(L"=====================!! \n");


            wprintf(L"corner_x is %d \n", c_x);
            wprintf(L"corner_y is %d \n", c_y);
            wprintf(L"corner_cnt now is %d \n", corner_cnt);
            wprintf(L"currently is on %d \n", third_dimension);  */
            
        }

    }

    test_stats_off();

    verify_results(vx, vy, de, vx_ref, vy_ref, de_ref);

    //return 0;
    exit(0);
}
