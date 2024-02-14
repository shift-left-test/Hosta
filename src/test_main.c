#include "unity.h"

void setUp() {
}

void tearDown() {
}

int add(int x, int y) {
  return x + y;
}

int minus(int x, int y) {
  return x - y;
}

void test_add() {
  TEST_ASSERT_EQUAL(3, add(1, 2));
}

void test_minus() {
  TEST_ASSERT_EQUAL(-1, minus(1, 2));
}

int main() {
  UNITY_BEGIN();
  RUN_TEST(test_add);
  RUN_TEST(test_minus);
  return UNITY_END();
}
