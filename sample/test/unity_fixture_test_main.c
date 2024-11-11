#include "fff.h"
#include "unity_fixture.h"
#include "calc.h"

DEFINE_FFF_GLOBALS;

TEST_GROUP(UnityFixtureTest);

TEST_SETUP(UnityFixtureTest) {
  FFF_RESET_HISTORY();
}

TEST_TEAR_DOWN(UnityFixtureTest) {
}

TEST(UnityFixtureTest, test_plus) {
  TEST_ASSERT_EQUAL(3, plus(1, 2));
}

TEST(UnityFixtureTest, test_minus) {
  TEST_ASSERT_EQUAL(-1, minus(1, 2));
}

TEST(UnityFixtureTest, test_multiply) {
  TEST_ASSERT_EQUAL(2, multiply(1, 2));
}

TEST(UnityFixtureTest, test_divide) {
  TEST_ASSERT_EQUAL_DOUBLE(0.5, divide(1, 2));
}

TEST_GROUP_RUNNER(UnityFixtureTest) {
  RUN_TEST_CASE(UnityFixtureTest, test_plus);
  RUN_TEST_CASE(UnityFixtureTest, test_minus);
  RUN_TEST_CASE(UnityFixtureTest, test_multiply);
  RUN_TEST_CASE(UnityFixtureTest, test_divide);
}

static void runAllTests(void) {
  RUN_TEST_GROUP(UnityFixtureTest);
}

int main(int argc, const char* argv[]) {
  return UnityMain(argc, argv, runAllTests);
}
