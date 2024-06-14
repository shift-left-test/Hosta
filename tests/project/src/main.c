#include <stdio.h>
#include "calc.h"

int main() {
  printf("1 + 2 = %d\n", plus(1, 2));
  printf("1 - 2 = %d\n", minus(1, 2));
  printf("1 * 2 = %d\n", multiply(1, 2));
  printf("1 / 2 = %f\n", divide(1, 2));
  return 0;
}
