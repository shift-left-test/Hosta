#include "unity.h"

void setUp() {
}

void tearDown() {
}

void test_hello() {
  TEST_ASSERT_EQUAL("hello", "hello");
}

int main() {
  UNITY_BEGIN();
  RUN_TEST(test_hello);
  return UNITY_END();
}
