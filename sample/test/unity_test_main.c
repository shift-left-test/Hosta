#include "fff.h"
#include "unity.h"
#include "calc.h"

DEFINE_FFF_GLOBALS;

void setUp() {
  FFF_RESET_HISTORY();
}

void tearDown() {
}

void test_plus() {
  TEST_ASSERT_EQUAL(3, plus(1, 2));
}

void test_minus() {
  TEST_ASSERT_EQUAL(-1, minus(1, 2));
}

void test_multiply() {
  TEST_ASSERT_EQUAL(2, multiply(1, 2));
}

void test_divide() {
  TEST_ASSERT_EQUAL_DOUBLE(0.5, divide(1, 2));
}

int main() {
  UNITY_BEGIN();
  RUN_TEST(test_plus);
  RUN_TEST(test_minus);
  RUN_TEST(test_multiply);
  RUN_TEST(test_divide);
  return UNITY_END();
}
