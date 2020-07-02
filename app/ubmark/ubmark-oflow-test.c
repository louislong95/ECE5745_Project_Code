#include <stdio.h>
#include "stdint.h"
#include <assert.h>

#include "ubmark-oflow-function/image_parameters.h"
#include "ubmark-oflow-test/oflow-test-corner-decoder.c"
#include "ubmark-oflow-test/oflow-test-derivative-x.c"
#include "ubmark-oflow-test/oflow-test-derivative-y.c"
#include "ubmark-oflow-test/oflow-test-derivative-t.c"
#include "ubmark-oflow-test/oflow-test-matrix-multi.c"
#include "ubmark-oflow-test/oflow-test-pixel-sum.c"
#include "ubmark-oflow-test/oflow-test-matrix-inverse-2x2.c"
#include "ubmark-oflow-test/oflow-test-matrix-2x2-multi-2x1.c"

int main () { 
    
    corner_decoder_test_collection();
    derivative_x_test_collection();
    derivative_y_test_collection();
    derivative_t_test_collection();
    matrix_multi_test_collection();
    pixel_sum_test_collection();
    matrix_inverse_2x2_test_collection();
    matrix_2x2_multi_2x1_test_collection();

}