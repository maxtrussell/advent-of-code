#include <string>
#include <vector>

#include <boost/algorithm/string/predicate.hpp>

#include "../../lib/aoc.cpp"

#include "md5.h"

using namespace std;

int main(int argc, char *argv[]) {
  const string key = aoc::input_lines(argc, argv)[0];
  const string p1_prefix = "00000";
  const string p2_prefix = "000000";
  int part1 = 0;

  int i = 0;
  while (true) {
    string hash = md5(key + to_string(i++));
    if (part1 == 0 && boost::starts_with(hash, p1_prefix))
      part1 = i - 1;
    if (boost::starts_with(hash, p2_prefix))
      break;
  }
  aoc::output(part1);
  aoc::output(i - 1);
}
