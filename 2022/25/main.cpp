#include <algorithm>
#include <string>
#include <vector>

#include "../lib/aoc.cpp"

using namespace std;

int64_t snafu_to_dec(const string& snafu) {
  int64_t dec = 0;
  for (int64_t i = 0; i < snafu.length(); ++i) {
    int64_t base = pow(5, snafu.length() - 1 - i);
    if (snafu[i] == '=')
      dec += -2 * base;
    else if (snafu[i] == '-')
      dec += -1 * base;
    else
      dec += (snafu[i] - '0') * base;
  }
  return dec;
}

string dec_to_snafu(int64_t dec) {
  string snafu = "";
  int64_t i = 0;
  for (; dec / pow(5, i) >= 2; ++i) {
  }

  int64_t remainder = dec;
  for (int64_t j = i; j >= 0; --j) {
    double times = remainder / pow(5, j);
    if (times > 1.5) {
      snafu += '2';
      remainder -= (2 * pow(5, j));
    } else if (times > 0.5) {
      snafu += '1';
      remainder -= pow(5, j);
    } else if (times > -0.5) {
      snafu += '0';
    } else if (times > -1.5) {
      snafu += '-';
      remainder += pow(5, j);
    } else {
      snafu += '=';
      remainder += (2 * pow(5, j));
    }
  }
  assert(remainder == 0);
  return snafu;
}

int main(int argc, char *argv[]) {
  int64_t sum = 0;
  for (const string& snafu : aoc::input_lines(argc, argv))
    sum += snafu_to_dec(snafu);
  aoc::output(dec_to_snafu(sum));
}
