#include <gtest/gtest.h>

extern "C" {
  #include "calc.h"
}

class GoogleTest : public ::testing::Test {
 protected:
  void SetUp() override {
  }

  void TearDown() override {
  }
};

TEST_F(GoogleTest, test_plus) {
  EXPECT_EQ(3, plus(1, 2));
}

TEST_F(GoogleTest, test_minus) {
  EXPECT_EQ(-1, minus(1, 2));
}

TEST_F(GoogleTest, test_multiply) {
  EXPECT_EQ(2, multiply(1, 2));
}

TEST_F(GoogleTest, test_divide) {
  EXPECT_EQ(0.5, divide(1, 2));
}

int main(int argc, char* argv[]) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
