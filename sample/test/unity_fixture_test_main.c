#include "unity_fixture.h"
#include "calc.h"

TEST_GROUP(CalculatorTest);

TEST_SETUP(CalculatorTest) {
}

TEST_TEAR_DOWN(CalculatorTest) {
}

TEST(CalculatorTest, test_plus) {
  TEST_ASSERT_EQUAL(3, plus(1, 2));
}

TEST(CalculatorTest, test_minus) {
  TEST_ASSERT_EQUAL(-1, minus(1, 2));
}

TEST(CalculatorTest, test_multiply) {
  TEST_ASSERT_EQUAL(2, multiply(1, 2));
}

TEST(CalculatorTest, test_divide) {
  TEST_ASSERT_EQUAL_DOUBLE(0.5, divide(1, 2));
}

TEST_GROUP_RUNNER(CalculatorTest) {
  RUN_TEST_CASE(CalculatorTest, test_plus);
  RUN_TEST_CASE(CalculatorTest, test_minus);
  RUN_TEST_CASE(CalculatorTest, test_multiply);
  RUN_TEST_CASE(CalculatorTest, test_divide);
}

static void runAllTests(void) {
  RUN_TEST_GROUP(CalculatorTest);
}

int main(int argc, const char* argv[]) {
  return UnityMain(argc, argv, runAllTests);
}
