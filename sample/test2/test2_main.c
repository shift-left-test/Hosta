#include "unity.h"
#include "calc.h"

void setUp() {
}

void tearDown() {
}

void test_plus2() {
  TEST_ASSERT_EQUAL(0, plus(0, 0));
}

int main() {
  UNITY_BEGIN();
  RUN_TEST(test_plus2);
  return UNITY_END();
}
