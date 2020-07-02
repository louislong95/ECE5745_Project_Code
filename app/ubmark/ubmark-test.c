#include "common.h"
#include "stdint.h"

__attribute__ ((noinline))

int main( int argc, char* argv[] )
{
  int dest[2][2][2];
  int32_t a;

  dest[0][0][0] = 1;
  a = dest[1][1][1];

  return 0;
}
