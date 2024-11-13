#include <memory>
#include <gtest/gtest.h>
#include "calc.hpp"

class GoogleTest : public ::testing::Test {
 protected:
  void SetUp() override {
    calculator = std::make_shared<Calculator>();
  }

  void TearDown() override {
  }

  std::shared_ptr<Calculator> calculator;
};

TEST_F(GoogleTest, test_plus) {
  EXPECT_EQ(3, calculator->plus(1, 2));
}

TEST_F(GoogleTest, DISABLED_test_minus) {
  EXPECT_EQ(-1, calculator->minus(1, 2));
}

TEST_F(GoogleTest, test_multiply) {
  EXPECT_EQ(2, calculator->multiply(1, 2));
}

TEST_F(GoogleTest, test_divide) {
  EXPECT_EQ(0.5, calculator->divide(1, 2));
}

int main(int argc, char* argv[]) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
