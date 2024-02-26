#include "unity.h"
#include "calc.h"

void setUp() {
}

void tearDown() {
}

void test_plus() {
  TEST_ASSERT_EQUAL(3, plus(1, 2));
}

void test_minus() {
  TEST_ASSERT_EQUAL(-1, minus(1, 2));
}

int main() {
  UNITY_BEGIN();
  RUN_TEST(test_plus);
  RUN_TEST(test_minus);
  return UNITY_END();
}
